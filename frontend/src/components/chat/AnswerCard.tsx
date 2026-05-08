import type { AnswerCard as AnswerCardData, AnswerCardType } from "../../../types/answer_card";
import { canShowInternalDebug } from "../../lib/frontendMode";

type AnswerCardProps = {
  card?: Partial<AnswerCardData>;
};

const cardTypeLabels: Record<AnswerCardType, string> = {
  spot_card: "景点导览",
  city_card: "城市导览",
  food_card: "美食建议",
  route_card: "路线建议",
  culture_card: "文化故事",
  generic_card: "旅行建议",
};

const cardTypeTone: Record<AnswerCardType, string> = {
  spot_card: "bg-blue-50 text-blue-700",
  city_card: "bg-indigo-50 text-indigo-700",
  food_card: "bg-emerald-50 text-emerald-700",
  route_card: "bg-amber-50 text-amber-700",
  culture_card: "bg-violet-50 text-violet-700",
  generic_card: "bg-slate-100 text-slate-700",
};

const fallbackCard: AnswerCardData = {
  id: "fallback",
  card_type: "generic_card",
  title: "日本旅行导览",
  subtitle: "先从一个清晰方向开始",
  description: "我会先给你一版适合第一次来日本游客的基础建议，再帮你继续拆成景点、路线、美食和住宿。",
  story: "你可以直接问一个城市、景点、路线或文化问题，我会用导游式的方式整理重点。",
  audio: {},
  nearby: [],
  foods: [],
  hotels: [],
  actions: [{ label: "继续了解", action: "ask_followup", enabled: true, source: "mock" }],
  metadata: { language: "zh", mock: true, sources: ["mock"] },
};

