# AI-First Software Development Experiment

# Experiment Findings v3

## Purpose

This document captures lessons learned across experiment execution and evaluation.

Unlike individual run reports, this document focuses on reusable insights regarding AI-assisted and AI-led software development.

Version 3 incorporates findings from:

| Run    | Agent       | Status   |
| ------ | ----------- | -------- |
| Run 01 | Antigravity | Complete |
| Run 02 | Codex       | Complete |
| Run 03 | Claude Code | Complete |

---

# Experiment Status

Three independent implementation agents were evaluated using substantially identical:

* Product Vision
* Experiment Plan
* Execution Guide
* Baseline Branch
* Repository State
* Evaluation Process
* Supervisor Role

The experiment intentionally controlled for project scope and starting conditions in order to observe differences in agent behavior.

All three agents produced:

* Functioning MVP software
* Automated tests
* Engineering artifacts
* Documentation
* Maintainable repository structures

However, the engineering processes differed significantly.

The most important outcome of the experiment is no longer whether AI can generate software.

The more important finding is that different AI agents exhibit materially different software engineering behaviors under otherwise identical conditions.

---

# Cross-Run Summary

## Run 01 — Antigravity

Primary behavior:

> Product-focused implementation engineer

Characteristics:

* Rapid implementation
* Visible progress
* Strong architecture instincts
* Limited traceability
* Weak validation planning
* Implementation-first decision making

---

## Run 02 — Codex

Primary behavior:

> Disciplined systems engineer

Characteristics:

* Strong requirements engineering
* Strong traceability
* Strong artifact maintenance
* Validation-boundary discipline
* Process-oriented execution

---

## Run 03 — Claude Code

Primary behavior:

> Validation-oriented lead engineer

Characteristics:

* Strong assumption management
* Strong self-critique
* Independent verification behavior
* Validation-oriented decision making
* Explicit uncertainty management
* Strong claim discipline

---

# Confirmed Findings

## Finding 1: AI Agents Exhibit A Strong Implementation Bias

### Status

Confirmed

### Observation

All three agents successfully generated functioning software systems.

Implementation activity consistently progressed faster than real-world validation activity.

### Evidence

Run 01 prioritized implementation.

Run 02 prioritized implementation within a stronger engineering process.

Run 03 demonstrated the weakest implementation bias but still produced software substantially faster than validation evidence.

### Implication

Software generation is no longer the primary challenge.

Validation activities must be explicitly planned, measured, and evaluated.

---

## Finding 2: Maintainability Is Achievable

### Status

Confirmed

### Observation

The concern that AI-generated software would be inherently unmaintainable was not supported.

### Evidence

All three runs produced:

* Modular architectures
* Repository organization
* Documentation
* Automated tests
* Clear module boundaries

### Implication

Maintainability appears achievable when appropriate project structure and expectations are provided.

---

## Finding 3: Real-World Validation Remains The Hardest Problem

### Status

Confirmed

### Observation

All three runs successfully demonstrated technical capability.

None demonstrated domain effectiveness.

### Evidence

All runs relied primarily on synthetic telemetry.

None established:

* Coaching correctness
* Driver performance improvement
* Real-world ranking accuracy
* Real telemetry effectiveness

### Implication

The primary challenge is no longer generating software.

The primary challenge is establishing confidence that generated software solves the intended real-world problem.

---

## Finding 4: Human Domain Expertise Remains Necessary

### Status

Confirmed

### Observation

No run independently validated coaching effectiveness.

### Evidence

Domain validation still requires:

* Representative telemetry
* Domain expertise
* Real-world evaluation
* Human judgment

### Implication

AI development agents can generate systems, but domain experts remain necessary to validate outcomes.

---

## Finding 5: Engineering Process Quality Is Agent-Dependent

### Status

Confirmed

### Observation

Engineering-process behavior varied significantly despite controlled experiment conditions.

### Evidence

Run 01 demonstrated weaker requirements engineering and traceability.

Run 02 demonstrated strong systems-engineering discipline.

Run 03 demonstrated strong validation-oriented engineering discipline.

### Implication

Engineering-process quality should not be treated as a universal AI capability.

Agent selection matters.

---

## Finding 6: Documentation Quality Is Uneven

### Status

Confirmed

### Observation

Documentation quality varies by both artifact type and agent.

### Evidence

Run 01 excelled at handoff documentation.

Run 02 excelled at traceability and artifact maintenance.

Run 03 excelled at assumptions, risks, limitations, and validation documentation.

### Implication

Documentation should be evaluated by category rather than as a single metric.

---

## Finding 7: Human Supervision Requirements Vary By Agent

### Status

Confirmed

### Observation

The amount and type of supervision required varied significantly between runs.

### Evidence

Run 01 required more process oversight.

Run 02 primarily required governance and milestone review.

Run 03 primarily required evaluation and evidence review.

No run required implementation assistance.

### Implication

Future evaluations should distinguish between:

* Implementation assistance
* Process supervision
* Governance oversight
* Evaluation activities

---

## Finding 8: Validation-Boundary Discipline Is A Critical Engineering Behavior

### Status

Confirmed

### Observation

High-quality agents consistently constrained claims to validated capabilities.

### Evidence

Run 02 repeatedly refused to claim unsupported `.ibt` capabilities.

Run 03 repeatedly distinguished between:

* Implemented
* Demonstrated
* Validated

behavior.

### Implication

Future evaluations should assess not only what agents build, but what they refuse to claim without evidence.

---

## Finding 9: Artifact Maintenance Matters More Than Artifact Creation

### Status

Confirmed

### Observation

Generating engineering artifacts is less valuable than maintaining them throughout development.

### Evidence

Run 02 and Run 03 continuously updated:

