# SDD Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Add a lightweight, Codex-aware Spec Driven Development workflow to the repository.

**Architecture:** Keep the process in versioned Markdown: root `AGENTS.md` gives Codex durable repository instructions, `docs/DEVELOPMENT.md` explains the workflow, and templates under `docs/specs/_templates/` provide repeatable artifacts. The README links to the guide and keeps commands aligned with this repository.

**Tech Stack:** Markdown, Codex `AGENTS.md`, existing Django/Poetry/Pytest/Ruff workflow.

**Spec:** `docs/superpowers/specs/2026-11-19-sdd-workflow-design.md`

## Global Constraints

- Do not install Spec Kit or another SDD tool or dependency.
- Do not change application behavior, models, endpoints, or runtime configuration.
- Do not create retrospective specs for existing functionality.
- Keep bugs and small local changes on the short documented path.
- Use `docs/specs/<NNN>-<kebab-case-name>/` for feature artifacts.
- Templates live in `docs/specs/_templates/`.

## Review Focus

- New work must not start before the user has reviewed the spec and technical plan; document this gate in both `AGENTS.md` and the guide.
- A bug or local change should not be forced through three documents; include a short-note template/example and an explicit escalation rule for significant scope.
- Requirements, plans, and tasks can drift apart; include acceptance-criteria IDs and a completion/status field that ties them together.
- README commands can point to nonexistent files; use the actual `tests/` directory and configured Poetry commands, and remove Qwen CLI commands.
- README should retain MkDocs + Material, identify GPT via Codex/ChatGPT Plus as development assistance, and avoid implying API credits come with Plus.
- Links/templates can become inconsistent; cross-check all relative links, paths, and command examples before finishing.

---

### Task 1: Codex Instructions and Development Guide

**Files:**
- Create: `AGENTS.md`
- Create: `docs/DEVELOPMENT.md`

**Interfaces:**
- Consumes: Approved flow and requirements from `docs/superpowers/specs/2026-11-19-sdd-workflow-design.md`.
- Produces: Root instructions requiring Codex to read `docs/DEVELOPMENT.md` and the active feature docs before implementation; a guide defining the complete feature workflow, user review gates, proportional bug path, and legacy policy.

- [x] **Step 1: Draft the development guide**

  Include: when to use full SDD vs. short change note; the lifecycle `spec.md` → user review → `plan.md` → user review → `tasks.md` → implementation/verification; how acceptance criteria map to tasks; how to handle scope changes; where feature folders live and the `NNN-kebab-case` naming scheme. The short note must cover current behavior, expected behavior, verification criterion, and affected files, with a rule for when scope requires a full spec.

- [x] **Step 2: Add Codex repository instructions**

  In root `AGENTS.md`, require reading the guide and active spec/plan/tasks before edits; prohibit starting feature implementation until spec and plan are reviewed by the user; require reporting verification and keeping docs synchronized; point out that bugs/small changes use the short path.

- [x] **Step 3: Review guide against approved behavior**

  Manually compare each workflow rule with the spec. Confirm no rule requires backfilling legacy specs or adds an external tool.

---

### Task 2: Reusable SDD Templates

**Files:**
- Create: `docs/specs/_templates/spec-template.md`
- Create: `docs/specs/_templates/plan-template.md`
- Create: `docs/specs/_templates/tasks-template.md`

**Interfaces:**
- Consumes: Folder naming and review flow documented in Task 1.
- Produces: Three templates that make a new feature spec, implementation plan, and acceptance-linked task checklist.

- [x] **Step 1: Create the spec template**

  Include problem/context, user and outcome, goals, in-scope/out-of-scope, functional requirements, numbered observable acceptance criteria, assumptions, and unresolved questions. Include a status/review field.

- [x] **Step 2: Create the plan template**

  Include the source spec link, technical approach, affected components/data/interfaces, error handling, validation strategy, risks, and plan review status. Require each design decision to support one or more acceptance criteria.

- [x] **Step 3: Create the task template**

  Include small checkable tasks, acceptance-criteria references, relevant files, implementation notes, verification commands/results, and completion status. Keep implementation details open where the codebase gives the implementer a clear choice.

- [x] **Step 4: Check template usability**

  Read the templates as a new contributor and confirm each can be copied into `docs/specs/<NNN>-<kebab-case-name>/` without changing its section structure or resolving ambiguous instructions.

---

### Task 3: README SDD Entry Point and Accurate Commands

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: Guide path and workflow terminology from Task 1; templates from Task 2.
- Produces: README overview of SDD with a link to `docs/DEVELOPMENT.md`, and development/test instructions that match the repository.

- [x] **Step 1: Add the SDD overview and link**

  Add a short section explaining that feature work starts with reviewed requirements and a technical plan, then link to `docs/DEVELOPMENT.md` for the full workflow.

- [x] **Step 2: Remove stale assistant instructions and fix test paths**

  Remove the Qwen CLI assistant section and commands. Keep `MkDocs + Material` under Documentation and Pytest + Pytest-Django under Testing. Describe GPT via Codex/ChatGPT Plus as development assistance, not an application API integration. Replace the nonexistent `apps/members/tests/` example with the real `tests/` path; retain valid Poetry/Pytest/Ruff commands from `pyproject.toml`.

- [x] **Step 3: Check README consistency**

  Search the README for remaining Qwen references, invalid test paths, and broken new links. Confirm MkDocs + Material, Pytest + Pytest-Django, and GPT via Codex/ChatGPT Plus appear accurately; correct relevant occurrences.

---

### Task 4: Documentation Review

**Files:**
- Review: `AGENTS.md`
- Review: `docs/DEVELOPMENT.md`
- Review: `docs/specs/_templates/*.md`
- Review: `README.md`

**Interfaces:**
- Consumes: Deliverables from Tasks 1–3.
- Produces: A consistent SDD entry point with no application or dependency changes.

- [x] **Step 1: Check links, paths, and command examples**

  Verify each internal Markdown link resolves, referenced templates and folders exist, and commands correspond to `pyproject.toml` and the checked-in `tests/` directory.

- [x] **Step 2: Check scope and repository diff**

  Run `git diff --check`; inspect the final diff and confirm it changes only process documentation and the README, with no dependency or application changes.

- [x] **Step 3: Report verification**

  Report the files added/updated and the exact documentation checks performed. Since application code is unchanged, do not run the application test suite solely for this documentation change.
