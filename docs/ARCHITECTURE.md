# Biological Engineering Module — Architecture

## 1. Independence and boundary
This is an independently versioned YJ64 module. It is neither a submodule of Engineering Core nor a submodule of Molecular & Genetic Engineering. Integration occurs through versioned task, evidence, interface, hazard, review and enhancement contracts.

The module owns biological materials and organism/system-level biological engineering analysis. It does not own molecular/genetic design, general chemistry, robot architecture or system-level approval.

## 2. Scope
1. Biological and bio-derived materials, biocomposites and biofabricated structures.
2. Biohybrid actuator concepts, treated as hypotheses until supported by reproducible evidence.
3. Microbial/fungal interactions with surfaces: colonisation, degradation and biofouling.
4. Controlled surface-protection and maintenance concepts.
5. Contamination monitoring, sensing, inspection and evidence management.
6. Compatibility assessment for validated cleaning, disinfection and decontamination.
7. Containment, exposure pathways, persistence, shedding, waste and end-of-life.
8. Human/environmental interface and lifecycle impact assessment.

## 3. Two mandatory outputs from every relevant discipline
For every candidate version, each relevant module must provide two logically independent outputs:

### A. Independent review
One of PASS, CONDITIONAL, REJECT, NOT_APPLICABLE_WITH_RATIONALE, or NOT_REVIEWED. A review identifies the exact candidate/version, scope, assumptions, evidence/provenance, uncertainty, interfaces, hazards, hard constraints and unresolved questions.

### B. Enhancement contribution
One or more proposals, or an explicit NO_PROPOSAL response with rationale. A proposal describes:
- the parent objective or candidate aspect it could improve;
- the originating discipline and mechanism of contribution;
- expected benefit and measurable success criteria;
- evidence/provenance and confidence;
- assumptions, costs, trade-offs, risks and dependencies;
- suggested validation and affected modules.

This second output is not merely criticism. A module should actively look for useful knowledge, methods, materials, models, constraints or alternatives from its own field that could strengthen the parent process—even when its review status is PASS.

## 4. Parent-process decision
The parent coordinator owns proposal triage. Each proposal is ACCEPTED, REJECTED, DEFERRED or NEEDS_EVIDENCE with a recorded rationale and decision version. Modules cannot apply their own suggestions directly to the parent candidate. Accepted proposals create a new candidate revision or explicit child task; affected downstream reviews and enhancement contributions are recalculated.

A proposal is not an approval, and acceptance of a proposal does not waive independent reviews. Conflicting suggestions remain visible and are escalated rather than averaged away.

## 5. Final acceptance invariants
- The originating module cannot self-certify system-level acceptability.
- All relevant independent reviews must be complete.
- Missing, timed-out or unavailable reviewers are NOT_REVIEWED, never approval.
- REJECT or unresolved hard constraints block acceptance.
- CONDITIONAL requires explicit satisfaction or disposition of every condition.
- NOT_APPLICABLE requires a reason and can be challenged by the coordinator.
- Candidate changes invalidate affected downstream reviews.
- Review and enhancement records are pinned to candidate, schema and module versions.

## 6. Biological safety and evidence boundaries
Prefer well-characterised non-pathogenic research systems and non-living alternatives where appropriate. Biological proposals require qualified biosafety review, suitable containment, exposure assessment, monitoring, validated inactivation and waste handling. No design objective may rely on uncontrolled spread, environmental release, increased pathogenicity, host-range expansion, immune evasion or resistance to containment.

This repository defines architecture and assessment contracts only. It does not provide organism construction, genetic modification, culture, propagation or pathogen-handling procedures. No autonomous wet-lab execution is in scope.

Bacteriophages are bacteria-specific, not universal disinfectants or general antiviral agents. Biological surface maintenance does not replace validated cleaning, disinfection or sterilisation.

## 7. Research evaluation
Compare biological candidates against non-biological baselines. For biohybrid actuators assess force, stroke, speed, efficiency, controllability, repeatability, fatigue, lifetime, environmental stability, energy/nutrient requirements, by-products, maintenance, containment and failure modes. Model output is not experimental validation.

## 8. Integration
The module publishes versioned candidate records and consumes reviewed outputs from Molecular & Genetic Engineering where applicable. Shared YJ64 contracts define lifecycle and orchestration; this repository owns biological domain semantics only.