* Requirements
* Architecture
* Decisions
* Assumptions
* Traceability
* Test Strategy

as implementation evolved.

### Implication

Artifact maintenance should be evaluated separately from artifact generation.

---

## Finding 10: Agent Selection Is A Dominant Independent Variable

### Status

Confirmed

### Observation

Agent choice produced materially different engineering behaviors despite controlled inputs.

### Evidence

All three agents received substantially identical:

* Vision
* Constraints
* Baseline
* Evaluation process

yet exhibited significantly different engineering characteristics.

### Implication

Agent selection appears to be one of the most important determinants of engineering-process outcomes in AI-first software development.

---

## Finding 11: Evaluation Criteria Influence Behavior

### Status

Confirmed

### Observation

Agents appear to optimize toward the outputs that are visible, measurable, and evaluated.

### Evidence

Later runs demonstrated stronger engineering-process behavior after process quality became an explicit evaluation concern.

### Implication

Evaluation criteria should be treated as part of the engineering system rather than merely a reporting mechanism.

---

# New Confirmed Findings

## Finding 12: Epistemic Discipline Varies Significantly Between Agents

### Status

Confirmed

### Observation

Agents differ not only in implementation style and engineering-process quality but also in how aggressively they challenge their own assumptions.

### Evidence

Run 01 focused primarily on implementation progress.

Run 02 focused primarily on engineering-process rigor.

Run 03 repeatedly:

* Identified unsupported assumptions
* Challenged its own conclusions
* Sought additional evidence
* Reduced uncertainty before expanding scope
* Constrained claims to available evidence

### Implication

Future evaluations should explicitly measure:

* Assumption management
* Uncertainty management
* Self-verification behavior
* Validation-seeking behavior
* Claim discipline

These behaviors may be stronger predictors of engineering quality than implementation speed.

---

## Finding 13: Self-Verification Can Produce Real Engineering Value

### Status

Confirmed

### Observation

AI agents can discover meaningful defects through targeted verification activities rather than through traditional testing alone.

### Evidence

Run 03 independently identified and corrected a pyirsdk API defect through retrospective analysis and source verification.

The defect was not discovered through:

* Human review
* Runtime failure
* Test failure
* Bug reports

### Implication

Self-verification behavior may be an important independent measure of engineering maturity.

Future evaluations should explicitly observe whether agents revisit assumptions and verify earlier decisions.

---

## Finding 14: Engineering Success And Product Success Are Distinct Outcomes

### Status

Confirmed

### Observation

All three runs achieved substantially stronger engineering outcomes than product-validation outcomes.

### Evidence

All three runs produced maintainable, functional systems.

None demonstrated validated coaching effectiveness.

### Implication

Future evaluations should continue separating:

* Implementation capability
* Engineering-process capability
* Validation capability
* Product effectiveness

These dimensions are not interchangeable.

---

# Emerging Findings

The following findings are strongly suggested but require additional replication.

---

## Emerging Finding A: Validation-Oriented Engineering May Be A Distinct Agent Capability

### Observation

Run 03 demonstrated behavior not clearly observed in previous runs.

### Evidence

Claude repeatedly prioritized:

* Validation
* Risk reduction
* Evidence gathering
* Assumption review

over additional implementation.

### Open Question

Is this a unique Claude characteristic or would similar behavior appear in future runs using the same agent?

---

## Emerging Finding B: Epistemic Discipline May Predict Long-Term Engineering Quality

### Observation

The strongest engineering behavior observed in Run 03 was not implementation.

It was recognition of uncertainty.

### Evidence

The run repeatedly identified:

* What was known
* What was unknown
* What remained unvalidated

and adjusted behavior accordingly.

### Open Question

Does stronger epistemic discipline correlate with better long-term project outcomes?

---

# Open Questions

The following questions remain unresolved.

---

## Question 1

Would repeated runs using the same agent produce similar engineering-process outcomes?

---

## Question 2

How much of observed behavior is attributable to:

* Agent architecture
* Agent training
* Tooling environment

rather than the experiment framework itself?

---

## Question 3

Can AI agents independently create meaningful domain-validation plans?

---

## Question 4

Can AI agents successfully transition from synthetic validation to real telemetry validation?

---

## Question 5

Can self-verification behavior be intentionally encouraged through process design?

---

## Question 6

Does stronger epistemic discipline lead to better long-term product outcomes?

---

# Recommended Experiment Updates

## Process Updates

Continue requiring:

* Use Cases
* Requirements
* Architecture
* Assumptions
* Traceability
* Test Strategy
* Validation Planning

before implementation begins.

---

## Evaluation Updates

Evaluate separately:

* Requirements Quality
* Architecture Quality
* Traceability Quality
* Validation Strategy
* Assumption Management
* Artifact Maintenance
* Validation-Boundary Discipline
* Self-Verification Behavior
* Epistemic Discipline

---

## Future Experiment Design

Future experiments should attempt to isolate:

* Agent effects
* Tool effects
* Prompt effects
* Process effects
* Evaluation effects

to better understand which variables most strongly influence outcomes.

---

# Current Conclusion

After three completed runs, the evidence suggests that modern AI agents are capable of producing maintainable software systems with limited human intervention.

The experiment no longer indicates that software generation itself is the primary challenge.

Instead, the critical challenges appear to be:

* Validation
* Domain confidence
* Assumption management
* Engineering-process quality
* Real-world evidence
* Product effectiveness

The most significant finding from Version 3 is that AI agents do not merely differ in implementation quality.

They differ in engineering behavior.

Some behave primarily as implementation engineers.

Some behave primarily as systems engineers.

Some behave primarily as validation-oriented engineers.

Agent selection appears to be a first-class engineering decision in AI-first software development and may be one of the strongest determinants of engineering-process outcomes.
