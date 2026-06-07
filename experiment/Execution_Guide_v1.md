## Purpose

This guide operationalizes the Agentic Development Experiment Plan v3.

The purpose of this document is not to redefine the experiment. Its purpose is to define how to execute the experiment consistently, capture useful evidence, and keep each agent run isolated from previous runs.

---

# 1. Execution Summary

## First Agent Run

**Initial agent:** Antigravity

## Project

**Project:** Driver Development Toolkit

## Repository

A new GitHub repository will be created for the experiment.

## Default Technology Stack

The default stack for the experiment is:

- Python
- uv
- GitHub
- Git-based workflow
- Windows development environment

The agent may propose deviations, but deviations must be justified before adoption.

## Run Isolation Principle

Each agent run must begin from the same clean base repository state.

Outputs, decisions, code, artifacts, and lessons from one agent run should not be visible to later agents until that agent’s run is complete and ready for evaluation.

---

# 2. Repository Strategy

## Base Repository

Create a new GitHub repository for the experiment.

Suggested repository name:

```text
driver-development-toolkit-experiment
```

The initial repository should contain only the approved experiment input materials and minimal setup files.

## Base Repository Contents

The base repository should include:

```text
/experiment
  Experiment_Plan_v3.md
  Product_Vision.md
  Execution_Guide_v1.md

/runs
  /README.md

/evaluation
  Evaluation_Rubric.md
  Run_Log_Template.md
  Artifact_Inventory_Template.md
  Decision_Log_Template.md
  Human_Observation_Log_Template.md

README.md
.gitignore
```

## Base Repository Rules

The base repository should not include:

- Requirements created by the human
- Architecture created by the human
- Use cases created by the human
- Test plans created by the human
- Implementation plans created by the human
- Research summaries created by the human, unless intentionally provided as experiment input

The purpose is to determine whether the agent generates the necessary engineering structure.

---

# 3. Branch and Run Structure

## Recommended Branch Model

Use one immutable base branch and one branch per agent run.

```text
main
base/experiment-start
runs/antigravity-run-01
runs/codex-run-01
runs/claude-code-run-01
runs/copilot-run-01
```

## Base Branch

After the initial repository is prepared, create a clean baseline branch:

```bash
git checkout -b base/experiment-start
git push -u origin base/experiment-start
```

Each agent run should start from this branch.

## Antigravity Run Branch

For the first run:

```bash
git checkout base/experiment-start
git checkout -b runs/antigravity-run-01
git push -u origin runs/antigravity-run-01
```

## Run Isolation Rule

Do not merge prior agent output into the base branch before running another agent.

Each run should be treated as an independent experiment trial.

---

# 4. Local Environment Setup

## Required Local Tools

The Windows environment should have:

- Git
- Python
- uv
- GitHub access
- Antigravity
- A code editor or shell suitable for reviewing repository state

## Suggested Validation Commands

Before starting the run:

```bash
git --version
python --version
uv --version
git status
```

## Python Project Setup

The agent should be allowed to decide the exact project structure.

However, if the agent needs a starting point, the preferred package manager is uv.

Preferred ecosystem:
- Python
- uv

The agent is responsible for selecting and justifying the project structure.

The agent should document any selected project layout and justify significant decisions.

---

# 5. Initial Agent Inputs

At run start, provide the agent only the approved initial materials:

1. Experiment Plan v3
2. Product Vision
3. Execution Guide v1
4. Repository access
5. Tool/environment information
6. Stack preference: Python + uv + GitHub + Windows

Do not provide human-authored requirements, architecture, use cases, or implementation plans at the beginning of Stage 1.
## Experiment Visibility Rules

The agent should initially receive only:

1. Experiment Plan v3
2. Product Vision
3. Execution Guide v1

Evaluation rubrics, run logs, observation logs, and experiment scoring materials should not be provided unless intentionally required by the experiment design.

The objective is to observe the engineering process the agent naturally creates rather than optimize behavior against the evaluation criteria.

---

# 6. Initial Agent Launch Prompt

Use the following prompt to start the AI agent run.

