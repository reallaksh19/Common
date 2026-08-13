# Install Grade 4 Skill

This directory is a self-contained Agent Skill bundle.

## ChatGPT

If your account/workspace supports Skills:

1. Open **Plugins** in the ChatGPT sidebar.
2. Open the **Skills** tab.
3. Choose **Create** -> **Upload from your computer**.
4. Upload the `grade4` skill folder (or a ZIP containing this folder, if the upload UI accepts ZIP on your surface).
5. Review the generated skill draft and choose **Install**.

After installation, ChatGPT can use the skill automatically when relevant, or you can explicitly invoke it with `@grade4` where @-mentioning Skills is supported.

## Example prompts

- `@grade4 Create a Grade 4 Division learning cell for interpreting remainders.`
- `@grade4 Analyze these Grade 4 Math textbook pages and build a chapter blueprint.`
- `@grade4 Create a 30-question Division diagnostic with misconception probes and repair paths.`
- `@grade4 Turn this validated Division chapter into student and teacher PDF-ready editions.`
- `@grade4 Build a Grade 4 reading-inference lesson from this story.`

## Bundle layout

```text
grade4/
├── SKILL.md
├── INSTALL.md
└── references/
    ├── workflows/
    │   ├── grade4-math.md
    │   ├── grade4-english.md
    │   └── grade4-publishing.md
    └── schemas/
        ├── Grade4MathSchema.md
        ├── Grade4EnglishSchema.md
        ├── Grade4PublishingSchema.md
        ├── Grade4MathDivisionSchema.md
        └── Grade4MathDivisionPublishingContract.md
```

The root `SKILL.md` is intentionally compact. It uses progressive disclosure: it loads the appropriate workflow/schema references only when needed.
