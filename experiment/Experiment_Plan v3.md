I would consider this the **final V3** and the version I would actually use to launch the experiment. It incorporates:

- Clear experiment vision
    
- Defined responsibilities
    
- Technical constraints
    
- Human intervention boundaries
    
- Artifact observation
    
- Evidence collection
    
- Evaluation rubric
    
- Experimental variants (multiple agents)
    
- Maintainability-focused success criteria
    

Most importantly, it reflects your actual intent:

> Determine whether AI can transform human intent into a maintainable software system using appropriate software engineering practices while minimizing the need for humans to create engineering artifacts.

---

# Agentic Development Experiment Plan v3

## Purpose

The purpose of this experiment is to evaluate whether modern AI development agents can transform a human-defined product vision into a high-quality software system while independently applying appropriate software engineering practices.

The experiment is not intended to evaluate AI autonomy alone.

The experiment is intended to determine:

- What information must be supplied by humans
    
- What engineering activities can be performed by AI
    
- Which software engineering artifacts remain necessary
    
- What level of human involvement is required
    
- Whether AI-generated systems remain understandable and maintainable
    

The Driver Development Toolkit serves as the experimental project used to conduct this evaluation.

---

# Experiment Vision

The long-term objective is to understand how software should be developed in an AI-first environment.

The experiment seeks to discover the minimum effective combination of:

- Human intent
    
- Human oversight
    
- AI capability
    
- Software engineering discipline
    

required to consistently produce useful software.

The experiment assumes software engineering best practices continue to provide value but seeks to identify which practices remain necessary, which may be simplified, and which may be automated.

---

# Primary Research Questions

1. Can AI transform a product vision into a complete engineering effort?
    
2. Will AI independently generate appropriate engineering artifacts?
    
3. Which engineering artifacts remain valuable?
    
4. Which engineering activities still require human participation?
    
5. Can AI maintain consistency across generated artifacts?
    
6. Can AI produce software that remains understandable and maintainable?
    
7. What is the minimum effective process required for successful software development?
    

---

# Hypothesis

A capable AI development agent should be able to transform a well-defined vision into a structured software engineering process.

The agent should be capable of generating and maintaining engineering artifacts including:

- Use Cases
    
- Features
    
- Requirements
    
- Architecture
    
- Test Strategy
    
- Implementation Plans
    
- Technical Documentation
    

without requiring the human to manually author those artifacts.

The human should primarily provide:

- Intent
    
- Domain knowledge
    
- Constraints
    
- Tradeoff decisions
    
- Acceptance decisions
    

rather than performing engineering documentation activities.

---

# Experimental Project

## Project Name

Driver Development Toolkit

## Project Purpose

Provide data-driven driving improvement insights using iRacing telemetry data.

The project represents a real problem that the human participant wants solved.

The project is not intended to be a toy application.

---

# Experiment Inputs

## Required Inputs

- Experiment Vision
    
- Experiment Plan
    
- Product Vision
    
- Repository / Workspace
    
- Tooling Information
    
- Available Development Environment
    

## Optional Inputs

- Existing Research
    
- Existing Code
    
- Existing Assets
    
- Public Open Source Projects
    
- Reference Documentation
    

The experiment should minimize human-created engineering artifacts unless required by the experiment protocol.

---

# Technical Constraints

## Technology Selection

Technology choices must be justified.

Existing open-source solutions should be researched before creating custom implementations.

Reusing proven solutions is preferred over unnecessary reinvention.

## Maintainability

The resulting system must be maintainable by the human participant.

The resulting design should support future enhancement.

The resulting artifacts should support future development.

## Traceability

Major design decisions must be documented.

Assumptions must be documented.

Tradeoffs must be documented.

## Quality

Generated software should meet normal professional software engineering expectations.

Working software alone is not sufficient.

---

# Human Responsibilities

The human participant is responsible for:

- Defining vision
    
- Defining goals
    
- Defining constraints
    
- Providing domain expertise
    
- Answering clarification questions
    
- Reviewing outputs
    
- Approving major decisions
    

The human should avoid creating engineering artifacts unless required by the experiment.

---

# Agent Responsibilities

The agent is responsible for:

- Understanding vision
    
- Identifying missing information
    
- Researching relevant solutions
    
- Creating engineering artifacts
    
- Maintaining engineering artifacts
    
- Designing solutions
    
- Implementing solutions
    
- Creating tests
    
- Creating documentation
    

The agent should determine which artifacts are necessary.

---

# Agent Operating Rules

## Ask When Material Uncertainty Exists

Agents should request clarification when uncertainty materially impacts implementation.

## Do Not Invent Critical Requirements

Major assumptions must be surfaced for review.

## Document Assumptions

Important assumptions should be captured and maintained.

## Explain Significant Decisions

Architecture decisions and major tradeoffs should be documented.

## Prefer Existing Solutions

Research should occur before custom implementation.

## Maintain Artifact Consistency

Generated artifacts should remain synchronized throughout development.

---

# Experiment Execution Protocol

## Initial Agent Inputs

At experiment start the agent will receive:

- Product Vision
    
- Experiment Vision
    
- Experiment Plan
    
- Repository Access
    
- Tool Access
    
- Environment Information
    

No additional engineering artifacts shall be provided initially.

---

## Initial Agent Prompt

The agent shall be instructed to:

1. Analyze the provided vision.
    
2. Identify missing information.
    
3. Create any engineering artifacts it believes are necessary.
    
4. Explain its proposed development approach.
    
5. Proceed using its preferred software engineering process.
    

The human will not prescribe a specific process.

---

## Human Intervention Rules

Human intervention is permitted only for:

- Clarification requests
    
- Domain knowledge
    
- Constraint definition
    
