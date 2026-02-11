---
description: Workflow for /ui-ux-pro-max - Design Intelligence Workflow.
---

Before answering:
- Apply the most relevant skills and rules for this platform.
- Prefer the single most specific skill/rule when possible.
- If no skill or rule clearly matches, ignore all and answer normally.

# /ui-ux-pro-max - Design Intelligence Workflow

$ARGUMENTS

## Purpose
Generate a design system and UI/UX guidance using the `ui-ux-pro-max` dataset and scripts.

## Prerequisites
Ensure Python is available:
```bash
python3 --version || python --version
```

## Workflow
1. **Analyze requirements**
   - Product type, style keywords, industry, target stack
2. **Generate design system (required)**
```bash
python3 <platform-skills-dir>/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system -p "Project Name"
```
3. **Persist design system (optional)**
```bash
python3 <platform-skills-dir>/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name"
```
4. **Supplement with detailed searches**
```bash
python3 <platform-skills-dir>/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```
5. **Apply stack-specific guidance**
```bash
python3 <platform-skills-dir>/ui-ux-pro-max/scripts/search.py "<keyword>" --stack html-tailwind
```

## Tips
- Use specific keywords (product + industry + style)
- Combine domains for complete coverage
- Always validate accessibility and contrast

## Routing
This workflow delegates to the [orchestrator](../agents/orchestrator.md) agent in **`mode="ui-ux-pro-max"`**. The orchestrator:
- Uses [intelligent-routing](../skills/intelligent-routing/SKILL.md) to select [frontend-specialist](../agents/frontend-specialist.md) and design-focused skills (such as [frontend-design](../skills/frontend-design/SKILL.md), [ui-styling](../skills/ui-styling/SKILL.md), and [ui-ux-pro-max](../skills/ui-ux-pro-max/SKILL.md)) to drive the workflow.
- Coordinates any required script execution through the appropriate agents while keeping the user-facing workflow thin and declarative.

Users should invoke this workflow; the orchestrator decides how design intelligence skills and agents are applied.
