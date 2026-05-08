import type { MultiCardResponse } from "../../../types/answer-card";
import { AnalyticsDebugPanel } from "./AnalyticsDebugPanel";
import { AnswerCard } from "./AnswerCard";
import { JourneyTimelineView } from "./JourneyTimelineView";
import { RecommendationSection } from "./RecommendationSection";
import { RelatedCards } from "./RelatedCards";
import { canShowInternalDebug } from "../../lib/frontendMode";

export function MultiCardResponseView({
  response,
  onPromptSelect,
}: {
  response: MultiCardResponse;
  onPromptSelect?: (prompt: string) => void;
}) {
  const showDebug = canShowInternalDebug();
  const timeline = response.metadata?.timeline ?? null;
  const timelineConstraint = response.metadata?.timeline_constraint ?? null;
  const adaptiveJourney = response.metadata?.adaptive_journey ?? null;
  const travelContext = response.metadata?.travel_context ?? null;
  const travelMemory = response.metadata?.travel_memory ?? null;
  const orchestration = response.metadata?.orchestration ?? response.main_card.metadata?.orchestration;
  const scores = [
    response.main_card.metadata?.ranking,
    ...(response.main_card.metadata?.related_candidates ?? []),
  ].filter(Boolean);

  return (
    <div className="jag-multi-card-flow">
      <AnswerCard card={response.main_card} />
      <RelatedCards cards={response.related_cards} />
      <JourneyTimelineView
        key={timeline?.timeline_id ?? "no-timeline"}
        timeline={timeline}
        constraint={timelineConstraint}
        adaptiveJourney={adaptiveJourney}
        travelContext={travelContext}
        travelMemory={travelMemory}
      />
      {response.sections.map((section) => (
        <RecommendationSection key={section.section_type} section={section} onPromptSelect={onPromptSelect} />
      ))}
      <AnalyticsDebugPanel response={response} />
      {showDebug ? (
        <div className="rounded-2xl border border-dashed border-indigo-200 bg-indigo-50 p-3 text-xs font-bold leading-5 text-indigo-800">
          <div>Main Card: {response.main_card.title}</div>
          <div>Related Cards Count: {response.related_cards.length}</div>
          <div>Section Count: {response.sections.length}</div>
          <div>Top Candidate Scores: {scores.map((score) => `${score?.slug}:${score?.score}`).join(", ") || "-"}</div>
          <div>Orchestration Strategy: {orchestration?.strategy ?? "-"}</div>
          <div>Section Order: {orchestration?.section_order?.join(", ") ?? "-"}</div>
          <div>Deduped Count: {orchestration?.deduped_count ?? 0}</div>
          <div>Timeline Days: {timeline?.days?.length ?? 0}</div>
          <div>City Transitions: {timeline?.transitions?.length ?? 0}</div>
          <div>Timeline Feasibility: {timelineConstraint?.timeline_feasibility ?? "-"}</div>
          <div>Adaptation Count: {adaptiveJourney?.adaptation_count ?? 0}</div>
          <div>Travel Context: {travelContext?.condition?.context_level ?? "-"}</div>
          <div>Memory Updates: {response.metadata?.analytics?.memory_updates ?? 0}</div>
        </div>
      ) : null}
    </div>
  );
}
