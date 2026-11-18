# Contributing to Antigravity Codex Orchestrator

Thank you for your interest in contributing to **Antigravity Codex Orchestrator**!

## How to Contribute
1. **Playbook Refinements**: Improve prompt templates in `templates/` or add specialized check items in `playbooks/`.
2. **Schema Enhancements**: Extend `schemas/ledger_schema.json` to capture additional metrics (e.g. AST diffs, test coverage).
3. **Dashboard Improvements**: Enhance `dashboard/harness_dashboard.html` with new visualization controls.

## Development Guidelines
- Maintain zero-intrusion on Antigravity core mechanisms.
- Keep commands safe for Windows, macOS, and Linux (e.g. handle stdin deadlocks properly).
- Verify all JSON schemas conform to draft-07 standard.
