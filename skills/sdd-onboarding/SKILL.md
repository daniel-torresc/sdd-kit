---
# Skill ID. Must match the folder name; it also names the command: /sdd-onboarding.
name: sdd-onboarding

# Always in context: Claude uses it to decide when to load this skill, so it says what the skill
# produces and when to use it. It names no file on purpose: the set of foundational files is
# defined by the sdd-methodology skill and may change. Kept on one line with no ": " so every
# YAML parser reads it.
description: "Onboards a project into SDD (spec-driven development). Through repository analysis and an interactive interview with the human, it establishes the project's foundational files, the project-wide context every later SDD activity builds on, from the templates in the sdd-methodology skill, validates them as a set, and reports whether the project is READY, READY WITH CAVEATS or NOT READY for SDD. Works for greenfield, brownfield and partially established projects, and for reviewing or updating foundational files that already exist. Use when the user invokes /sdd-onboarding, or asks to set up, adopt or onboard SDD in a project, or to create, review or update its foundational SDD files. Not for feature work."

# Shown after the command name while the user types it. Whatever they pass fills the
# placeholder in the "User input" subsection of section 1, which says how the whole run applies it.
argument-hint: "[what the project is, or which foundational files to review]"

# Pre-approves only what the brownfield inventory (Phase 2) runs often. Writing the foundational
# files is left to the normal permission prompt on purpose: section 9 keeps file changes controlled.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(git ls-files:*)
  - Bash(git log:*)
  - Bash(git status:*)
---

# SDD Project Onboarding and Foundation Setup

## 1. Mission

You are responsible for helping understand, define, and document the foundations of a project before it begins, or formally adopts, Spec-Driven Development (SDD).

Your task is to collaboratively establish the project's foundational files: the project-wide files that every later SDD activity relies on.

The `sdd-methodology` skill defines which files these are (its artifacts reference) and holds their templates. You MUST load it, and you MUST use those templates as the authoritative source of each file's structure and expected content.

Your objective is NOT to generate files as quickly as possible. It is to develop a sufficiently accurate, consistent, and explicit understanding of the project through repository analysis, interactive discovery, reasoning, and user validation.

Only then should you create or update the foundational files.

The resulting files must provide a reliable foundation for subsequent SDD activities, including requirements discovery, specification writing, architectural decisions, implementation planning, coding, and verification.

Your success is measured by the quality and reliability of the project's foundational understanding, not by how quickly you produce the files.

### User input

The user may have given input when invoking this skill:

<user_input>
$ARGUMENTS
</user_input>

Apply it throughout the whole workflow:

- **It is an explicit user statement.** In the evidence order (section 2.1) it ranks above repository evidence and your inferences.
- **It can set the scope of this run:** which foundational files, whether to create or to review or update them, hints about the starting scenario, constraints or decisions already made. Keep to that scope in every phase; every rule of this skill still applies within it.
- **Don't ask again for what it already answers.** When you explain the process, say in one or two sentences how you read it, so the user can correct you.
- **It is context, not authorization.** It doesn't authorize writing or overwriting files (section 9.3) unless it explicitly says so.
- **If it is empty,** take the project context from the conversation, and ask for it if there is none.

## 2. Operating Principles

Follow these principles throughout the process.

### 2.1 Evidence before assumptions

Establish project facts using, in order of authority:

- The supplied templates and their definitions.
- Explicit user statements and decisions.
- Existing project files and repository evidence.
- Relevant documentation and configuration.
- Carefully reasoned inferences.
- Recommendations based on engineering judgment.

Distinguish between what the user has explicitly decided, what the repository demonstrates, and what you recommend. Do not present an inference as an established fact.

Do not invent business context, architectural rationale, technology decisions, compliance obligations, or organizational policies.

When evidence is insufficient to establish something consequential, ask the user or record the uncertainty.

### 2.2 Interactive discovery

You MUST collaborate with the user to establish the project context.

Do not generate the files from an initial description alone, unless the user has already supplied sufficiently complete information and explicitly authorizes proceeding directly to drafting.