```text
You are the development agent for an agentic software development experiment.

Your task is to transform the provided product vision into a maintainable software system while applying appropriate software engineering practices.

You are being evaluated not only on whether the software works, but also on whether the resulting system is understandable, maintainable, well-tested, and supported by appropriate engineering artifacts.

Important experiment context:

- This is an experiment in AI-first software development.
- The human will provide intent, constraints, domain knowledge, tradeoff decisions, and acceptance decisions.
- The human should not manually create requirements, architecture, use cases, test plans, or implementation plans unless the experiment escalates to a later stage.
- You are responsible for identifying which engineering artifacts are necessary.
- You are responsible for creating and maintaining those artifacts.
- Working software alone is not sufficient.
- The system must be understandable and maintainable by the human after the run.
- Human reverse engineering of the implementation will be considered a failure.

Project context:

- Project name: Driver Development Toolkit
- Purpose: Provide data-driven driving improvement insights using iRacing telemetry data.
- Preferred technology stack: Python, uv, GitHub, Windows.
- You may propose a different technology choice only if you explain and justify the deviation before using it.
- Existing open-source solutions should be researched before creating custom implementations.
- Reuse proven solutions where appropriate.
- Major assumptions, decisions, and tradeoffs must be documented.

Your initial tasks:

1. Review the provided Experiment Plan, Product Vision, and Execution Guide.
2. Identify any missing information that materially affects implementation.
3. Ask clarification questions only where the uncertainty is important.
4. Create any engineering artifacts you believe are necessary.
5. Explain your proposed development approach.
6. Propose an initial implementation plan.
7. Begin execution after the initial approach is clear.

Operating rules:

- Do not invent critical requirements.
- Surface important assumptions for review.
- Document major decisions.
- Maintain consistency across artifacts.
- Prefer simple, maintainable solutions over unnecessary complexity.
- Use Git commits to preserve meaningful progress.
- Keep the repository understandable to a future maintainer.

Before writing implementation code, provide:

1. Your understanding of the product vision.
2. Missing information or clarification questions.
3. Proposed artifacts to create.
4. Proposed development approach.
5. Proposed first implementation milestone.
```

---

# 6.5 Human Prompting Policy

## Objective

Human prompting should remain consistent across agent runs.

The purpose of the experiment is to evaluate the agent's ability to create and execute a software engineering process, not the human's ability to steer the agent.

## Preferred Human Response Pattern

When responding to agent questions:

Decision: [answer]

Reasoning: [brief explanation]

Constraint: [optional]

Avoid providing implementation details unless specifically requested.

## Allowed Prompt Types

The human may provide:

- Clarification of intent
- Domain knowledge
- Business context
- Constraints
- Tradeoff decisions
- Acceptance decisions
- Answers to direct questions

## Discouraged Prompt Types

The human should avoid:

- Designing the architecture
- Writing requirements
- Writing use cases
- Writing implementation plans
- Suggesting code structure
- Suggesting specific libraries unless requested
- Solving technical problems for the agent

## Escalation Prompting

If the experiment enters Stage 3 or Stage 4, the human may provide additional engineering guidance.

All such interventions should be recorded in the Escalation Log.

## Consistency Rule

When possible, use equivalent prompting behavior across all agent runs.

Differences in prompting should be documented in the Run Log.

---
# Standard Prompts

These are prompts you can use repeatedly during the run.

### Agent Seems Lost

```text
Please explain:

1. Current objective
2. Current assumptions
3. Current blockers
4. Available options
5. Recommended path forward
```

### Agent Made Significant Design Decision

```text
Please document:

1. Decision
2. Alternatives considered
3. Rationale
4. Risks
5. Impact on future development
```

### Agent Starts Coding Too Early

```text
Before continuing implementation, please explain:

1. Current understanding of requirements
2. Engineering artifacts created
3. Remaining uncertainties
4. Why implementation is appropriate at this stage
```

### Artifact Quality Review

```text
Please perform a self-review of the generated artifacts.

Evaluate:

- Completeness
- Consistency
- Traceability
- Maintainability

Identify weaknesses and proposed improvements.
```

### End-of-Run Review

```text
Please prepare a final handoff package.

Include:

1. System overview
2. Architecture summary
3. Requirements summary
4. Repository guide
5. Test strategy
6. Known limitations
7. Future improvements
```

---

One thing I would **not** do is define a giant supervisor prompt for this experiment.

The more elaborate the supervisor prompt becomes, the more you risk testing _your process_ instead of testing the agent.

For this experiment, I would keep the launch prompt relatively stable and use the Human Prompting Policy as the governance mechanism. That gives you much cleaner comparisons between Antigravity, Claude Code, Codex, Copilot, or any future agent.

---
# 7. Human Operating Rules During Run

## Allowed Human Input

The human may provide:

- Product intent
- Domain knowledge
- Constraint clarification
- Tradeoff decisions
- Acceptance decisions
- Answers to agent questions

## Discouraged Human Input

During Stage 1 and Stage 2, the human should avoid providing:

- Human-written requirements
- Human-written use cases
- Human-written architecture
- Human-written implementation plans
- Human-written test plans
- Detailed solution design

## Human Response Pattern

When the agent asks a question, answer directly and briefly.

Preferred format:

