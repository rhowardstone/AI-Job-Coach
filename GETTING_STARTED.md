# Getting Started with AI Career Coach

This guide will help you set up the toolkit and learn how to work with Claude as your career coach.

## What This Toolkit Does

Traditional job applications have notoriously low success rates. Research suggests 50-80% of positions are filled through networking before being publicly posted.

This toolkit implements an alternative approach grounded in career development research:

1. **Research people** whose work genuinely interests you
2. **Build relationships** through informational conversations
3. **Demonstrate value** before formal hiring processes
4. **Apply formally** as backup/formality

The key insight: treat job search as relationship-building, not mass application submission.

---

## Installation

### Prerequisites
- [Claude Code](https://claude.ai/code) installed
- Python 3.8+ (for search scripts)
- Git
- **Optional**: Browser automation plugin (e.g., [Playwright MCP](https://github.com/anthropics/anthropic-cookbook/tree/main/misc/mcp_playwright)) for form-filling assistance

### Setup

```bash
# Clone the repo
git clone https://github.com/rhowardstone/AI-Job-Coach.git
cd AI-Job-Coach

# Install Python dependencies
pip install python-jobspy pandas requests

# Optional: Set up email verification
export HUNTER_API_KEY="your_key_here"  # Free at hunter.io
```

### Configure Your Profile

1. **Copy the template:**
   ```bash
   cp toolkit/profile_template.json profile.json
   ```

2. **Edit `profile.json`** with your info:
   - Name, email, phone
   - LinkedIn, GitHub (if applicable)
   - Location and relocation preferences

3. **Edit `.claude/CLAUDE.md`** with:
   - Your background and key differentiators
   - Target roles and companies
   - Compensation requirements
   - Hard constraints (what NOT to apply to)
   - References

4. **Add your resume** to `documents/` folder

5. **Start Claude Code:**
   ```bash
   claude
   ```

---

## How to Talk to Your Career Coach

Claude Code with this toolkit acts as a career coach, not just a form-filler. Here's how to interact effectively.

### Starting a Session

When you start Claude Code in this directory, it automatically loads:
- Your profile from `.claude/CLAUDE.md`
- All skills in `.claude/skills/`
- Your application history

**Good first prompts:**
- "Search for [role type] jobs at [company type]"
- "Research people at [company] whose work might interest me"
- "Help me understand what [company] is working on"
- "Review my application materials for [company]"

### The Interactive Workflow

This toolkit is designed for **conversation**, not automation. Here's the flow:

```
You: "Research people at Stripe whose work might interest me"

Claude: [Researches, finds people, summarizes their work]
        "Here's what I found about Jane Smith - she works on..."
        "Could you honestly talk to this person for 20 minutes
         and you'd both be fascinated?"

You: "Yes, her fraud detection work is interesting"
     OR "No, that's not my area - who else?"

Claude: [If yes, helps draft outreach]
        [If no, moves on to next person]
```

**The key question Claude will ask:** "Could you honestly talk to this person for 20 minutes about their work, and you'd BOTH be fascinated?"

If the answer is no, don't force it. Move on. Fake enthusiasm is obvious and counterproductive.

### What You Do vs. What Claude Does

| Claude Does | You Do |
|-------------|--------|
| Research companies and people | Validate genuine interest |
| Find their actual work (papers, talks, GitHub) | Read the summaries, click links if curious |
| Draft outreach emails | Review, edit, and SEND |
| Fill application forms | Click SUBMIT |
| Track applications | Confirm when you've submitted |
| Suggest follow-ups | Decide when/whether to follow up |

**Critical rule:** Claude NEVER sends emails or clicks submit. You always make the final human contact.

### Slash Commands (Skills)

| Command | What It Does |
|---------|--------------|
| `/apply` | Relationship-focused application workflow |
| `/job-search` | Search across job boards |
| `/job-batch` | Process multiple applications at once |
| `/ats-review` | Score resume against job description |
| `/interview-prep` | Generate questions + STAR feedback |
| `/anti-ai-writing` | Style guide for human-sounding text |

### Example Conversations

**Finding Jobs:**
```
You: "Search for ML engineer jobs in Seattle paying over $180k"
Claude: [Runs search, presents results with fit assessment]

You: "That Stripe role looks interesting. Research people there."
Claude: [Researches, presents spark notes on relevant people]
```

**Preparing Outreach:**
```
You: "I read about Jane's work on fraud detection. Yes, I could
     genuinely talk to her about that for 20 minutes."
Claude: [Drafts outreach email following elite methodology]
        "Here's a draft. It focuses on her work, not your job hunt..."

You: "Change the second paragraph to mention my similar experience"
Claude: [Revises draft]

You: "Good. I'll send that."
Claude: [Records in tracking, suggests follow-up timeline]
```

**Applying to Jobs:**
```
You: "Apply to the Stripe ML Engineer role"
Claude: [Opens application, fills all fields, leaves tab open]
        "Application pre-filled. Review and submit when ready."

You: "Submitted"
Claude: [Moves to submitted folder, updates tracking]
```

---

## File Locations (Absolute Paths)

When Claude refers to files, it uses absolute paths. Here's the structure:

```
/path/to/AI-Job-Coach/
├── .claude/
│   ├── CLAUDE.md              # YOUR profile and preferences
│   ├── settings.json          # Project config
│   └── skills/                # Auto-discovered skills
│       ├── apply/SKILL.md
│       ├── job-search/SKILL.md
│       ├── job-batch/SKILL.md
│       ├── ats-review/SKILL.md
│       ├── interview-prep/SKILL.md
│       └── anti-ai-writing/SKILL.md
├── toolkit/
│   ├── scripts/               # Python automation
│   │   ├── job_search.py
│   │   ├── greenhouse_search.py
│   │   └── email_finder.py
│   └── profile_template.json
├── templates/
│   ├── cover_letter.tex
│   └── history_template.json  # Application tracking schema
├── documents/
│   └── [your resume here]
├── applications/
│   ├── pending/               # Pre-filled, awaiting your review
│   ├── submitted/             # You've submitted these
│   └── history.json           # Tracking data
├── profile.json               # Your personal info (gitignored)
└── GETTING_STARTED.md         # This file
```

---

## The Methodology

This toolkit implements research-backed career development frameworks:

### Weak Tie Theory (Granovetter, 1973)
- 55.6% of jobs found through personal contacts
- Predominantly "weak ties" (acquaintances, not close friends)
- Your next job likely comes from someone you don't know well yet

### Signaling Theory (Spence, 1973)
- Nobel Prize-winning economics research
- Candidates demonstrate quality through costly signals
- Portfolios and demonstrated work correlate with actual ability

### Networking Effectiveness (Wanberg et al., 2020)
- Structured networking interventions improve job outcomes
- Networking self-efficacy predicts reemployment quality
- Even introverts benefit from deliberate networking practice

### Informational Interviewing (Kanar, 2023)
- Learn about their work, don't pitch yourself
- Empirically validated for improving networking outcomes
- Build relationships before jobs are posted

### Persuasion Psychology (Cialdini, 1984)
- Reciprocity: offer value first
- Specificity: reference their actual work
- Easy yes/no: reduce friction in requests

### The Core Insight

**Traditional approach:**
- 100 applications → 2 interviews → maybe 1 offer

**Relationship approach:**
- 10 targeted companies with genuine research
- 5-7 real conversations
- 3+ interviews
- Multiple offers

The difference: You're having conversations before jobs are even posted.

---

## Tips for Success

### DO:
- Be honest about what interests you (fake enthusiasm fails)
- Let Claude do the research legwork
- Take time to read about people before reaching out
- Follow up (most people don't, so you'll stand out)
- Track everything

### DON'T:
- Spam outreach to people whose work you haven't read
- Lead with "I applied for your job" (that's transactional)
- Ask for a job in your first email (ask to learn)
- Let Claude send emails or submit applications for you

---

## Troubleshooting

**"Claude doesn't know my background"**
- Edit `.claude/CLAUDE.md` with your full profile
- Add your resume to `documents/`

**"Job search returns no results"**
- Check your salary filters (might be too restrictive)
- Try broader search terms
- Some job boards rate-limit - wait and retry

**"Email finder can't verify"**
- Set `HUNTER_API_KEY` environment variable
- Some companies block verification - that's normal

**"Claude wants to submit for me"**
- Say "stop" - Claude should never submit
- If it persists, check `.claude/CLAUDE.md` has the rules

---

## Getting Help

- **Issues**: [github.com/rhowardstone/AI-Job-Coach/issues](https://github.com/rhowardstone/AI-Job-Coach/issues)
- **Claude Code help**: `/help` in any Claude Code session

---

*"In the age of AI, those who ask better questions get better answers."*
