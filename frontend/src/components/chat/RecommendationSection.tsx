import type { RecommendationSection as RecommendationSectionData } from "../../../types/answer-card";

export function RecommendationSection({ section }: { section: RecommendationSectionData }) {
  if (section.cards.length === 0) return null;

  return (
    <section className="jag-recommendation-section">
      <div className="jag-section-title">{section.title}</div>
      <div className="jag-section-grid">
        {section.cards.map((card) => (
          <article key={`${section.section_type}-${card.id}`} className="jag-section-card">
            <h3 className="line-clamp-1 text-sm font-black text-[var(--jag-color-ink)]">{card.title}</h3>
            <p className="mt-2 line-clamp-2 text-xs leading-5 text-[var(--jag-color-muted)]">
              {card.subtitle}
            </p>
          </article>
        ))}
      </div>
    </section>
  );
}