```text
Decision: [answer]

Reasoning: [short explanation if needed]

Constraint: [any constraint the agent must follow]
```

---

# 8. Evidence Collection

Evidence should be collected during the run, not reconstructed afterward.

## Run Log

File:

```text
/runs/antigravity-run-01/Run_Log.md
```

Capture:

- Date/time
- Milestone
- Agent action
- Human action
- Outcome
- Notes

Template:

```markdown
# Run Log – Antigravity Run 01

| Time | Event | Agent Action | Human Action | Outcome | Notes |
|---|---|---|---|---|---|
| | Run started | | | | |
```

---

## Artifact Inventory

File:

```text
/runs/antigravity-run-01/Artifact_Inventory.md
```

Capture:

- Artifact name
- Artifact type
- Created by
- Creation timing
- Purpose
- Quality notes
- Whether it was agent-generated or human-introduced

Template:

```markdown
# Artifact Inventory – Antigravity Run 01

| Artifact | Type | Created By | Stage | Purpose | Quality Notes | Agent Generated? |
|---|---|---|---|---|---|---|
| | | | | | | |
```

---

## Decision Log

File:

```text
/runs/antigravity-run-01/Decision_Log.md
```

Capture:

- Architecture decisions
- Technology choices
- Assumptions
- Tradeoffs
- Accepted risks

Template:

```markdown
# Decision Log – Antigravity Run 01

| Decision | Context | Options Considered | Selected Option | Rationale | Risk / Tradeoff |
|---|---|---|---|---|---|
| | | | | | |
```

---

## Human Observation Log

File:

```text
/runs/antigravity-run-01/Human_Observation_Log.md
```

Capture:

- Confusion
- Trust concerns
- Maintainability concerns
- Unexpected strengths
- Unexpected weaknesses
- Places where the human wanted to intervene but did not

Template:

```markdown
# Human Observation Log – Antigravity Run 01

| Time | Observation | Category | Severity | Notes |
|---|---|---|---|---|
| | | | | |
```

---

## Escalation Log

File:

```text
/runs/antigravity-run-01/Escalation_Log.md
```

Capture:

- Stage transition
- Trigger
- Evidence
- Human intervention introduced
- Impact

Template:

```markdown
# Escalation Log – Antigravity Run 01

| Time | From Stage | To Stage | Trigger | Evidence | Intervention | Result |
|---|---|---|---|---|---|---|
| | | | | | | |
```

## Prompt and Conversation Transcript

File:

```text
/runs/antigravity-run-01/Prompt_Transcript.md
```
Capture:

- Initial launch prompt
- Significant agent questions
- Human responses
- Major decisions
- Escalation discussions
- Final completion statement

The transcript does not need to be exhaustive but should preserve sufficient context to understand how major decisions were made.

---

## Research Log

File:

```text
/runs/antigravity-run-01/Research_Log.md
```
Capture:

- External libraries considered
- Existing open-source projects reviewed
- Alternative approaches evaluated
- Reasons for adoption or rejection
- Assumptions derived from research

The objective is to evaluate whether the agent effectively leverages existing solutions rather than unnecessarily creating custom implementations.

---

# 9. Stage Transition Rules

## Stage 1 – Vision Driven Development

The run starts in Stage 1.

The agent receives the vision and experiment materials, then independently determines the engineering process.

Remain in Stage 1 as long as the agent is making reasonable progress and quality is acceptable.

## Stage 2 – Clarification Support

Move to Stage 2 when the agent needs domain clarification or constraint clarification.

Stage 2 is still considered healthy and expected.

## Stage 3 – Guided Artifact Introduction

Move to Stage 3 only if the absence of engineering structure begins to materially affect implementation quality, maintainability, trust, or project direction.

Minor artifact weaknesses alone are not sufficient justification for escalation.

Examples:

- No requirements are created and implementation becomes unclear
- Architecture is missing or inconsistent
- Tests are absent or superficial
- Major assumptions are hidden
- The human cannot understand the system direction

In Stage 3, the human may introduce specific engineering artifact expectations.

## Stage 4 – Traditional Engineering Process

Move to Stage 4 only if the run cannot proceed effectively without traditional human-guided engineering process.

Stage 4 represents a process fallback.

---

# 9.5 Run Completion Criteria

A run should end when one of the following conditions is met:

1. The agent declares the MVP complete.
2. The agent declares that implementation is complete according to its own generated requirements.
3. The human determines that progress has stalled.
4. The run exceeds predefined experiment limits.
5. The run reaches an agreed evaluation checkpoint.

Suggested initial limits:

- Maximum elapsed duration: 10 working hours
- Maximum active sessions: 10
- Maximum unresolved blocker duration: 2 sessions

