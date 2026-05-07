import type { MultiCardResponse } from "../../../types/answer-card";
import { AnswerCard } from "./AnswerCard";
import { RecommendationSection } from "./RecommendationSection";
import { RelatedCards } from "./RelatedCards";

export function MultiCardResponseView({ response }: { response: MultiCardResponse }) {
  const showDebug = process.env.NODE_ENV !== "production";
  const scores = [
    response.main_card.metadata?.ranking,
    ...(response.main_card.metadata?.related_candidates ?? []),
  ].filter(Boolean);

  return (
    <div className="jag-multi-card-flow">
      <AnswerCard card={response.main_card} />
      <RelatedCards cards={response.related_cards} />
      {response.sections.map((section) => (
        <RecommendationSection key={section.section_type} section={section} />
      ))}
      {showDebug ? (
        <div className="rounded-2xl border border-dashed border-indigo-200 bg-indigo-50 p-3 text-xs font-bold leading-5 text-indigo-800">
          <div>Main Card: {response.main_card.title}</div>
          <div>Related Cards Count: {response.related_cards.length}</div>
          <div>Section Count: {response.sections.length}</div>
          <div>Top Candidate Scores: {scores.map((score) => `${score?.slug}:${score?.score}`).join(", ") || "-"}</div>
        </div>
      ) : null}
    </div>
  );
}
