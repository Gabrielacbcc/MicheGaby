# Regular Expression Patterns

This document explains the regular expressions behind Stage 1 of the pipeline, one section per field the guide asks the extractor to recognize. It grows together with the code in src/stage1_extraction, so each section here matches one extractor function already present in that package.

## Contact information

The resume text is expected to contain an email address and, usually, a phone number, each on its own line rather than buried inside a sentence. Two independent patterns are used instead of one combined pattern, since the two fields do not have to sit next to each other and either one might be missing from a given resume.

The email pattern is [\w.+-]+@[\w-]+\.[\w.-]+. It matches the ordinary shape of an address: one or more word characters, dots, plus signs or hyphens before the @ sign, then a domain name made of word characters and hyphens, then a dot and at least one more domain segment. This is intentionally looser than a strict RFC compliant pattern, since the goal here is to locate a string that looks like an email inside free text, not to validate a form field.

The phone pattern is (?:\+?\d{1,3}[\s-]?)?\d{3}[\s-]?\d{3}[\s-]?\d{4}. It was written with Colombian numbers in mind, since that is what our sample resumes use: an optional country code of up to three digits, possibly preceded by a plus sign, followed by three digit groups of three, three and four digits that can be separated by spaces, hyphens, or nothing at all. This covers both a longer form such as +57 300 555 0199 and a bare ten digit number such as 3005550199.

extract_contact_info runs both patterns against the full text with re.search, so it finds the first match wherever it occurs instead of requiring the field to sit at a fixed position in the resume, and it returns a dictionary that only includes the keys it actually matched. A resume with no phone number ends up with just an email key, not a phone key set to None, which keeps the output honest about what was actually found in the text.
