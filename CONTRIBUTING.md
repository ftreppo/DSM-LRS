# Contributing to DSM-LRS

DSM-LRS is an open project with a strict privacy boundary.

## Community Adapter Lab

If you want to contribute a real-world Adapter result without changing code, use the structured GitHub Issue Form:

**Submit an Adapter Example / Beispiel einreichen / Invia un esempio**

https://github.com/ftreppo/DSM-LRS/issues/new?template=adapter-example.yml

The submission is public.

Before submitting:
- remove personal/student information;
- do not upload diagnoses, clinical reports or PDP/Förderplan documents;
- do not include private Drive links, credentials or correspondence;
- share only material you have the right to share;
- when material is copyrighted/confidential, use a short synthetic/anonymized equivalent that reproduces the behavior.

Raw submissions are reviewed first. They do not automatically become canonical examples or Adapter rules.

See:
- [Community Adapter Lab](docs/community/COMMUNITY_ADAPTER_LAB.md)
- [Review Checklist](docs/community/REVIEW_CHECKLIST.md)
- [Improvement Register](docs/community/IMPROVEMENT_REGISTER.md)

## Code / documentation scope

Contributions may cover public product code, specifications, documentation, tests, synthetic examples and the public website.

## Privacy boundary

Never submit student data, diagnoses, PDPs, clinical reports, names, grades, signatures, student numbers, access tokens, private Google Drive links or other protected/personalized material.

Use synthetic data for examples and tests.

## Architecture

Keep DSM-LRS independent from MindMap, Notion and personal infrastructure.

The generic Adapter has passed its standalone extraction gate and will move to the separate `lrs-adapter` repository once that repository is created. Generic Adapter community submissions should eventually follow the generic Adapter there; DSM-LRS may retain DSM-specific integrations and case studies.

Before substantial structural changes, check [docs/roadmap.md](docs/roadmap.md).
