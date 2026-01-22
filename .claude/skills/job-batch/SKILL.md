---
name: job-batch
description: Process a batch of job applications - discover roles, prepare materials, pre-fill forms. Use when ready to apply to multiple positions.
---

# Job Application Batch Processor

*Slash command: `/job-batch`*

## Purpose

Process a batch of job applications: discover roles, prepare materials, pre-fill forms, and present for user review.

---

## Workflow

### Phase 1: Discovery
1. Search for roles matching CLAUDE.md criteria
2. Verify each role is still open via Playwright
3. Check `applications/history.json` for duplicates
4. Create batch of 10 candidates

### Phase 2: User Selection
1. Present batch with compensation, location, fit assessment
2. User selects which to proceed with
3. Create folders in `applications/pending/{company}_{role}_{date}/`

### Phase 3: Research & Materials
1. Navigate to each job posting via Playwright
2. Extract full job description to `notes.md`
3. Write fit assessment
4. Generate cover letter following anti-AI-writing guidelines
5. Fill any application-specific questions in `responses.md`

### Phase 4: Form Pre-fill
1. Open each application in separate Playwright tab
2. Fill standard fields:
   - Name, email, phone, location
   - LinkedIn, GitHub URLs
   - Resume upload (CV PDF)
   - Cover letter (paste or upload)
3. Leave tabs open for user review
4. DO NOT submit - wait for user

### Phase 5: Report
Generate summary with:
- Tab index for each application
- Company, role, compensation
- Cover letter preview
- Any fields that couldn't be auto-filled
- Questions requiring custom answers

---

## Job Board Handling

### Greenhouse (AI2, many others)
- Standard form structure
- Resume upload, cover letter text area
- May have custom questions

### Ashby (Genesis, Insitro)
- Clean modern forms
- Often has "How did you hear about us?"
- Resume upload supported

### Workday (Flatiron/Simons, PacBio)
- Complex multi-step forms
- May require account creation
- Often has duplicate entry issues

### Lever
- Simple single-page forms
- Resume + cover letter + optional fields

### Interfolio (Academic)
- Academic-specific
- May require separate documents (CV, research statement)

---

## Standard Field Values

Read from user's `.claude/CLAUDE.md` and `profile.json`:
- Name, email, phone, location
- LinkedIn, GitHub URLs
- Resume path (typically `documents/*.pdf`)

Users must configure these files before using batch processing. See `GETTING_STARTED.md`.

---

## Anti-AI Writing Checklist

Before finalizing any cover letter, verify:
- [ ] No "delve," "tapestry," "multifaceted," "pivotal"
- [ ] Em dashes < 2
- [ ] Contains at least one contraction
- [ ] Varied paragraph lengths
- [ ] Specific technical details
- [ ] No generic company praise

See: `/anti-ai-writing` skill

---

## Output

After pre-filling, provide:

```
## Applications Ready for Review

| Tab | Company | Role | Comp | Status |
|-----|---------|------|------|--------|
| 1 | Flatiron | Sr SWE Lead | $190-235K | Ready |
| 2 | Genesis | ML Scientist | Competitive | Ready |
...

### Tab 1: Flatiron Institute
- URL: [link]
- Cover letter: [preview first 200 chars]
- Unfilled fields: None
- Notes: Workday may have asked for duplicate info

[etc for each tab]

### Next Steps
1. Review each tab
2. Edit any fields as needed
3. Submit when ready
4. I'll move to `applications/submitted/` and update history.json
```
