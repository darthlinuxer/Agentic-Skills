# Project Brief

## Project
Agentic-Skills

## Purpose
Create and maintain a multi-platform agentic ecosystem for AI-assisted software development workflows across:
- Cursor (`.cursor/`)
- Claude Code (`.claude/`)
- Google Anthropic Agent (`.agent/`)

## Core Goals
1. Provide consistent entry points (commands/workflows) for common development modes.
2. Route all execution through a platform orchestrator.
3. Use domain-specialist agents and reusable skills for implementation quality and consistency.
4. Keep platform structures aligned while respecting platform-specific constraints.
5. Validate repository quality via automated checks.

## Scope
- 17 standardized command/workflow modes (plan, implement, fix, docs, deploy, etc.).
- Orchestrator-driven routing.
- Specialist agent definitions by domain.
- Reusable skill catalog.
- Validation scripts and reports.

## Non-Goals
- Direct user invocation of low-level agents/skills.
- Command-to-skill or skill-to-command cyclic routing.

## Success Criteria
- Entry points are discoverable and consistent across platforms.
- Orchestration and routing are clear and non-overlapping.
- Documentation remains synchronized with implementation.
- Validation script completes successfully and reports issues clearly.

## Source
Initialized from `README.md` and `.clinerules.md` on 2026-02-18.
