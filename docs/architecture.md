# System Architecture

This document covers the first part of the design deliverable: how ResumeLens is organized as a pipeline and what data moves between its stages. The function level detail for each module is kept separate, in module-design.md, since that part depends on decisions made here.

## Overview

ResumeLens is a linear pipeline split across four packages under src/, one per stage of the guide: stage1_extraction, stage2_normalization, stage3_recognition and stage4_grammar. Each package exposes a small set of functions that the next stage consumes, and a thin orchestrator module ties the four stages together so that all four supported profiles are processed through the same code path, instead of through independent implementations per profile, as required by the guide.

A single resume is always pushed through the full pipeline once per profile under consideration. The output of one stage never skips ahead to a later stage, and no stage reaches back into an earlier one: Stage 1 does not know what a profile is, Stage 2 does not parse raw text, and Stage 3 never looks at the original resume again once it has its normalized sequence.

## Data flow between stages

Stage 1 receives the raw resume text as a plain string and returns a structured but not yet normalized representation, grouping the fields the guide asks for: contact information, a list of raw qualification strings exactly as they appear in the text (for example "JS", "React.js", "Postgres"), education entries and experience entries. Nothing at this point has been checked for equivalence. "JS" and "Javascript" are still two different strings as far as Stage 1 is concerned, and that is intentional, since the guide treats extraction and normalization as separate concerns.

Stage 2 receives the raw qualification list produced by Stage 1 together with the name of the profile being evaluated, and returns a normalized list of canonical tokens in the order that profile defines. The profile name decides two things at once: which transducer runs (because the set of qualifications that matter differs between, say, Full Stack Developer and Data Engineer) and what canonical order the sorting step applies afterward, since the guide's example order (Frontend, then Backend, then Database, then Version control for Full Stack Developer) is itself specific to the profile rather than a fixed global order.

Stage 3 receives the normalized, ordered sequence from Stage 2 together with the automaton built for one profile, and returns a boolean result, accepted or rejected, for that profile only. Because a single resume needs to be checked against all four profiles, Stage 3 is invoked once per profile with the sequence Stage 2 produced for that same profile, and the four results are collected before moving on.

Stage 4 receives everything produced so far: the contact, education and experience fields from Stage 1, the normalized qualifications from Stage 2, and the per profile acceptance results from Stage 3. It assembles this information into the concrete syntax of the candidate profile DSL, validates that text against the grammar defined with textX, and if the text is valid renders the HTML or Markdown visualization. If the text is not valid, Stage 4 reports which rule of the grammar was violated instead of silently producing an output, since the guide explicitly asks the system to reject representations that break the DSL's lexical or syntactic rules.

## Module layout

The repository already reflects this split:

src/stage1_extraction holds the regular expression based extraction functions, one group of functions per field type plus one function that aggregates all of them into a single result for a resume.

src/stage2_normalization holds the finite-state transducers, built with pyformlang, and the canonical ordering tables, one of each per profile.

src/stage3_recognition holds the finite automata, also built with pyformlang, and the classification function, one automaton per profile.

src/stage4_grammar holds the textX grammar file, the functions that build and validate a candidate profile instance, and the HTML or Markdown renderer.

A new module, src/pipeline.py, will hold the orchestrator that calls the four stages in order for a given resume and a given list of profiles, and is the only place in the codebase that is allowed to know about all four stages at once.
