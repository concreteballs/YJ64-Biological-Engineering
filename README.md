# YJ64 Biological Engineering

Independent biological-engineering module for the YJ64 ecosystem.

**Status:** architecture scaffold; no biological execution, wet-lab automation, organism handling, or deployment capability is implemented.

## Scope
- Biological and bio-derived materials and biocomposites
- Biohybrid actuator concepts as research candidates
- Biological surface interactions, biofouling and degradation assessment
- Contamination monitoring and validated decontamination compatibility
- Containment, exposure, persistence, waste and end-of-life assessment

Molecular/genetic design is owned by the separate YJ64 Molecular & Genetic Engineering module.

## Core rule
A module's own domain checks never constitute final system acceptance. Every candidate must undergo independent review by all relevant disciplines. Missing reviews are not approval.

## Cross-disciplinary contribution
Each relevant module must also return either:
- one or more evidence-linked enhancement proposals explaining how its discipline could improve the parent process; or
- an explicit `no_proposal` response with rationale.

Enhancement proposals are advisory, separately evaluated by the parent process, and never silently applied. Acceptance/rejection and rationale are recorded. Changes invalidate affected downstream reviews.

## Initial code
- `src/yj64_bio/contracts.py`: typed contracts and fail-closed assessment logic
- `tests/test_contracts.py`: contract tests

See [architecture](docs/ARCHITECTURE.md).