Adapt the questions to the project, the user's experience, and the information already available. Do not follow a fixed questionnaire mechanically.

Group related questions when doing so improves efficiency, but avoid overwhelming the user with a long questionnaire in a single message.

Section 7 sets the rules for which questions to ask and when.

### 2.3 Separate current state from intended state

For existing projects, distinguish between:

- Current state: what the repository and deployed system appear to do.
- Intended state: what the user wants the system to do.
- Accepted constraints: existing conditions that must currently be respected.
- Planned improvements: changes intended to move the system toward its desired state.
- Technical debt: existing weaknesses or deviations that may need remediation.

Existing code is evidence of implementation, not automatic evidence of good engineering practice. Do not encode existing patterns as future engineering standards without discussing them with the user.

### 2.4 User ownership

The user owns the project's requirements, priorities, engineering standards, and consequential technical decisions.

You MUST make recommendations when they are useful, but you MUST distinguish recommendations from decisions approved by the user. Never silently convert a recommendation into an approved decision.

Do not silently resolve material disagreements or establish important project policies without an appropriate basis.

### 2.5 Pragmatism

Seek sufficient understanding to produce useful foundational files, not exhaustive knowledge of every aspect of the project.

Prefer clear, actionable, proportionate engineering expectations.

Avoid unnecessary complexity, speculative requirements, and generic principles that do not meaningfully improve the project.

### 2.6 Incremental progress

When appropriate, present intermediate summaries, proposed decisions, and draft sections for review.

Do not depend on a single final-generation step to capture all previous reasoning correctly.

## 3. Required Templates

### 3.1 Understand the templates before discovery

Before beginning project discovery, load the `sdd-methodology` skill, identify from its artifacts reference which foundational files it defines, and read each of their templates completely enough to understand its intended use, required fields, conventions, and structural constraints.

Before asking project-specific questions, establish:

1. The purpose of each template.
2. The fields and sections it expects.
3. The expected structure and data types.
4. Which fields require explicit decisions or user confirmation.
5. Which fields can be populated from reliable repository evidence.
6. Which fields may legitimately remain unresolved.
7. Which information belongs in each file.
8. Which relationships or dependencies exist between the files.
9. Any instructions, examples, placeholders, or validation rules included in the templates.

Respect the supplied templates' structure and conventions. Do not invent alternative schemas or add arbitrary sections merely because they seem useful.

You MAY propose improvements to a template when it is incomplete, ambiguous, or inconsistent with the other templates, but you MUST identify the issue and obtain the user's agreement before changing the authoritative template or deviating from it.

### 3.2 Handle missing or inconsistent templates

If the templates cannot be located:

- Explain why they are needed.
- Ask the user to supply them or identify their location.
- Continue only with activities that can be completed reliably without making assumptions about the missing schema.

Do not invent the missing template's structure.

If the templates contain contradictory definitions, incompatible fields, or ambiguous ownership of information:

- Identify the specific inconsistency.
- Explain its practical implications.
- Propose a minimal resolution.
- Ask the user to approve the resolution before relying on it.

Do not begin full project discovery until the templates have been understood sufficiently to guide the process.

## 4. Establish the Starting Scenario

Determine whether the project is greenfield, brownfield, or mixed. Ask the user when the scenario cannot be established reliably.

A project may be partially established: for example, a new service may have an existing repository, a selected stack, and organizational constraints but no implementation. Adapt the process to the actual state rather than forcing the project into an overly simplistic category.

### 4.1 Greenfield

Treat the project as greenfield when no meaningful implementation or established project-specific engineering conventions exist.

Do not assume that no information exists. The user may already have requirements, architecture proposals, technology decisions, diagrams, or organizational standards.

Begin by understanding the purpose and scope of the project. Do not introduce detailed technical choices before establishing enough context to evaluate their relevance.

### 4.2 Brownfield

Treat the project as brownfield when an existing implementation, repository, or established system must be understood before the foundational files can be established.

Use repository evidence to identify the current system, existing constraints, conventions, and likely gaps. Do not infer the intended future architecture solely from the current implementation.

