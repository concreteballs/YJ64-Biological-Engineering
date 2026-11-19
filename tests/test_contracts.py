import pytest

from yj64_bio.contracts import (
    CandidateRef, ContributionResponse, CrossDisciplinaryAssessment,
    DisciplineReview, EnhancementProposal, EvidenceRef, ReviewStatus,
    affected_reviews_to_invalidate,
)


@pytest.fixture
def candidate():
    return CandidateRef("bio-candidate-1", 1, "1.0")


def test_missing_relevant_review_blocks_acceptance(candidate):
    assessment = CrossDisciplinaryAssessment(candidate, frozenset({"biology", "materials"}), (), ())
    assert assessment.missing_reviews() == frozenset({"biology", "materials"})
    assert not assessment.may_accept()


def test_originating_module_cannot_self_certify(candidate):
    review = DisciplineReview("biology", candidate, ReviewStatus.PASS, "Domain checks passed")
    contribution = ContributionResponse("biology", candidate, no_proposal=True,
                                         no_proposal_rationale="No useful cross-domain proposal found")
    assessment = CrossDisciplinaryAssessment(candidate, frozenset({"biology", "materials"}),
                                             (review,), (contribution,))
    assert not assessment.may_accept()


def test_reject_blocks_acceptance_even_with_complete_contributions(candidate):
    reviews = (
        DisciplineReview("biology", candidate, ReviewStatus.PASS, "Local review passed"),
        DisciplineReview("materials", candidate, ReviewStatus.REJECT, "Material interface fails"),
    )
    contributions = tuple(
        ContributionResponse(m, candidate, no_proposal=True, no_proposal_rationale="No proposal")
        for m in ("biology", "materials")
    )
    assessment = CrossDisciplinaryAssessment(candidate, frozenset({"biology", "materials"}),
                                             reviews, contributions)
    assert not assessment.may_accept()


def test_every_relevant_module_must_contribute(candidate):
    review = DisciplineReview("biology", candidate, ReviewStatus.PASS, "Reviewed")
    contribution = ContributionResponse("biology", candidate, no_proposal=True,
                                         no_proposal_rationale="No proposal")
    assessment = CrossDisciplinaryAssessment(candidate, frozenset({"biology", "materials"}),
                                             (review,), (contribution,))
    assert assessment.missing_contributions() == frozenset({"materials"})
    assert not assessment.may_accept()


def test_enhancement_proposal_is_version_pinned(candidate):
    proposal = EnhancementProposal(
        proposal_id="p-1", proposing_module="materials", candidate=candidate,
        parent_objective="Improve actuator durability", improvement="Add a fatigue-resistant layer",
        mechanism="Material fatigue modelling", expected_benefit="Longer cycle life",
        success_criteria=("Increase validated cycle life by 20%",),
        evidence=(EvidenceRef("paper:example", "literature"),),
    )
    response = ContributionResponse("materials", candidate, proposals=(proposal,))
    assert response.proposals[0].candidate == candidate


def test_candidate_mismatch_rejected(candidate):
    other = CandidateRef("bio-candidate-1", 2, "1.0")
    with pytest.raises(ValueError):
        ContributionResponse("materials", candidate, proposals=(
            EnhancementProposal(
                proposal_id="p-2", proposing_module="materials", candidate=other,
                parent_objective="Improve", improvement="Improve", mechanism="Mechanism",
                expected_benefit="Benefit", success_criteria=("criterion",), evidence=(),
            ),
        ))


def test_downstream_review_invalidation_is_transitive():
    dependencies = {
        "biology": frozenset({"materials"}),
        "materials": frozenset({"robotics"}),
        "robotics": frozenset({"safety"}),
    }
    assert affected_reviews_to_invalidate(frozenset({"biology"}), dependencies) == frozenset(
        {"materials", "robotics", "safety"}
    )
