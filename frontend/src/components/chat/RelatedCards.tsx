import type { AnswerCard } from "../../../types/answer-card";

const contentTypeLabels: Record<string, string> = {
  spot: "顺路景点",
  city: "城市方向",
  food: "美食方向",
  route: "路线参考",
  culture: "文化背景",
  hotel: "住宿建议",
};

export function RelatedCards({ cards }: { cards: AnswerCard[] }) {
  if (cards.length === 0) return null;

  return (
    <section className="jag-related-flow" aria-label="Related cards">
      {cards.map((card) => (
        <article key={card.id} className="jag-related-card">
          <div className="text-xs font-black uppercase tracking-normal text-blue-600">
            {contentTypeLabels[String(card.metadata?.ranking?.content_type ?? "")] ?? "继续探索"}
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
