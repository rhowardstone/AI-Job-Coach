#!/bin/bash
# AI Career Coach Toolkit - Setup Script

set -e

echo "Setting up AI Career Coach Toolkit..."
echo ""

# Create directories that are gitignored (not in repo)
mkdir -p applications/pending
mkdir -p applications/submitted
mkdir -p documents

# Copy CLAUDE.md template if user doesn't have one
if [ ! -f ".claude/CLAUDE.md" ]; then
    cp CLAUDE.template.md .claude/CLAUDE.md
    echo "✓ Created .claude/CLAUDE.md - EDIT THIS with your profile"
else
    echo "• .claude/CLAUDE.md already exists, skipping"
fi

# Copy profile template if user doesn't have one
if [ ! -f "profile.json" ]; then
    cp toolkit/profile_template.json profile.json
    echo "✓ Created profile.json - EDIT THIS with your details"
else
    echo "• profile.json already exists, skipping"
fi

# Initialize history.json if it doesn't exist
if [ ! -f "applications/history.json" ]; then
    cat > applications/history.json << 'EOF'
{
  "applications": [],
  "stats": {
    "total_applied": 0,
    "pending": 0,
    "rejected": 0,
    "offers": 0
  },
  "last_updated": null
}
EOF
    echo "✓ Created applications/history.json"
else
    echo "• applications/history.json already exists, skipping"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .claude/CLAUDE.md with your profile (name, email, targets, etc.)"
echo "  2. Edit profile.json with your details"
echo "  3. Add your resume to documents/"
echo "  4. Run: claude"
echo ""
