# Regular Expression Patterns

This document explains the regular expressions behind Stage 1 of the pipeline, one section per field the guide asks the extractor to recognize. It grows together with the code in src/stage1_extraction, so each section here matches one extractor function already present in that package.

## Contact information

The resume text is expected to contain an email address and, usually, a phone number, each on its own line rather than buried inside a sentence. Two independent patterns are used instead of one combined pattern, since the two fields do not have to sit next to each other and either one might be missing from a given resume.

The email pattern is [\w.+-]+@[\w-]+\.[\w.-]+. It matches the ordinary shape of an address: one or more word characters, dots, plus signs or hyphens before the @ sign, then a domain name made of word characters and hyphens, then a dot and at least one more domain segment. This is intentionally looser than a strict RFC compliant pattern, since the goal here is to locate a string that looks like an email inside free text, not to validate a form field.

The phone pattern is (?:\+?\d{1,3}[\s-]?)?\d{3}[\s-]?\d{3}[\s-]?\d{4}. It was written with Colombian numbers in mind, since that is what our sample resumes use: an optional country code of up to three digits, possibly preceded by a plus sign, followed by three digit groups of three, three and four digits that can be separated by spaces, hyphens, or nothing at all. This covers both a longer form such as +57 300 555 0199 and a bare ten digit number such as 3005550199.

extract_contact_info runs both patterns against the full text with re.search, so it finds the first match wherever it occurs instead of requiring the field to sit at a fixed position in the resume, and it returns a dictionary that only includes the keys it actually matched. A resume with no phone number ends up with just an email key, not a phone key set to None, which keeps the output honest about what was actually found in the text.

## Programming languages, frameworks, databases and tools

These four fields are handled together in technical_skills.py because they share the same underlying technique: rather than writing a pattern that describes the general shape of a technology name, which does not really exist, each category is a plain list of the raw spellings we expect to see for that category's qualifications, and the pattern is built by joining that list into a single alternation. Programming languages covers things like JS or Python, frameworks covers React.js or TensorFlow, databases covers Postgres or SQL, and tools covers Git or Docker, following the same split the guide uses in its list of information types.

This only works because Stage 1 does not need to decide that "JS" and "Javascript" are the same qualification, it only needs to notice that something matching one of the known spellings showed up in the text. That equivalence decision belongs to Stage 2, so every raw spelling we are aware of is listed separately here rather than folded into a single term, even when two entries will end up meaning the same thing later.

The order inside each list matters. A compound name like React.js has to appear before the bare word React, because regex alternation tries each option in the order it is written and stops at the first one that matches at a given position; if React came first, it would match the "React" inside "React.js" and leave the ".js" part behind. Keeping specific, longer names ahead of their shorter, more generic relatives avoids this.

One more case came up while testing: the word boundary check that keeps "JS" from matching inside longer words treats a dot as a boundary too, which means the "js" at the end of "React.js" or "Node.js" looks, on its own, exactly like a standalone mention of the JS language. To avoid counting it twice, under two different categories, a match is dropped whenever it is immediately preceded by a dot with no space before it, since in practice that pattern only shows up at the tail of a dotted framework name, never as a real standalone qualification on its own line.
