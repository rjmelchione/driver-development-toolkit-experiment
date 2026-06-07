# AI-First Software Development Experiment

# Experiment Findings v2

## Purpose

This document captures lessons learned across experiment execution and evaluation.

Unlike individual run reports, this document focuses on reusable insights about AI-assisted and AI-led software development.

Version 2 incorporates findings from both Run 01 (Antigravity) and Run 02 (Codex).

---

# Experiment Status

| Run    | Agent       | Status   |
| ------ | ----------- | -------- |
| Run 01 | Antigravity | Complete |
| Run 02 | Codex       | Complete |

---

# Cross-Run Summary

Two independent implementation agents were evaluated using substantially the same:

* Product Vision
* Experiment Plan
* Execution Guide
* Baseline Branch
* Evaluation Process
* Supervisor Role

Both agents produced:

* Functioning MVP software
* Automated tests
* Documentation
* Maintainable repository structures

However, the engineering processes differed significantly.

Run 01 behaved primarily as a highly capable implementation engineer.

Run 02 behaved more like a disciplined systems engineer operating within a structured engineering process.

This difference became one of the most significant findings of the experiment.

---

# Confirmed Findings

## Finding 1: AI Agents Naturally Optimize Toward Implementation

### Status

Confirmed

### Observation

Both agents demonstrated a strong bias toward building working software.

Implementation activity consistently progressed faster than validation activity.

### Evidence

Run 01 rapidly transitioned from planning to implementation.

Run 02 demonstrated stronger engineering rigor but still focused primarily on producing an MVP rather than establishing real-world confidence in coaching effectiveness.

### Implication

Validation activities must be explicitly planned, measured, and evaluated.

---

## Finding 2: Maintainability Is Achievable

### Status

Confirmed

### Observation

The concern that AI-generated systems would be inherently unmaintainable was not supported.

### Evidence

Both runs produced:

* Layered architectures
* Repository organization
* Automated tests
* Documentation
* Clear module boundaries

### Implication

Maintainability appears achievable when agents are provided appropriate project structure and expectations.

---

## Finding 3: Real-World Validation Remains the Hardest Problem

### Status

Confirmed

### Observation

Both runs successfully demonstrated technical capability.

Neither run successfully demonstrated domain effectiveness.

### Evidence

Both implementations relied on synthetic telemetry.

Neither run established that:

* Coaching recommendations are correct.
* Drivers improve performance.
* Time-loss calculations accurately represent real telemetry behavior.

### Implication

The primary challenge is not software generation.

The primary challenge is establishing confidence that the generated software solves the intended real-world problem.

---

## Finding 4: Human Domain Expertise Remains Important

### Status

Confirmed

### Observation

Neither run could independently validate coaching effectiveness.

### Evidence

Domain validation still requires:

* Representative telemetry
* Driving expertise
* Real-world evaluation

### Implication

AI development agents can generate systems, but domain experts remain necessary to validate outcomes.

---

# Refined Findings

## Finding 5: Engineering Artifact Generation Is Agent-Dependent

### Previous Conclusion (Run 01)

AI agents do not naturally generate complete engineering artifacts.

### Updated Conclusion

Engineering artifact behavior varies significantly between agents.

### Evidence

Run 01 generated a limited engineering process and weaker traceability.

Run 02 generated and maintained:

* Requirements
* Use Cases
* Architecture
* Assumptions
* Traceability
* Analysis Rules
* Test Strategy
* Closeout Documentation

### Implication

Artifact generation should not be treated as a universal AI capability or limitation.

Agent selection appears to matter significantly.

---

## Finding 6: Documentation Quality Is Uneven

### Status

Refined

### Observation

Documentation quality varies both by artifact type and by agent.

### Evidence

Run 01 produced strong handoff documentation but weaker traceability and decision capture.

Run 02 produced stronger traceability, assumptions management, process documentation, and artifact maintenance.

### Implication

Documentation should be evaluated by category rather than as a single metric.

---

## Finding 7: Human Supervision Requirements Vary By Agent

### Previous Conclusion (Run 01)

Human intervention requirements were lower than expected.

### Updated Conclusion

The amount and type of supervision required varies significantly between agents.

### Evidence

Run 01 required more attention around process quality.

Run 02 primarily required governance, milestone review, and evidence evaluation.

Neither run required implementation assistance.

### Implication

Future evaluations should distinguish between:

* Implementation assistance
* Process supervision
* Governance oversight
* Evaluation activities

---

# New Findings

## Finding 8: Validation-Boundary Discipline Is A Critical Engineering Behavior

### Observation

Run 02 repeatedly refused to claim capabilities that had not been validated.

### Evidence

The implementation preserved and documented a hard boundary around real `.ibt` support.

The system explicitly communicated:

* What was validated
* What was not validated
* Why validation was missing

### Implication

Future evaluations should assess not only what an agent builds, but also what it refuses to claim without evidence.

---

## Finding 9: Artifact Maintenance Matters More Than Artifact Creation

### Observation

Generating engineering artifacts is not sufficient.

Maintaining them throughout implementation is more valuable.

### Evidence

Run 02 continuously updated:

* Requirements
* Architecture
* Traceability
* Assumptions
* Test Strategy

as implementation evolved.

### Implication

Artifact maintenance should be evaluated separately from artifact generation.

---

## Finding 10: Agent Selection Is A Major Independent Variable

### Observation

Different agents exhibited materially different software engineering behaviors despite operating under substantially the same experiment framework.

### Evidence

Run 01 and Run 02 produced similar MVP outcomes but substantially different engineering processes.

### Implication

Agent selection appears to be one of the most important independent variables in AI-first software development outcomes.

Future experiments should treat agent choice as a primary experimental factor.

---

## Finding 11: Explicit Evaluation Criteria Influence Behavior

### Observation

Agents appear to optimize toward the outputs that are visible, measurable, and evaluated.

### Evidence

Both runs produced the artifacts emphasized by the experiment.

Run 02 demonstrated stronger adherence to process-oriented artifacts and evidence generation.

### Implication

Evaluation criteria should be treated as part of the engineering system rather than merely a reporting mechanism.

---

# Open Questions

These questions remain unresolved.

## Question 1

Are the observed differences primarily caused by agent behavior or by normal run-to-run variation?

## Question 2

Would repeating Run 02 with the same agent produce similar process quality?

## Question 3

Can AI agents independently create meaningful real-world validation plans?

## Question 4

Can AI agents successfully transition from synthetic validation to real telemetry validation?

## Question 5

How much domain expertise can be embedded into the engineering process versus requiring human review?

---

# Recommended Experiment Updates

## Process Updates

Continue requiring:

* Use Cases
* Requirements
* Architecture
* Test Strategy
* Traceability
* Assumptions
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

---

## Future Experiment Design

Future runs should attempt to isolate:

* Agent effects
* Prompt effects
* Process effects
* Evaluation effects

to better understand which factors most strongly influence outcomes.

---

# Current Conclusion

After two completed runs, the evidence suggests that modern AI agents are capable of producing maintainable software systems with limited human intervention.

The experiment no longer indicates that software generation itself is the primary challenge.

Instead, the critical challenges appear to be:

* Validation
* Requirements rigor
* Traceability
* Assumption management
* Engineering process quality
* Domain confidence

The most significant new finding is that different AI agents can exhibit substantially different software engineering behaviors even when operating under the same project vision, constraints, and evaluation framework.

Agent selection appears to be a major determinant of engineering process outcomes and should be treated as a first-class experimental variable.
