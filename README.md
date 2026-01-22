# AI Career Coach Toolkit

Claude Code skills for relationship-focused job searching, implementing methodology grounded in career development research.

## The Problem

Online job applications have notoriously low success rates. Research suggests 50-80% of positions are filled through networking and referrals before being publicly posted, with employee referrals accounting for 30-50% of hires despite comprising only 7% of applicants (Wanberg et al., 2020).

## A Different Approach

Most AI job tools automate the traditional approach: generate more cover letters, apply to more positions, faster. This toolkit does the opposite—fewer applications, more relationships. The AI handles research and drafting; you decide whether you could genuinely talk to someone about their work for 20 minutes before reaching out.

## Practical Framework

1. **Research people** whose work genuinely interests you
2. **Build relationships** through informational conversations
3. **Demonstrate value** through signals (portfolio, proposals, demonstrated understanding)
4. **Apply formally** as backup/formality

## Quick Start

```bash
git clone https://github.com/rhowardstone/AI-Job-Coach.git
cd AI-Job-Coach
pip install python-jobspy pandas requests
./install.sh
# Edit .claude/CLAUDE.md with your profile
claude
```

The install script creates the directory structure and copies templates. Edit `.claude/CLAUDE.md` with your name, email, target companies, and preferences before running `claude`.

**Browser automation** (optional): For form-filling, run `/plugin` inside Claude Code and install Playwright.

See [GETTING_STARTED.md](GETTING_STARTED.md) for complete setup guide.

## Features

### Scripts
```bash
python toolkit/scripts/job_search.py "software engineer" --location "Seattle" --min-salary 150000
python toolkit/scripts/greenhouse_search.py stripe anthropic --keyword "engineer"
python toolkit/scripts/email_finder.py "Jane Smith" company.com --verify
```

### Skills

| Command | Description |
|---------|-------------|
| `/apply` | Relationship-focused application workflow |
| `/job-search` | Multi-board job search |
| `/job-batch` | Batch processing |
| `/ats-review` | Resume vs job description analysis |
| `/interview-prep` | Question generation + STAR feedback |
| `/anti-ai-writing` | Human-sounding text guidelines |

## Core Principle

**Claude fills, you submit.**

- Claude drafts → You send
- Claude researches → You validate interest
- Claude fills forms → You click submit

## Research Foundation

### Weak Tie Theory

Granovetter's foundational research found that 55.6% of job-finders learned about their position through personal contacts—predominantly "weak ties" (acquaintances) rather than close friends.

> Granovetter, M. S. (1973). The Strength of Weak Ties. *American Journal of Sociology*, 78(6), 1360-1380. [DOI: 10.1086/225469](https://doi.org/10.1086/225469)

### Signaling Theory

Spence's Nobel Prize-winning work established that candidates can demonstrate quality through costly signals—credentials, portfolios, and demonstrated work that correlate with actual ability.

> Spence, M. (1973). Job Market Signaling. *The Quarterly Journal of Economics*, 87(3), 355-374. [DOI: 10.2307/1882010](https://doi.org/10.2307/1882010)

### Networking Interventions

Recent research validates that structured networking interventions improve both networking self-efficacy and reemployment quality.

> Wanberg, C. R., van Hooft, E. A. J., Liu, S., & Csillag, B. (2020). Can job seekers achieve more through networking? *Personnel Psychology*, 73(4), 559-585. [DOI: 10.1111/peps.12380](https://doi.org/10.1111/peps.12380)

### Informational Interviewing

The informational interview—conversations to learn about someone's work rather than to pitch yourself—has empirical support for improving networking outcomes.

> Kanar, A. (2023). Effectiveness of informational interviewing for facilitating networking self-efficacy. *The Career Development Quarterly*. [DOI: 10.1002/cdq.12318](https://doi.org/10.1002/cdq.12318)

### Persuasion Psychology

Effective outreach follows established principles: reciprocity (offer value first), specificity, and making requests easy to accept or decline.

> Cialdini, R. B. (1984). *Influence: The Psychology of Persuasion*. William Morrow. [Internet-Archive](https://ia800203.us.archive.org/33/items/ThePsychologyOfPersuasion/The%20Psychology%20of%20Persuasion.pdf)

## License

MIT