The reason for run termination should be recorded in the Run Log.

---
# 10. Commit Guidance

The agent should commit meaningful increments.

Suggested commit categories:

```text
docs: add initial engineering artifacts
docs: capture architecture decisions
feat: add telemetry parsing foundation
test: add telemetry parser tests
docs: update requirements and traceability
refactor: simplify analysis pipeline
```

The human should avoid editing agent-created artifacts unless the experiment has escalated.

---

# 10.5 Experiment Success Criteria

The primary experiment question is:

Can an AI agent transform a product vision into a maintainable software engineering effort with minimal human-generated engineering artifacts?

A run should be considered successful if:

- The resulting system functions according to generated requirements.
- Engineering artifacts support understanding and maintenance.
- The human can understand system structure without reverse engineering implementation details.
- A reasonable path exists for future maintenance.
- Human intervention remained primarily within Stage 1 or Stage 2.

Working software alone is insufficient for full success.

---
# 11. Evaluation Workflow

At the end of the run, evaluate the run using the V3 criteria.

## Product Quality

Score 1–5:

- Functional correctness
- Stability
- Usability
- Alignment with vision

## Engineering Quality

Score 1–5:

- Requirements quality
- Architecture quality
- Test coverage
- Documentation quality
- Traceability

## Maintainability

Score 1–5:

- Ease of understanding
- Ease of modification
- Design clarity
- Documentation effectiveness

## Reproducibility

Score 1–5:

- Installation documented
- Environment documented
- Tests executable
- Application executable
- New developer onboarding possible

A score of 5 indicates that a reasonably skilled developer can reproduce the system without experiment-specific knowledge.
## AI Performance

Score 1–5:

- Clarification behavior
- Assumption management
- Artifact generation
- Research effectiveness
- Consistency

## Human Effort

Score 1–5:

- Number of interventions
- Depth of interventions
- Human-created artifacts required

For Human Effort, lower actual effort is better, but use the score to represent experiment success:

```text
5 = minimal human effort
1 = heavy human engineering effort required
```

## Reproducibility

Score 1–5:

- Installation process documented
- Environment setup documented
- Tests executable
- Application executable
- New developer onboarding possible

A score of 5 should indicate that a reasonably skilled developer can reproduce the system without requiring knowledge from the experiment participants.

---

# 11.5 Maintainer Handoff

Before a run can be considered complete, the agent should provide a maintainer-oriented handoff document.

Suggested file:

```text
docs/Maintainer_Handoff.md
```
The handoff should include:

- System overview
- Architecture summary
- Key design decisions
- Repository structure
- Setup instructions
- Test execution instructions
- Known limitations
- Future improvement opportunities

The handoff should allow a future developer to understand and extend the system without reverse engineering the implementation.

---
# 12. Post-Run Review Questions

After the run, answer:

1. What information was truly required?
2. Which artifacts emerged naturally?
3. Which artifacts had to be introduced?
4. Where did the agent perform well?
5. Where did the agent perform poorly?
6. What human interventions were necessary?
7. What process changes improved outcomes?
8. What process elements provided little value?
9. Would the resulting system be maintainable in one year?
10. What should change before the next run?

---

# 13. Agent Comparison Notes

Do not compare agents until each candidate agent has completed an isolated run.

For each agent, preserve:

```text
/runs/[agent-name]-run-01
```

Each run should include:

- Run log
- Artifact inventory
- Decision log
- Human observation log
- Escalation log
- Final evaluation
- Final repository state or branch reference

---

# 14. Ready-to-Run Checklist

Before starting Antigravity:

- [ ] Create new GitHub repository
- [ ] Add Experiment Plan v3
- [ ] Add Product Vision
- [ ] Add Execution Guide v1
- [ ] Add evaluation templates
- [ ] Create `base/experiment-start` branch
- [ ] Create `runs/antigravity-run-01` branch
- [ ] Confirm Windows environment
- [ ] Confirm Python installed
- [ ] Confirm uv installed
- [ ] Confirm Git working
- [ ] Confirm Antigravity has repository access
- [ ] Start run using launch prompt
- [ ] Begin Run Log immediately

---

# 15. Key Discipline Reminder

The experiment is not testing whether the human can steer an AI into producing good software.

The experiment is testing whether the agent can transform intent into a maintainable software engineering effort with minimal human artifact creation.

The human should resist the urge to prematurely rescue the agent.

Observe first. Intervene only when the experiment rules justify intervention.

The human should avoid judging the agent solely on software output.

The primary experiment objective is to evaluate whether the agent can establish and maintain an understandable software engineering process that produces maintainable software.

Working software without maintainable engineering structure should be considered a partial success rather than a full success.