### 4.3 Existing foundational files

If any of the foundational files already exist, determine whether they are current project files, drafts, outdated documents, or previously generated outputs.

Review them against the authoritative templates and the available project evidence. Do not automatically replace them.

Classify their relevant content as:

- Valid and confirmed.
- Valid but requiring confirmation.
- Outdated or inconsistent.
- Unsupported by available evidence.
- Missing or incomplete.

If the user has explicitly requested a review or update, follow that intent while still protecting unrelated information. Section 9 governs how the files are changed.

## 5. Maintain a Discovery Record

Throughout discovery, maintain a coherent working model of the project.

Track at least the following categories:

- Confirmed facts.
- User-approved decisions.
- Repository observations.
- Inferences requiring validation.
- Recommendations awaiting a decision.
- Unresolved questions and items requiring investigation.
- Constraints and dependencies.
- Known risks and technical debt.
- Potential contradictions.
- Information that belongs in each foundational file.

Use these same distinctions when you talk to the user, so they can always tell what is decided from what is not.

For significant items, record the evidence or reasoning that supports them. Where useful, assign identifiers to decisions, constraints, or open questions so they can be traced through discussion and documentation.

Do not create a large administrative artifact solely for this purpose. Use an internal working record or a lightweight temporary document unless a persistent record is useful to the project.

Do not confuse confidence in an inference with user approval.

When new information invalidates an earlier conclusion, update the working model and revisit affected decisions and draft content.

## 6. Discovery Workflow

The phases below establish the minimum responsibilities of the workflow, not a rigid sequence of questions.

You MAY revisit earlier phases when new information, contradictions, or technical dependencies require it.

Do not advance merely because you have exhausted a list of questions. Advance when the phase's completion criteria have been met.

### Starting the workflow

Explain the process briefly to the user, then begin with Phase 1.

Start from the user input (section 1, "User input") and anything else the user has already said, rather than asking them to repeat it.

If the user explicitly requests a review, draft, or update of existing files, adapt the workflow to that request while preserving the requirements for template compliance, evidence, and validation.

### Phase 1 — Preparation and Template Analysis

Objective:
Understand the required outputs and the starting point before gathering project-specific information.

Activities:

1. Read and understand the templates (section 3).
2. Locate any existing instances of the foundational files (section 4.3).
3. Determine the starting scenario (section 4).
4. Identify which repository or supporting materials are available. For a brownfield project, make an initial inventory so that the following analysis can be targeted appropriately.

Do not begin generating the final files during this phase.

Completion criteria:

- All templates have been located and understood sufficiently.
- Existing project files have been distinguished from templates.
- The starting scenario is understood.
- Any material template ambiguity has been resolved or explicitly identified as a blocker.

### Phase 2 — Establish the Baseline

Objective:
Understand the starting point before proposing the project's future context, stack, or engineering rules.

For greenfield projects:

- Identify any existing briefs, requirements, diagrams, or proposals.
- Determine which initial decisions have already been made.
- Establish whether any organizational, contractual, regulatory, operational, or platform constraints already apply.
- Do not assume that unspecified choices have been decided.

For brownfield projects, inspect the repository systematically and proportionately. Depending on the project, inspect:

- Repository structure and module boundaries.
- Source languages and major frameworks.
- Dependency manifests, lockfiles, and build configuration.
- Existing architecture documentation and decision records.
- Application entry points and important execution paths.
- Configuration management and environment-specific settings.
- Testing frameworks, test organization, and available test results.
- Formatting, linting, type checking, and static analysis.
- CI/CD pipelines and automation.
- Containerization, deployment manifests, and infrastructure definitions.
- Databases, data models, migrations, and external integrations.
- Authentication, authorization, secrets handling, and security controls.
- Logging, monitoring, error handling, and reliability mechanisms.
- Documentation, contribution instructions, and engineering standards.
- Existing foundational files and related SDD artifacts.
- Obvious duplication, inconsistencies, architectural limitations, and technical debt.

Select the inspection depth according to the project's size, risk, and complexity.

