# Job Application Toolkit

Python scripts and Claude Code skills for relationship-focused job searching.

## Philosophy

Online applications have notoriously low success rates. Research indicates 50-80% of positions are filled through networking before being publicly posted.

**Traditional:** Apply → Wait → Nothing

**Relationship-focused:** Research people → Find genuine interest → Build connection → Apply (as formality)

## Research Foundation

- **Granovetter, M. S. (1973)**. The Strength of Weak Ties. *American Journal of Sociology*, 78(6), 1360-1380. DOI: 10.1086/225469
  - 55.6% of jobs obtained through personal contacts, predominantly weak ties

- **Spence, M. (1973)**. Job Market Signaling. *The Quarterly Journal of Economics*, 87(3), 355-374. DOI: 10.2307/1882010
  - Nobel Prize-winning work on demonstrating quality through costly signals

- **Wanberg, C. R. et al. (2020)**. Can job seekers achieve more through networking? *Personnel Psychology*, 73(4), 559-585. DOI: 10.1111/peps.12380
  - Networking interventions improve reemployment quality

- **Kanar, A. (2023)**. Effectiveness of informational interviewing. *The Career Development Quarterly*. DOI: 10.1002/cdq.12318
  - Empirical validation of informational interview effectiveness

- **Cialdini, R. B. (1984)**. *Influence: The Psychology of Persuasion*. William Morrow.
  - Foundational persuasion principles: reciprocity, specificity

## Project Structure

```
AI-Job-Coach/
├── README.md                    # Project overview
├── GETTING_STARTED.md           # User guide
├── .claude/
│   ├── CLAUDE.md                # Your profile (create this)
│   └── skills/                  # Auto-discovered skills
│       ├── apply/SKILL.md       # Relationship-focused workflow
│       ├── job-search/SKILL.md
│       ├── job-batch/SKILL.md
│       ├── ats-review/SKILL.md
│       ├── interview-prep/SKILL.md
│       └── anti-ai-writing/SKILL.md
├── toolkit/
│   ├── scripts/                 # Python tools
│   ├── profile_template.json
│   └── README.md                # This file
├── templates/
│   ├── cover_letter.tex
│   └── history_template.json
├── documents/                   # Your CV (gitignored)
└── applications/                # Tracking (gitignored)
```

## Setup

```bash
# Install dependencies
pip install python-jobspy pandas requests

# Optional: Email verification
export HUNTER_API_KEY="your_key"  # Free tier at hunter.io
```

## Scripts

### job_search.py - Multi-board search

```bash
python toolkit/scripts/job_search.py "software engineer" --location "Seattle" --min-salary 150000
python toolkit/scripts/job_search.py "ML engineer" --remote --hours 48
```

Searches: Indeed, LinkedIn, Glassdoor, Google Jobs, ZipRecruiter

### greenhouse_search.py - Company career pages

```bash
python toolkit/scripts/greenhouse_search.py stripe anthropic databricks --keyword "engineer"
python toolkit/scripts/greenhouse_search.py --list-known
```

Direct queries to company Greenhouse/Lever APIs.

### email_finder.py - Email pattern detection

```bash
python toolkit/scripts/email_finder.py "Jane Smith" company.com
python toolkit/scripts/email_finder.py "John Doe" anthropic.com --verify
```

Generates likely email permutations. `--verify` requires HUNTER_API_KEY.

## Skills (Slash Commands)

| Command | Description |
|---------|-------------|
| `/apply` | Relationship-focused application workflow |
| `/job-search` | Multi-board job search |
| `/job-batch` | Batch application processing |
| `/ats-review` | Resume vs job description scoring |
| `/interview-prep` | Question generation + STAR feedback |
| `/anti-ai-writing` | Human-sounding text guidelines |

## The Workflow

### 1. Find People Whose Work Interests You

**Not:** "Who is hiring?"
**Yes:** "Whose work do I find genuinely interesting?"

Claude researches, presents summaries. You decide: "Could I talk to this person for 20 minutes and we'd both be fascinated?"

### 2. Research Their Work

Before reaching out:
- What specific work caught your attention?
- What's one real question you have?
- What can you offer?

**Test:** Would you email them even with no job openings?

### 3. Craft Outreach

Make it about THEM. Be specific. Easy yes/no.

### 4. Formal Application (Last)

After building connection. This is formality, not strategy.

## User Rules

- **Claude drafts, you send** - Never auto-send emails
- **Claude fills, you submit** - Never auto-submit applications
- **No forced connections** - If interest isn't genuine, move on

## Quick Start

```bash
# 1. Configure profile
cp toolkit/profile_template.json profile.json
# Edit profile.json

# 2. Create .claude/CLAUDE.md with your preferences

# 3. Run Claude Code
claude

# 4. Try:
#    "Search for jobs matching my profile"
#    "Research people at [company]"
```

## License

MIT