- Tradeoff decisions
    
- Acceptance decisions
    

Humans should avoid creating requirements, architecture, or implementation artifacts during Stage 1 and Stage 2.

---

## Escalation Rules

Escalation to later stages occurs only when:

- Progress stalls
    
- Quality degrades
    
- Significant misunderstanding occurs
    
- Maintainability concerns emerge
    

Escalation events must be documented.

---

# Artifact Observation Protocol

The following artifacts shall be tracked.

## Agent Generated Artifacts

Artifacts created independently by the agent.

Examples:

- Use Cases
    
- Features
    
- Requirements
    
- Architecture
    
- Design Documents
    
- Test Plans
    

## Human Introduced Artifacts

Artifacts supplied by the human after experiment start.

## Missing Artifacts

Artifacts later determined necessary but not created by the agent.

---

# Experimental Stages

## Stage 1 – Vision Driven Development

### Inputs

- Product Vision
    
- Experiment Materials
    

### Objective

Determine whether the agent independently creates the engineering structure required for success.

---

## Stage 2 – Clarification Support

Human clarification may be provided.

The agent remains responsible for engineering artifacts.

---

## Stage 3 – Guided Artifact Introduction

Additional artifacts may be introduced if quality degrades.

Examples:

- Use Cases
    
- Features
    
- Requirements
    
- Architecture Guidance
    

All introduced artifacts must be documented.

The purpose of this stage is to determine whether specific engineering artifacts measurably improve outcomes.

---

## Stage 4 – Traditional Engineering Process

Traditional engineering governance and development practices may be introduced.

This establishes the upper bound of process required for success.

---

# Evidence Collection

## Run Log

Record:

- Major milestones
    
- Clarification requests
    
- Significant decisions
    
- Escalations
    

---

## Artifact Inventory

Record:

- Artifacts created
    
- Creation timing
    
- Artifact quality observations
    

---

## Decision Log

Record:

- Architectural decisions
    
- Technology selections
    
- Tradeoffs
    
- Assumptions
    

---

## Human Observation Log

Record:

- Areas of confusion
    
- Areas requiring intervention
    
- Unexpected strengths
    
- Unexpected weaknesses
    

---

# Evaluation Criteria

## Product Quality

Evaluate:

- Functional correctness
    
- Stability
    
- Usability
    
- Alignment with vision
    

Score: 1–5

---

## Engineering Quality

Evaluate:

- Requirements quality
    
- Architecture quality
    
- Test coverage
    
- Documentation quality
    
- Traceability
    

Score: 1–5

---

## Maintainability

Evaluate:

- Ease of understanding
    
- Ease of modification
    
- Design clarity
    
- Documentation effectiveness
    

Score: 1–5

---

## AI Performance

Evaluate:

- Clarification behavior
    
- Assumption management
    
- Artifact generation
    
- Research effectiveness
    
- Consistency
    

Score: 1–5

---

## Human Effort

Evaluate:

- Number of interventions
    
- Depth of interventions
    
- Human-created artifacts required
    

Score: 1–5

Lower human effort is preferred.

---

# Success Criteria

The experiment is successful if it provides evidence regarding:

- What information AI requires
    
- What information humans must provide
    
- Which artifacts AI can create effectively
    
- Which artifacts remain necessary
    
- Which engineering practices provide measurable value
    
- How much human involvement is required
    

Additionally:

- The resulting system must remain understandable.
    
- The resulting system must remain maintainable.
    
- Major decisions must be explainable.
    
- Human reverse engineering should not be required.
    

---

# Failure Criteria

The experiment should be considered unsuccessful if:

- The resulting system cannot be understood.
    
- Significant reverse engineering is required.
    
- Major design decisions cannot be explained.
    
- Maintenance becomes impractical.
    
- The implementation diverges substantially from intent.
    

Working software alone does not constitute success.

---

# Experimental Variants

## Objective

Evaluate whether different AI development agents produce materially different outcomes when given the same vision and operating constraints.

## Candidate Agents

Examples:

- Claude Code
    
- Codex
    
- GitHub Copilot
    
- Antigravity
    
- Future AI development agents
    

## Execution Method

Each agent should receive:

- Product Vision
    
- Experiment Vision
    
- Experiment Plan
    
- Equivalent repository state
    
- Equivalent environment information
    

The human should provide equivalent clarification and oversight whenever practical.

## Comparison Areas

Evaluate:

- Artifact generation
    
- Clarification behavior
    
- Architecture quality
    
- Code quality
    
- Testing quality
    
- Documentation quality
    
- Maintainability
    
- Human effort required
    

## Outcome

The objective is not to identify a universal best agent.

The objective is to determine which agents are most effective for this type of software engineering work and whether different agents require different levels of process support.

---

# Final Experiment Review

At experiment completion perform a structured retrospective.

Questions:

1. What information was truly required?
    
2. Which artifacts emerged naturally?
    
3. Which artifacts had to be introduced?
    
4. Where did AI perform well?
    
5. Where did AI perform poorly?
    
6. What human interventions were necessary?
    
7. What process changes improved outcomes?
    
8. What process elements provided little value?
    
9. Would the resulting system be maintainable in one year?
    
10. What should change before the next experiment?
    

---

# Guiding Principle

The objective is not to prove that AI can replace software engineers.

The objective is to discover how humans and AI can most effectively collaborate to produce useful, understandable, and maintainable software systems.

---

One final observation: compared to where we started a few days ago, the plan has shifted from "can an AI build the Driver Development Toolkit?" to "what is the minimum effective software engineering process in an AI-first world?" That is a much stronger experiment because the toolkit becomes a realistic test vehicle rather than the primary goal. The software you produce will be useful, but the process learning is likely to be the more valuable long-term outcome.