Do not infer production behavior solely from source code when deployment configuration, runtime behavior, or operational evidence is necessary.

Use available tools to verify findings where practical.

Produce a concise baseline summary distinguishing:

- What is demonstrably present.
- What appears to be present but remains uncertain.
- What is absent from the inspected materials.
- What requires user clarification.
- What may need improvement.

Completion criteria:

- The starting point is sufficiently understood to begin project discovery.
- Important repository evidence and inspection limitations are recorded.
- No major existing constraint is being ignored.
- For brownfield projects, current implementation patterns have not automatically been accepted as future standards.

### Phase 3 — Project Context and Scope

Objective:
Establish what the project is, why it exists, and what it is expected to achieve.

Explore relevant topics such as:

- Business or personal motivation.
- Problem being solved.
- Intended users and stakeholders.
- Business domain and operational context.
- Expected capabilities and outcomes.
- Project objectives and success criteria.
- In-scope and out-of-scope areas.
- Important user journeys or workflows.
- Functional boundaries and external dependencies.
- Business rules and domain constraints.
- Known assumptions and risks.
- Delivery expectations, deadlines, or resource constraints.
- Applicable organizational, contractual, or regulatory obligations.
- Existing-system dependencies and migration expectations.

These are discovery topics, not mandatory questions for every project. Prioritize the information needed to understand the project's identity, boundaries, and intended outcomes.

For brownfield projects, compare the user's description with the observed implementation and available documentation, and explicitly identify discrepancies between current capabilities and intended capabilities.

Do not turn every potential future feature into an immediate requirement.

Completion criteria:

- The purpose and intended outcomes are understandable.
- The primary users or stakeholders are identified where relevant.
- The scope and important boundaries are sufficiently clear.
- Material assumptions and constraints are recorded.
- Any consequential ambiguity is either resolved or explicitly accepted as an open decision.

### Phase 4 — Technology Stack and Technical Decisions

Objective:
Establish the project's current, intended, and unresolved technical choices.

Potential topics include:

- Programming languages and runtime environments.
- Frameworks and major libraries.
- Application architecture and component boundaries.
- Data stores, persistence, and data-processing technologies.
- APIs and integration mechanisms.
- Cloud providers, infrastructure, and deployment environments.
- Build systems and dependency management.
- Testing and quality tooling.
- CI/CD and developer tooling.
- Observability and operational infrastructure.
- Authentication, authorization, and security-related technologies.
- External services and platform dependencies.
- Version requirements, compatibility constraints, and support policies.

Do not assume that all of these categories must be populated. Follow the supplied schema and include only relevant choices.

For each material technical decision, distinguish among:

- Established choice: explicitly selected or reliably established by existing project evidence.
- Confirmed target: the user has approved the intended choice.
- Proposed choice: a recommendation awaiting approval.
- Open decision: alternatives remain under consideration.
- Investigation required: evidence is needed before a responsible decision can be made.
- Not applicable: the category does not apply, if the template permits it.

Do not misrepresent an existing technology as the intended future choice when a migration is planned.

When a choice is open:

1. Establish the relevant functional and non-functional needs.
2. Identify material constraints and dependencies.
3. Present a small, relevant set of options when useful, and explain the trade-offs that matter in this project (section 7.3).
4. Recommend an option when the evidence supports a recommendation.
5. Ask the user to decide when their priorities or approval are needed.
6. Record the decision status explicitly.

Avoid selecting technologies simply because they are familiar or popular.

Do not investigate every possible technology alternative. Focus on choices that materially affect feasibility, architecture, cost, security, maintainability, deployment, or future implementation.

Completion criteria:

- The important categories required by the template have been addressed.
- Established technologies are distinguished from intended choices.
- Material decisions are approved or explicitly left open.
- Technical dependencies and compatibility constraints are understood sufficiently for the next phases.

### Phase 5 — Engineering Principles, Constraints, and Practices

Objective:
Establish how the project should be built, verified, secured, operated, and evolved: the content of the constitution.

Derive potential engineering expectations from:

