import type { RecommendationSection as RecommendationSectionData } from "../../../types/answer-card";
import { ItineraryFlowView } from "./ItineraryFlowView";

export function RecommendationSection({
  section,
  onPromptSelect,
}: {
  section: RecommendationSectionData;
  onPromptSelect?: (prompt: string) => void;
}) {
  const prompts = section.prompts ?? [];
  const itineraries = section.itineraries ?? [];
  if (section.cards.length === 0 && prompts.length === 0 && itineraries.length === 0) return null;

  return (
    <section className="jag-recommendation-section">
      <div>
        <div className="jag-section-title">{section.title}</div>
        {section.section_intro ? <p className="jag-section-intro">{section.section_intro}</p> : null}
        {section.section_narrative ? <p className="jag-section-narrative">{section.section_narrative}</p> : null}
      </div>

      {section.section_type === "itinerary_section" ? (
        <ItineraryFlowView itineraries={itineraries} />
      ) : section.section_type === "suggested_prompts" ? (
        <div className="jag-prompt-grid">
          {prompts.map((prompt) => (
            <button
              key={prompt}
              className="jag-prompt-button"
              type="button"
              onClick={() => onPromptSelect?.(prompt)}
            >
              {prompt}
            </button>
          ))}
        </div>
      ) : (
        <div className="jag-section-grid">
          {section.cards.map((card) => (
            <article key={`${section.section_type}-${card.id}`} className="jag-section-card">
              <h3 className="line-clamp-1 text-sm font-black text-[var(--jag-color-ink)]">{card.title}</h3>
              <p className="mt-2 line-clamp-2 text-xs leading-5 text-[var(--jag-color-muted)]">
                {card.subtitle}
              </p>
              {card.recommendation_reason ? (
                <p className="mt-3 text-xs font-bold leading-5 text-blue-700">{card.recommendation_reason}</p>
              ) : null}
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
