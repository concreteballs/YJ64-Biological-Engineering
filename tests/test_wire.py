import pytest
from yj64_bio.contracts import CandidateRef, ContributionResponse, DisciplineReview, EnhancementProposal, EvidenceRef, ReviewStatus
from yj64_bio.wire import to_wire_candidate, to_wire_contribution, to_wire_evidence, to_wire_proposal, to_wire_review

def candidate():
    return CandidateRef("bio-1", 2, "1.0", "biology")

def evidence(**kwargs):
    return EvidenceRef(source="paper:123", evidence_kind="literature", evidence_id="ev-123",
                       version="2025", limitations=("in vitro only",), **kwargs)

def test_candidate_identity_is_preserved():
    wire = to_wire_candidate(candidate())
    assert wire["schema_id"] == "yj64.cross_module.candidate.v1"
    assert wire["candidate_id"] == "bio-1" and wire["version"] == 2
    assert wire["candidate_schema_version"] == "1.0" and wire["origin_module"] == "biology"

def test_evidence_requires_stable_id_and_preserves_provenance():
    wire = to_wire_evidence(evidence(confidence=0.7))
    assert wire["evidence_id"] == "ev-123" and wire["evidence_type"] == "literature"
    assert wire["version"] == "2025" and wire["limitations"] == ["in vitro only"]
    assert wire["confidence"] == 0.7
    with pytest.raises(ValueError):
        to_wire_evidence(EvidenceRef("paper:123", "literature"))

def test_review_requires_explicit_host_version():
    review = DisciplineReview("biology", candidate(), ReviewStatus.CONDITIONAL, "Follow-up required",
                              conditions=("validate containment",))
    with pytest.raises(ValueError):
        to_wire_review(review, reviewer_version="")
    assert to_wire_review(review, reviewer_version="0.1.0")["reviewer_version"] == "0.1.0"

def test_proposal_maps_parent_objective():
    proposal = EnhancementProposal("p1", "biology", candidate(), "Improve robustness", "Add layer",
                                   "Comparative modelling", "Higher durability", ("cycle life",), (evidence(),))
    assert to_wire_proposal(proposal)["objective"] == "Improve robustness"

def test_no_proposal_reason_maps_to_rationale():
    response = ContributionResponse("biology", candidate(), no_proposal=True,
                                    no_proposal_rationale="No evidence-backed improvement")
    assert to_wire_contribution(response)["rationale"] == "No evidence-backed improvement"


def test_wire_proposal_rejects_missing_schema_required_evidence():
    proposal = EnhancementProposal(
        "p-no-evidence", "biology", candidate(), "Improve robustness", "Add layer",
        "Comparative modelling", "Higher durability", ("cycle life",), (),
    )
    with pytest.raises(ValueError, match="require evidence"):
        to_wire_proposal(proposal)
