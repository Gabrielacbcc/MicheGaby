# Stage 4: Candidate profile language (context-free grammar, textX)

Stage 4 does not extract, normalize or classify anything. It fixes how the results of Stages 1 to 3 must be written so that another program (or a person) can rely on their structure. The language is a small domain-specific language (DSL): `build_profile_text` writes a text in it, `validate_profile` checks the text with a textX grammar and `render_html` / `render_markdown` draw the validated model.

The grammar lives in `src/stage4_grammar/candidate.tx`.

## Example of a valid text

```
candidate "Wednesday Addams" {
  contact {
    email: wednesday.addams@nevermore.edu;
    phone: +57 300 555 0199;
  }
  education {
    degree "BSc in Computer Science" at "Nevermore Academy" year 2024;
  }
  experience {
    role "Web Application Developer" at "Nevermore Academy Projects" for 3 years;
    role "Freelance Developer" at "Self-employed" for 1 year;
  }
  qualifications FULL_STACK_DEVELOPER { JAVASCRIPT, REACT, NODE_JS, REST_API, POSTGRESQL, GIT }
  qualifications MACHINE_LEARNING_ENGINEER { POSTGRESQL, GIT }
  qualifications DEVOPS_ENGINEER { GIT }
  qualifications DATA_ENGINEER { POSTGRESQL, GIT }
  profile FULL_STACK_DEVELOPER: ACCEPTED;
  profile MACHINE_LEARNING_ENGINEER: REJECTED;
  profile DEVOPS_ENGINEER: REJECTED;
  profile DATA_ENGINEER: REJECTED;
}
```

## Grammar in EBNF

Non-terminals are written in CamelCase, terminals are quoted strings or regular expressions between slashes.

```
Candidate         = 'candidate' ( NameString | 'unnamed' ) '{'
                      Contact EducationSection ExperienceSection
                      Qualifications { Qualifications }
                      Result { Result }
                    '}' ;
Contact           = 'contact' '{' [ 'email' ':' Email ';' ] [ 'phone' ':' Phone ';' ] '}' ;
EducationSection  = 'education' '{' { EducationEntry } '}' ;
EducationEntry    = 'degree' NameString 'at' NameString 'year' Year ';' ;
ExperienceSection = 'experience' '{' { ExperienceEntry } '}' ;
ExperienceEntry   = 'role' NameString 'at' NameString 'for' Duration ';' ;
Qualifications    = 'qualifications' ProfileName '{' [ Token { ',' Token } ] '}' ;
Result            = 'profile' ProfileName ':' Status ';' ;

ProfileName = 'FULL_STACK_DEVELOPER' | 'MACHINE_LEARNING_ENGINEER'
            | 'DEVOPS_ENGINEER' | 'DATA_ENGINEER' ;
Status      = 'ACCEPTED' | 'REJECTED' ;
```

| Terminal | Pattern | Role |
|----------|---------|------|
| `Token` | `[A-Z][A-Z0-9_]*` | canonical qualification produced by Stage 2 |
| `Email` | `[\w.+-]+@[\w-]+(\.[\w-]+)+` | contact e-mail |
| `Phone` | `\+?\d[\d ()-]{5,18}\d` | contact phone |
| `Year` | `(19\|20)\d{2}` | graduation year |
| `Duration` | `\d+ years?` | length of a job |
| `NameString` | `"([^"\\\n]\|\\.)+"` | non empty quoted text, `\"` and `\\` escaped |
| keywords | `candidate`, `contact`, `education`, ... | fixed words of the language |

## Structural characteristics

- **Nesting.** A candidate contains sections, and sections contain entries. The language is not regular because blocks use matching braces, which a finite automaton cannot count; the nesting needs a stack, hence a context-free grammar.
- **Repetition.** `EducationEntry`, `ExperienceEntry`, `Qualifications` and `Result` repeat, so a resume can have any number of degrees and jobs.
- **Optional parts.** E-mail and phone are optional because Stage 1 leaves out a field it does not find; the name can be replaced by `unnamed`.
- **Lexical layer.** Terminals are regular expressions, so the lexical rules (what an e-mail, a year or a token looks like) are regular languages and the syntactic rules are context-free.
- **Deterministic reading.** Every rule starts with a different keyword, so a parser always knows which rule applies by reading one token (the grammar is LL(1) apart from the lists separated by commas).

## What the grammar cannot say (semantic checks)

A context-free grammar cannot say "every profile appears exactly once" or "the verdict agrees with the automaton". `validate_profile` checks these after parsing and raises `ProfileValidationError`:

1. each of the four profiles has exactly one `qualifications` block and one verdict;
2. every token belongs to the alphabet of its profile;
3. the verdict is the one the Stage 3 automaton gives for those tokens.

## Rejected representations

Text that breaks a lexical rule (`email: not-an-email;`, `year 24;`, `for three years;`, a lowercase token), a syntactic rule (a misspelled keyword, a status other than `ACCEPTED` / `REJECTED`) or a semantic rule above is rejected with an error and nothing is rendered. These cases are in `tests/test_stage4_grammar.py`.

## Visualization

`render_html(model)` returns a self-contained HTML page (name, contact, education, experience and a table with the four verdicts); `render_markdown(model)` returns the same content in Markdown. Both only receive a validated model, and the HTML renderer escapes all text. Run `python -m src analyze data/sample_resumes/wednesday_addams.txt --format html --out report.html` and open the file in a browser.

## Limitation

textX is built on parsing expression grammars (PEG): alternatives are tried in order and the first match wins, while a context-free grammar treats alternatives as unordered. For this DSL both give the same language because every alternative starts with a different keyword, but a grammar with overlapping alternatives could behave differently in textX.