export function AnswerCard({ card }: AnswerCardProps) {
  const safeCard = { ...fallbackCard, ...card };
  const cardType = safeCard.card_type ?? "generic_card";
  const nearby = safeCard.nearby ?? [];
  const foods = safeCard.foods ?? [];
  const hotels = safeCard.hotels ?? [];
  const actions = safeCard.actions ?? [];
  const intent = safeCard.metadata?.intent;
  const aiRuntime = safeCard.metadata?.ai_runtime;
  const contentSource = safeCard.metadata?.content_source;
  const cache = safeCard.metadata?.cache;
  const ranking = safeCard.metadata?.ranking;
  const relatedCandidates = safeCard.metadata?.related_candidates ?? [];
  const showDebug = canShowInternalDebug();

  return (
    <article className="jag-card jag-answer-card">
      <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
        <div className="min-w-0 flex-1">
          <div className={`jag-answer-badge ${cardTypeTone[cardType]}`}>
            {cardTypeLabels[cardType]}
          </div>
          <h2 className="break-words text-2xl font-black leading-tight tracking-normal text-[var(--jag-color-ink)] sm:text-3xl">
            {safeCard.title}
          </h2>
          <p className="mt-2 text-sm font-semibold leading-6 text-[var(--jag-color-muted)]">{safeCard.subtitle}</p>
          <p className="mt-4 max-w-3xl text-[15px] leading-8 text-[var(--jag-color-muted)]">
            {safeCard.description}
          </p>
          {safeCard.recommendation_reason ? (
            <p className="mt-4 inline-flex max-w-full rounded-full bg-blue-50 px-4 py-2 text-xs font-bold text-blue-700">
              {safeCard.recommendation_reason}
            </p>
          ) : null}
        </div>

        <div className="jag-guide-note">
          <div className="text-xs font-black uppercase tracking-normal text-white/70">AI Guide</div>
          <p className="mt-2 text-sm font-bold leading-6 text-white">
            我先帮你抓重点，再把下一步适合探索的方向放在下面。
          </p>
        </div>
      </div>

      <section className="jag-panel mt-6">
        <h3 className="text-sm font-black text-[var(--jag-color-ink)]">导游讲解</h3>
        <p className="mt-3 text-[15px] leading-8 text-[var(--jag-color-muted)]">{safeCard.story}</p>
      </section>

      <div className="mt-5 grid gap-4 lg:grid-cols-3">
        <ListPanel title="附近可以顺路看" empty="暂时没有附近建议，可以继续问路线或周边景点。" items={nearby.map((item) => `${item.name}${item.distance_text ? ` · ${item.distance_text}` : ""}`)} />
        <ListPanel title="可以搭配的美食" empty="暂时没有美食建议，可以继续问当地吃什么。" items={foods.map((item) => `${item.name}${item.area ? ` · ${item.area}` : ""}`)} />
        <ListPanel title="住宿判断方向" empty="暂时没有住宿建议，可以继续问适合住在哪个区域。" items={hotels.map((item) => `${item.name}${item.area ? ` · ${item.area}` : ""}`)} />
      </div>

      <div className="mt-5 flex flex-wrap gap-3">
        {actions.map((action) => (
          <button
            key={`${safeCard.id}-${action.action}-${action.label}`}
            className={action.enabled ? "jag-button-primary px-4 py-2 text-sm" : "jag-button-secondary px-4 py-2 text-sm opacity-70"}
            type="button"
            disabled={!action.enabled}
          >
            {action.label}
          </button>
        ))}
      </div>

      {showDebug && (intent || aiRuntime || contentSource || cache || ranking || relatedCandidates.length > 0) ? (
        <div className="jag-internal-debug mt-4">
          {intent ? (
            <>
              <div>Intent: {intent.intent_type}</div>
              <div>Entity: {intent.entity ?? "-"}</div>
              <div>Confidence: {intent.confidence.toFixed(2)}</div>
            </>
          ) : null}
          {aiRuntime ? (
            <>
              <div>AI Mode: {aiRuntime.mode ?? "-"}</div>
              <div>Realtime AI Used: {String(aiRuntime.realtime_ai_used ?? false)}</div>
              <div>Fallback Level: {aiRuntime.fallback_level ?? "-"}</div>
            </>
          ) : null}
          {contentSource ? (
            <>
              <div>Content Source: {contentSource.type ?? "-"}</div>
              <div>Slug: {contentSource.slug ?? "-"}</div>
              <div>Language: {contentSource.language ?? "-"}</div>
            </>
          ) : null}
          {cache ? (
            <>
              <div>Cache: {cache.hit ? "hit" : "miss"}</div>
              <div>Cache Key: {cache.key ?? "-"}</div>
            </>
          ) : null}
          {ranking ? (
            <div>
              Ranking: {ranking.slug ?? "-"} / {ranking.score?.toFixed(2) ?? "0.00"} / {ranking.matched_by ?? "-"}
            </div>
          ) : null}
          {relatedCandidates.length > 0 ? (
            <div className="mt-2">
              <div>Top Candidates:</div>
              <ul className="ml-4 list-disc">
                {[
                  ranking ? { slug: ranking.slug, score: ranking.score, content_type: ranking.content_type } : null,
                  ...relatedCandidates,
                ]
                  .filter(Boolean)
                  .map((candidate) => (
                    <li key={`${candidate?.slug}-${candidate?.score}`}>
                      {candidate?.slug ?? "-"} ({candidate?.score?.toFixed(2) ?? "0.00"})
                      {candidate?.content_type ? ` · ${candidate.content_type}` : ""}
                    </li>
                  ))}
              </ul>
            </div>
          ) : null}
        </div>
      ) : null}
    </article>
  );
}

function ListPanel({ title, empty, items }: { title: string; empty: string; items: string[] }) {
  return (
    <section className="jag-panel">
      <h3 className="text-sm font-black text-[var(--jag-color-ink)]">{title}</h3>
      {items.length > 0 ? (
        <ul className="mt-3 space-y-2 text-sm leading-6 text-[var(--jag-color-muted)]">
          {items.map((item) => (
            <li key={item} className="flex gap-2">
              <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-[var(--jag-color-primary)]" />
              <span>{item}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p className="mt-3 text-sm leading-6 text-[var(--jag-color-muted)]">{empty}</p>
      )}
    </section>
  );
}
