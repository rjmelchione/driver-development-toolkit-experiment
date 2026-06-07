# AI-First Software Development Experiment

# Experiment Findings v1

## Purpose

This document captures lessons learned across experiment execution and evaluation.

Unlike individual run reports, this document focuses on reusable insights about AI-assisted and AI-led software development.

These findings will be updated as additional runs are completed.

---

# Experiment Status

| Run    | Agent       | Status   |
| ------ | ----------- | -------- |
| Run 01 | Antigravity | Complete |

---

# Confirmed Findings

## Finding 1: AI Agents Naturally Optimize Toward Implementation

### Observation

When provided with a product vision and broad engineering goals, the agent rapidly moved toward implementation.

The agent performed some planning activities but consistently prioritized building software over reducing uncertainty.

### Evidence

Run 01 progression:

```text
Vision
→ Implementation Plan
→ Code
→ Tests
→ Documentation
```

The agent did not naturally spend significant effort on:

```text
Use Cases
Feature Analysis
Requirements Development
Acceptance Criteria
Traceability
Validation Planning
```

### Implication

Future experiments should explicitly require engineering deliverables before implementation begins.

---

## Finding 2: Maintainability Is Achievable

### Observation

Contrary to initial concerns, the resulting repository was understandable and maintainable.

### Evidence

The agent produced:

* Layered architecture
* Repository organization
* Unit tests
* Maintainer handoff documentation
* Walkthrough documentation
* Execution logs

A future engineer could likely continue development without reverse-engineering the implementation.

### Implication

The primary risk may not be maintainability of generated code.

The larger risk may be insufficient engineering rigor before implementation.

---

## Finding 3: Documentation Quality Is Uneven

### Observation

The agent generated documentation when requested.

Documentation quality varied significantly by artifact type.

### Strong Artifacts

* Maintainer Handoff
* Implementation Plan
* Walkthrough

### Weak Artifacts

* Decision Log
* Traceability
* Validation Strategy

### Implication

Future experiments should evaluate documentation quality by artifact category rather than treating documentation as a single metric.

---

## Finding 4: Validation Is Weaker Than Implementation

### Observation

The agent was highly effective at building software but less effective at demonstrating that the software solved the intended problem.

### Evidence

The Driver Development Toolkit was validated primarily using synthetic telemetry.

The run demonstrated:

* Technical functionality
* Working architecture
* UI capability

The run did not demonstrate:

* Real telemetry accuracy
* Coaching effectiveness
* Real-world driver improvement

### Implication

Future experiments should explicitly evaluate validation planning and evidence generation.

---

## Finding 5: Human Intervention Requirements Were Lower Than Expected

### Observation

The amount of required human guidance was significantly lower than anticipated.

### Evidence

After experiment startup, the agent completed:

* Research
* Planning
* Architecture
* Implementation
* Testing
* Documentation

without implementation assistance.

### Implication

Current AI agents appear capable of independently executing many software engineering activities once sufficient context is provided.

---

# Experiment Design Findings

## Finding 6: Vision Documents Matter

### Observation

The quality of the vision and experiment documents significantly influenced agent behavior.

### Evidence

Run 01 produced substantially more engineering artifacts than typical "vibe coding" experiences.

This was likely influenced by:

* Product Vision
* Experiment Plan
* Execution Guide

### Implication

Prompt quality alone is insufficient.

Project-level documentation appears to be a major factor in agent performance.

---

## Finding 7: Evaluation Criteria Must Be Explicit

### Observation

The agent optimized for the outputs it believed were important.

### Evidence

The agent produced:

* Code
* Tests
* Documentation
* UI

It did not naturally optimize for:

* Traceability
* Requirements completeness
* Validation rigor

### Implication

If these outcomes are important, they must be explicitly evaluated and scored.

---

## Finding 8: Software Engineering Artifacts Are Not Naturally Produced

### Observation

The agent produced some engineering artifacts but not a complete engineering process.

### Evidence

Missing or weak artifacts included:

* Use Cases
* Feature Catalog
* Acceptance Criteria
* Requirements Traceability
* Validation Plan

### Implication

Future experiments should require these artifacts explicitly.

---

# Unexpected Findings

## Finding 9: The Biggest Weakness Was Not Code Quality

### Observation

Prior to Run 01, the primary concern was that AI-generated code would be difficult to understand and maintain.

This concern was not supported by the experiment results.

### Evidence

The repository was understandable.

The architecture was coherent.

The documentation was sufficient for onboarding.

### Actual Weakness

Requirements engineering, traceability, and validation.

### Implication

Future process improvements should focus more heavily on engineering rigor than implementation quality.

---

## Finding 10: AI Behaved More Like an Implementation Engineer Than an Architect

### Observation

The agent demonstrated strong execution capability but weaker systems engineering capability.

### Characteristics Observed

Strong:

* Coding
* Refactoring
* Testing
* Architecture implementation
* Documentation generation

Weak:

* Requirements engineering
* Validation planning
* Assumption management
* Traceability

### Implication

AI agents may currently function best as highly productive implementation engineers operating within a structured engineering process.

---

# Open Questions

These questions remain unresolved and should be explored in future runs.

## Question 1

Will other agents exhibit the same implementation-first behavior?

---

## Question 2

Can another agent naturally produce stronger requirements engineering artifacts?

---

## Question 3

Can another agent establish meaningful traceability without being explicitly instructed?

---

## Question 4

How much of Run 01 behavior was driven by the experiment documents?

---

## Question 5

Can AI agents perform effective real-world validation planning?

---

# Recommended Experiment Changes

## Process Changes

Require generation of:

* Use Cases
* Feature Catalog
* Requirements Specification
* Acceptance Criteria
* Validation Plan
* Traceability Matrix

before implementation begins.

---

## Evaluation Changes

Add separate scoring for:

* Requirements Quality
* Traceability
* Validation Strategy
* Assumption Management

---

## Artifact Changes

Add templates for:

* Use Cases
* Requirements
* Validation Plan
* Traceability Matrix

---

# Current Conclusion

Run 01 demonstrated that modern AI agents can autonomously create maintainable software systems with relatively little human involvement.

The largest remaining challenge is not software generation.

The largest challenge is ensuring that generated software is supported by a rigorous engineering process that establishes confidence that the correct system is being built.