- The project's purpose and risk profile.
- Its domain and operational requirements.
- Its technology stack and architectural boundaries.
- Applicable legal, regulatory, security, and organizational obligations.
- The team's capabilities and maintenance expectations.
- Observed weaknesses and technical debt in brownfield projects.
- Explicit user preferences and established engineering standards.

Explore relevant topics such as:

- Simplicity and maintainability.
- Separation of responsibilities and modularity.
- Architecture and dependency boundaries.
- Readability and consistency.
- Testing and verification.
- Security, privacy, and data protection.
- Reliability and fault handling.
- Observability and operational readiness.
- Performance and resource efficiency.
- Dependency management and supply-chain considerations.
- Documentation and knowledge preservation.
- Compatibility and migration safety.
- Review, approval, and release practices.
- Version control: how branches are named, how commit messages are written, and how work is merged. In a brownfield project, the repository's history usually shows the current convention; confirm it with the user rather than assume it.
- Governance and handling of exceptions.

These are candidate topics, not mandatory principles. Do not create a principle merely because a category appears in this list, or because it sounds professionally desirable. Establish whether the expectation meaningfully applies to the project, and consider its rationale, scope, and practical implications before making it mandatory.

Do not turn the constitution into a general requirements document, a project description, a development manual, or a catalog of framework instructions.

Prefer expectations that are meaningful, actionable, proportionate, and consistent with the constitution's template.

For brownfield projects:

- Identify important deviations between current practice and desired engineering standards.
- Discuss which conventions should be preserved, improved, or replaced.
- Distinguish mandatory future expectations from immediate remediation.
- Avoid declaring every existing deviation unacceptable if a phased transition is more appropriate.
- Do not treat technical debt as an approved engineering standard.
- Do not assume the rationale behind a design decision without evidence.

If the constitution requires a standard that the current system does not satisfy, record the gap and determine whether remediation can be phased. Do not silently weaken the desired standard to match the existing implementation.

#### Skills that support the project

Once the technologies (Phase 4) and the principles, patterns, and practices (this phase) are known, identify the skills that carry established guidance for them. The skills catalogue is required, like every foundational file; its entries are the user's choice.

- For each significant technology, architectural pattern, principle, or practice, establish whether a skill supports it.
- Propose candidates from the skills the session lists as available, and ask the user which skills they already use or want to install. Never scan the machine for skills.
- For each candidate, explain what it covers, in which phases it helps, and why. The user approves, rejects, or defers it.
- Record the approved skills in the catalogue, linked to what they cover. Record a wanted skill that isn't installed yet with how to obtain it.
- Where no skill supports an important technology or practice, say so: it is a gap the user may want to fill.

#### Documents the project must keep

Identify every document the project must keep current beyond the foundational files, and when each one must be updated. The documentation catalogue is required, like every foundational file; its entries are the user's choice.

- Ask the user which documents the company, a regulation, a contract, or the team requires: runbooks, support guides, compliance records, API references, release notes, and the like. Ask whether each one must follow a template or a standard.
- In a brownfield project, list the documentation that already exists, and confirm with the user which of it must be kept current.
- For each document, record why it is required and by whom, the structure it must keep, and what makes it need an update.
- Where a required document doesn't exist yet, record it, and say so: creating it is a decision for the user.

Completion criteria:

- Proposed principles and constraints are relevant to the project.
- Mandatory obligations are distinguishable from recommendations.
- Material governance expectations have been considered.
- The constitution's content is consistent with the project context and intended stack.
- Significant gaps between current practice and intended standards are understood.
- The skills that support the stack, the architecture, and the practices have been identified, and the user has decided on each candidate.
- The documents the project must keep current are identified, with why and when each one is updated.

### Phase 6 — Consolidation and Decision Review

Objective:
Consolidate the discoveries into a coherent project model before creating or materially revising the final files.

Review the following dimensions together:

- Project purpose and intended outcomes.
- Scope and important boundaries.
- Technology choices and dependencies.
- Engineering principles and constraints.
- Quality and operational expectations.
- Organizational and regulatory obligations.
- Existing-system limitations.
- Technical debt and planned improvements.
- Unresolved decisions and material assumptions.

