import type { AnswerCard } from "../../../types/answer-card";

export function RelatedCards({ cards }: { cards: AnswerCard[] }) {
  if (cards.length === 0) return null;

  return (
    <section className="jag-related-flow" aria-label="Related cards">
      {cards.map((card) => (
        <article key={card.id} className="jag-related-card">
          <div className="text-xs font-black uppercase tracking-normal text-blue-600">
            {card.metadata?.ranking?.content_type ?? "related"}
          </div>
          <h3 className="mt-2 line-clamp-2 text-base font-black text-[var(--jag-color-ink)]">
            {card.title}
          </h3>
          <p className="mt-2 line-clamp-2 text-xs leading-5 text-[var(--jag-color-muted)]">
            {card.description}
          </p>
          <div className="mt-3 text-xs font-bold text-[var(--jag-color-muted)]">
            {card.recommendation_reason ?? "Related recommendation"}
          </div>
        </article>
      ))}
    </section>
  );
}
