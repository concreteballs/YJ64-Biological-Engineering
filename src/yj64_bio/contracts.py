"""Typed, fail-closed contracts for cross-disciplinary review and improvement.

This module contains orchestration data contracts only. It does not execute
biological workflows or grant permissions.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet, Optional, Sequence


class ReviewStatus(str, Enum):
    PASS = "pass"
    CONDITIONAL = "conditional"
    REJECT = "reject"
    NOT_APPLICABLE = "not_applicable"
    NOT_REVIEWED = "not_reviewed"


class ProposalStatus(str, Enum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DEFERRED = "deferred"
    NEEDS_EVIDENCE = "needs_evidence"


@dataclass(frozen=True)
class CandidateRef:
    candidate_id: str
    version: int
    schema_version: str

    def __post_init__(self) -> None:
        if not self.candidate_id.strip() or self.version < 1 or not self.schema_version.strip():
            raise ValueError("candidate identity, positive version and schema version are required")


@dataclass(frozen=True)
class EvidenceRef:
    source: str
    evidence_kind: str
    confidence: Optional[float] = None

    def __post_init__(self) -> None:
        if not self.source.strip() or not self.evidence_kind.strip():
            raise ValueError("evidence source and kind are required")
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True)
class DisciplineReview:
    reviewer_module: str
    candidate: CandidateRef
    status: ReviewStatus
    rationale: str
    evidence: Sequence[EvidenceRef] = field(default_factory=tuple)
    assumptions: Sequence[str] = field(default_factory=tuple)
    uncertainty: Sequence[str] = field(default_factory=tuple)
    interface_findings: Sequence[str] = field(default_factory=tuple)
    hazards: Sequence[str] = field(default_factory=tuple)
    hard_constraints: Sequence[str] = field(default_factory=tuple)
    conditions: Sequence[str] = field(default_factory=tuple)
    unresolved_questions: Sequence[str] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.reviewer_module.strip() or not self.rationale.strip():
            raise ValueError("reviewer module and rationale are required")
        if self.status == ReviewStatus.NOT_APPLICABLE and not self.rationale.strip():
            raise ValueError("not-applicable reviews require a rationale")
        if self.status == ReviewStatus.CONDITIONAL and not self.conditions:
            raise ValueError("conditional review must state conditions")
        if self.status == ReviewStatus.REJECT and not self.rationale.strip():
            raise ValueError("rejection must state rationale")


@dataclass(frozen=True)
class EnhancementProposal:
    proposal_id: str
    proposing_module: str
    candidate: CandidateRef
    parent_objective: str
    improvement: str
    mechanism: str
    expected_benefit: str
    success_criteria: Sequence[str]
    evidence: Sequence[EvidenceRef]
    assumptions: Sequence[str] = field(default_factory=tuple)
    tradeoffs: Sequence[str] = field(default_factory=tuple)
    risks: Sequence[str] = field(default_factory=tuple)
    dependencies: Sequence[str] = field(default_factory=tuple)
    validation_plan: Sequence[str] = field(default_factory=tuple)
    status: ProposalStatus = ProposalStatus.PROPOSED
    decision_rationale: Optional[str] = None

    def __post_init__(self) -> None:
        required = (self.proposal_id, self.proposing_module, self.parent_objective,
                    self.improvement, self.mechanism, self.expected_benefit)
        if any(not value.strip() for value in required):
            raise ValueError("proposal identity, origin, objective and contribution are required")
        if not self.success_criteria:
            raise ValueError("enhancement proposal requires measurable success criteria")
        if self.status != ProposalStatus.PROPOSED and not (self.decision_rationale or "").strip():
            raise ValueError("parent decisions require a recorded rationale")


@dataclass(frozen=True)
class ContributionResponse:
    module_id: str
    candidate: CandidateRef
    proposals: Sequence[EnhancementProposal] = field(default_factory=tuple)
    no_proposal: bool = False
    no_proposal_rationale: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.module_id.strip():
            raise ValueError("module id is required")
        if self.no_proposal == bool(self.proposals):
            raise ValueError("provide proposals OR an explicit no-proposal response")
        if self.no_proposal and not (self.no_proposal_rationale or "").strip():
            raise ValueError("no-proposal response requires rationale")
        if any(p.candidate != self.candidate for p in self.proposals):
            raise ValueError("proposal candidate must match contribution candidate")


@dataclass(frozen=True)
class CrossDisciplinaryAssessment:
    candidate: CandidateRef
    relevant_modules: FrozenSet[str]
    reviews: Sequence[DisciplineReview]
    contributions: Sequence[ContributionResponse]

    def missing_reviews(self) -> FrozenSet[str]:
        completed = {
            r.reviewer_module for r in self.reviews
            if r.candidate == self.candidate and r.status != ReviewStatus.NOT_REVIEWED
        }
        return self.relevant_modules - completed

    def blocking_reviews(self) -> Sequence[DisciplineReview]:
        return tuple(
            r for r in self.reviews
            if r.candidate == self.candidate and (
                r.status in (ReviewStatus.REJECT, ReviewStatus.NOT_REVIEWED)
                or bool(r.hard_constraints)
                or (r.status == ReviewStatus.CONDITIONAL and bool(r.conditions))
            )
        )

    def missing_contributions(self) -> FrozenSet[str]:
        completed = {
            c.module_id for c in self.contributions
            if c.candidate == self.candidate
        }
        return self.relevant_modules - completed

    def may_accept(self) -> bool:
        """Fail closed: only complete, non-blocking reviews permit acceptance."""
        if self.missing_reviews() or self.missing_contributions():
            return False
        if self.blocking_reviews():
            return False
        reviewers = {
            r.reviewer_module for r in self.reviews
            if r.candidate == self.candidate
        }
        return self.relevant_modules.issubset(reviewers)


def affected_reviews_to_invalidate(
    changed_modules: FrozenSet[str],
    dependency_map: dict[str, FrozenSet[str]],
) -> FrozenSet[str]:
    """Return transitive downstream modules whose prior reviews are stale.

    dependency_map maps a source module to modules whose assessments depend on it.
    """
    invalidated = set()
    frontier = list(changed_modules)
    while frontier:
        source = frontier.pop()
        for dependent in dependency_map.get(source, frozenset()):
            if dependent not in invalidated and dependent not in changed_modules:
                invalidated.add(dependent)
                frontier.append(dependent)
    return frozenset(invalidated)