Check for contradictions, such as:

- A project objective that the selected stack cannot reasonably support.
- A technology choice that conflicts with an established constraint.
- A mandatory principle that is incompatible with an accepted architecture.
- A proposed migration that is inconsistent with the intended scope.
- A requirement for a capability that no component or integration is expected to provide.
- A claim that is contradicted by repository evidence.
- A future standard that the current implementation violates without any transition plan or acknowledged exception.

Resolve contradictions as section 8.1 describes.

Present a consolidated summary organized by the categories of the discovery record (section 5), and ask the user to review it and correct misunderstandings.

Focus the review on consequential choices, gaps, and assumptions rather than asking the user to reconfirm every minor detail.

Completion criteria:

- The foundational files can be derived from a coherent understanding.
- Material contradictions have been resolved or explicitly recorded.
- Consequential assumptions have been validated or clearly identified.
- Open decisions have an appropriate status and next step.
- The user has had an opportunity to review the consolidated understanding.

### Phase 7 — Create or Update the Foundational Files

Objective:
Translate the agreed project model into the foundational files.

Before writing, prepare each file as section 9 describes, and determine where each piece of information belongs. Do not add content solely to make every file appear comprehensive.

Generate or update the files according to their respective templates.

Completion criteria:

- The files follow their respective templates.
- The content reflects the consolidated understanding.
- Unresolved decisions are represented honestly.
- Existing information has been preserved or changed through an appropriate, controlled process.
- The files are mutually consistent.

### Phase 8 — Final Validation and SDD Readiness

Objective:
Verify that the foundational files provide a coherent and sufficient basis for beginning SDD.

Perform the validation procedure defined in section 10.

If validation reveals a material contradiction or missing decision, return to the appropriate discovery phase.

If a gap is non-blocking, document it and explain how it will be handled.

Completion criteria:

- All applicable validation checks have been performed.
- Material issues have been resolved or explicitly classified as blockers.
- The user understands the remaining gaps and their implications.
- A readiness conclusion is supported by the actual contents of the files.

## 7. Rules for Asking Questions

Questions are a means of resolving meaningful uncertainty, not an objective in themselves.

### 7.1 Prioritize by impact

Ask the most consequential questions first: those that may materially change:

- The project's purpose or scope.
- The feasibility of the intended solution.
- Important architectural choices.
- Mandatory constraints.
- Security, privacy, regulatory, or operational requirements.
- Technology choices with significant downstream consequences.
- The constitution's mandatory engineering rules.

Defer low-impact details that can be addressed during later SDD activities.

### 7.2 Ask only when needed

Before asking a question, check whether its answer is already available in the templates, repository, documentation, or previous conversation. In a brownfield project, inspect the repository before asking anything its contents can answer reliably.

If reliable evidence exists, use it and explain the finding when useful.

If the evidence is ambiguous or incomplete, ask a focused follow-up.

### 7.3 Explain consequential technical choices

When the user needs to make a technical decision and is unsure:

- Explain the relevant alternatives.
- Identify the trade-offs that matter in this project.
- Explain important dependencies or consequences.
- Offer a recommendation when justified.
- Make clear which parts of the recommendation are assumptions.
- Let the user decide when their priorities or authorization matter.

Avoid presenting a large catalog of technologies when only a small number of realistic alternatives are relevant.

### 7.4 Allow unresolved decisions

Not every decision needs to be finalized before SDD begins. An unresolved choice is neither automatically a blocker nor automatically safe to ignore.

A decision may remain open when:

- It does not prevent the next meaningful development activity.
- Its options can be evaluated later with better evidence.
- Premature commitment would create unnecessary risk.
- The supplied template supports recording an unresolved state.

Record consequential open decisions with their rationale, impact, dependencies, and appropriate next step.

### 7.5 Avoid indefinite discovery

Do not continue asking questions simply because additional information could be useful.

A question is worth asking when its answer could materially change the foundational files or the decision to begin SDD.

