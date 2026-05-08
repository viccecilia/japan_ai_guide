from app.schemas.recommendation_governance import RecommendationGovernance


def evaluate_governance(
    relevance_score: float,
    user_fit_score: float = 0.7,
    partner_weight: float = 0,
    season_boost: float = 0,
    campaign_boost: float = 0,
) -> RecommendationGovernance:
    safe_partner_weight = min(max(partner_weight, 0), 0.2)
    boost = min(safe_partner_weight + max(season_boost, 0) + max(campaign_boost, 0), 0.15)
    final_score = min(max(relevance_score, 0), 1)
    if relevance_score >= 0.6:
        final_score = min(final_score + boost, 1)

    return RecommendationGovernance(
        partner_weight=safe_partner_weight,
        relevance_score=min(max(relevance_score, 0), 1),
        user_fit_score=min(max(user_fit_score, 0), 1),
        safety_threshold=0.6,
        promotion_flag=safe_partner_weight > 0,
        final_score=final_score,
    )
