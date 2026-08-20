# Research-to-Feature Spec

## Why
The gap between research insights and actionable feature specifications is a bottleneck for solo developers. A meta-study produces evidence synthesis; a business-use-case review produces commercial assessment — but neither produces a concrete, RICE-scored feature recommendation a developer can pick up and implement. This skill bridges that gap by chaining three existing skills into a single pipeline that terminates in one implementable feature spec.

## What Changes
- New skill `research-to-feature` that orchestrates `self-discover` → `notebooklm-meta-study` → `review-business-use-case` → RICE-scored feature recommendation
- The skill delegates to constituent skills; it does NOT re-implement their workflows
- Output: a single Markdown report containing exactly one RICE-scored feature recommendation with implementation-ready specification
- **BREAKING**: None — new skill, no existing artifacts modified

## Impact
- Affected specs: none (new)
- Affected code: new directory `research-to-feature/` with `SKILL.md`, `scripts/`, `references/`, `assets/`
- Dependencies: `self-discover`, `notebooklm-meta-study`, `review-business-use-case` skills must be installed and operational

## ADDED Requirements

### Requirement: Skill Orchestration Pipeline
The system SHALL execute a four-phase pipeline: (1) capability discovery via `self-discover`, (2) meta-study via `notebooklm-meta-study`, (3) business-use-case review via `review-business-use-case`, (4) RICE-scored feature recommendation synthesis.

#### Scenario: Full pipeline success
- **WHEN** user invokes the skill with a research topic
- **THEN** the agent runs self-discover to confirm required capabilities are available, executes a notebooklm meta-study on the topic, reviews the meta-study output for business use cases, and produces a single RICE-scored feature recommendation report

#### Scenario: Constituent skill unavailable
- **WHEN** `self-discover` reveals a required skill is missing
- **THEN** the agent halts and reports which skill is missing with installation instructions

### Requirement: RICE Scoring Framework
The system SHALL score each candidate feature on four axes: Reach (estimated users affected, 1–5), Impact (user value delivered, 1–5), Confidence (evidence strength, 0.0–1.0), and Effort (person-days, 1–20). The RICE score SHALL be computed as `(Reach × Impact × Confidence) / Effort`.

#### Scenario: Single feature recommendation
- **WHEN** the meta-study and business-use-case review yield multiple candidate features
- **THEN** the agent selects exactly one with the highest RICE score and presents it as the primary recommendation

#### Scenario: Confidence below threshold
- **WHEN** the Confidence score for the top feature is below 0.5
- **THEN** the agent flags the recommendation as `LOW-CONFIDENCE` and includes a "Validation Required" section specifying what evidence would raise confidence

### Requirement: Implementation-Ready Feature Specification
The system SHALL produce a feature specification containing: user story, acceptance criteria, technical approach (≤ 3 paragraphs), affected components, and a first-actionable-task for a developer.

#### Scenario: Developer-ready output
- **WHEN** the report is generated
- **THEN** the feature specification section contains all five required subsections and the first-actionable-task is a single, concrete, executable step

### Requirement: Report Output Contract
The system SHALL write the report to `research-to-feature-reports/<ISO-8601>-<topic-slug>.md` with these mandatory sections: Executive Summary, Meta-Study Digest, Business-Use-Case Digest, RICE-Scored Feature Recommendation, Implementation Specification, Confidence Calibration, Edge Cases & Risks.

#### Scenario: Report written to disk
- **WHEN** the pipeline completes
- **THEN** a report file exists at the specified path with all seven sections present and non-empty