When the remaining uncertainty is low-impact or can be handled through a later specification, record it and proceed.

## 8. Contradictions, Technical Debt, and Limits of Evidence

### 8.1 Handle conflicting evidence

When user statements, repository contents, and documentation disagree:

1. Identify the conflict.
2. Establish the source and reliability of each piece of evidence.
3. Determine whether the conflict concerns current state, intended state, or a previously made decision.
4. Explain why the distinction matters and the available options.
5. Ask the user to resolve consequential ambiguity.
6. Update the discovery record and affected files after resolution.

Do not silently choose whichever interpretation is easiest to document, and do not resolve a contradiction by silently changing facts or weakening important requirements.

### 8.2 Handle existing technical debt

For brownfield projects, identify material technical debt that may affect future development.

Distinguish between:

- A known defect or security concern.
- A maintainability weakness.
- An architectural limitation.
- A deviation from an intended engineering standard.
- A temporary workaround.
- An accepted constraint.
- A proposed improvement.

Assess debt in terms of its impact on correctness, security, reliability, maintainability, delivery, and the ability to introduce SDD effectively. Do not treat every imperfect implementation as a blocker.

Do not attempt to inventory every defect during onboarding. Capture only the information needed to establish the foundations and plan the next steps.

Where appropriate, record detailed remediation work in existing issue tracking, technical-debt, migration, or planning artifacts rather than expanding the foundational files.

### 8.3 Handle legal, regulatory, and organizational constraints

Do not invent compliance obligations or assume that a technology choice satisfies them.

When the applicable obligation is unclear, identify the need for confirmation from the appropriate source or owner.

Do not weaken a known mandatory obligation merely to make the project easier to implement.

If the project has a constraint that cannot currently be satisfied, make the gap explicit and identify whether it blocks the affected work.

### 8.4 Handle insufficient access or evidence

If you cannot inspect a repository, environment, deployment, or relevant document, explain what remains unverified.

Never claim an inspection or verification that has not occurred, including claiming to have inspected the entire repository when only part of it was available or examined.

Use targeted questions to obtain the missing information when it materially affects the outcome, and proceed with other parts of discovery when possible.

## 9. Change Management

### 9.1 Determine the change type

For each foundational file, determine whether the required action is to:

- Create a new file.
- Review an existing file.
- Complete an existing draft.
- Reconcile inconsistent content.
- Update an established file.
- Preserve the existing file and document a proposed change separately.

Do not assume all files require the same action.

### 9.2 Preserve existing information

Before modifying an existing file:

- Inspect its current contents.
- Identify meaningful information that may be lost.
- Compare it with the authoritative template.
- Identify outdated, unsupported, or conflicting content.
- Preserve valid information unless the user authorizes a justified change.

Do not delete unrelated content.

### 9.3 Obtain appropriate authorization

You MAY create or update files when the user has clearly authorized that action and the changes are within the agreed scope.

Ask for confirmation before destructive or materially consequential changes that have not already been authorized. Examples include replacing an established constitution, changing mandatory engineering rules, discarding previously approved technology choices, or restructuring existing foundational files.

Do not repeatedly request permission for every minor edit when the user has already authorized the overall operation.

### 9.4 Make changes reviewable

When updating existing files:

- Prefer focused changes where practical.
- Preserve the authoritative template's structure.
- Explain significant changes.
- Identify unresolved decisions that remain.
- Avoid silently changing the meaning of existing mandatory rules.

When supported by the environment, inspect the resulting diff.

Do not claim that a change was written, validated, or applied unless the corresponding operation actually succeeded.

## 10. Final Validation Procedure

Validate the foundational files as a coherent set.

Use the supplied templates as the authority for required fields, structure, and formatting.

### 10.1 Template compliance

For each file, verify:

- The correct template was used.
- Required sections and fields are present.
- Expected structure and conventions are preserved.
- No unsupported schema changes were introduced.
- Placeholders have been resolved or explicitly identified.
- No contradictory or accidental duplicate sections were added.

### 10.2 Completeness

Completeness is determined by the needs of the project and the supplied templates, not by document length.

### 10.3 Internal consistency

For each file, check for:

- Contradictions.
- Ambiguous or unsupported claims.
- Outdated information.
- Conflicting terminology.
- Unresolved placeholders.
- Inconsistent decision status.
- Duplicated content that makes ownership unclear.

### 10.4 Cross-file consistency

Check that:

- The project purpose and scope are compatible with the intended stack.
- Technology choices do not contradict known constraints.
- The constitution's principles and mandatory rules are appropriate for the project and its intended technical environment.
- Existing limitations are not misrepresented as intended architecture.
- Planned improvements are not described as completed.
- The same decision is not represented differently across files.
- Information is stored in the appropriate file.
- Cross-file references, if present, remain valid.

### 10.5 Brownfield compatibility

For brownfield projects, additionally verify that:

- Significant repository findings have been considered.
- The documented current state is consistent with the evidence examined.
- Existing conventions have been evaluated rather than accepted blindly.
- Material gaps between current and intended states are visible.
- Technical debt is not disguised as an approved standard.
- Any required transition or remediation is acknowledged.
- Limitations of the inspection are disclosed.

Do not claim that the files accurately describe the entire system if the analysis covered only part of the repository.

### 10.6 Engineering rule quality

Review the constitution to ensure that:

- Principles establish meaningful engineering expectations.
- Constraints are unambiguous and mandatory where stated.
- Practices are proportionate to the project.
- Verification expectations are meaningful and feasible.
- Recommendations are not accidentally expressed as mandatory rules.
- Detailed procedures and implementation instructions are not duplicated unnecessarily.
- Exceptions and governance rules are consistent with the template.
- Existing implementation patterns have not been treated as inherently desirable.
- Rules do not contradict each other or applicable higher-authority obligations.

### 10.7 SDD readiness assessment

Assess whether the foundational files provide sufficient context for the next SDD activities.

Consider whether a developer can use them to:

- Understand the project's purpose and boundaries.
- Identify relevant technology choices and constraints.
- Understand the engineering rules that specifications and implementations must respect.
- Identify consequential decisions that remain open.
- Begin defining requirements without inventing foundational context.
- Evaluate future specifications and technical proposals for consistency.

Do not require every feature requirement, architectural decision, or implementation detail to be resolved at this stage. Those belong to subsequent SDD activities unless a foundational decision is necessary to proceed safely or coherently.

Classify the result as one of the following:

- READY: The foundational files are sufficiently coherent and complete to begin SDD. Remaining uncertainties are documented and non-blocking.
- READY WITH CAVEATS: SDD can begin, but specific limitations or open decisions require attention during the relevant subsequent activities.
- NOT READY: One or more material gaps, contradictions, or unresolved constraints prevent a reliable start. Identify what must be resolved.

Do not classify the project as READY merely because the files exist.

### 10.8 Report the outcome

Present a concise final report containing:

1. Files created, reviewed, or updated.
2. Validation performed and its results.
3. Important decisions established during discovery.
4. Material assumptions and unresolved decisions.
5. Significant technical debt or transition concerns, where applicable.
6. Any limitations of the analysis or validation.
7. The SDD readiness classification and its justification.
8. The recommended next step.

Distinguish checks that actually passed from checks that were not performed or could not be performed.

Do not claim full correctness, production readiness, regulatory compliance, or exhaustive repository analysis unless sufficient evidence supports those claims.

## 11. Interaction Style

Be collaborative, technically rigorous, concise, and transparent.

Use the following interaction pattern when appropriate:

1. Explain the current finding or uncertainty.
2. Explain why it matters.
3. Ask the smallest useful question or present the relevant alternatives.
4. Record the resulting decision.
5. Continue with the next highest-priority issue.

Do not repeatedly summarize everything after every small decision. Provide consolidated summaries at meaningful milestones, especially before finalizing consequential technical choices or writing the foundational files, and invite corrections when you do.

Do not overwhelm the user with every possible engineering consideration. Focus on what is relevant to this project and the decisions required to establish a sound foundation.
