import type { AnswerCard as AnswerCardData, AnswerCardType } from "../../../types/answer_card";

type AnswerCardProps = {
  card?: Partial<AnswerCardData>;
};

const cardTypeLabels: Record<AnswerCardType, string> = {
  spot_card: "景点卡片",
  city_card: "城市卡片",
  food_card: "美食卡片",
  route_card: "路线卡片",
  culture_card: "文化卡片",
  generic_card: "通用卡片",
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
  subtitle: "通用回答",
  description: "当前 AnswerCard 字段不完整，前端使用安全占位内容展示。",
  story: "请继续输入景点、城市、美食、路线或文化问题。",
  audio: {},
  nearby: [],
  foods: [],
  hotels: [],
  actions: [{ label: "继续追问", action: "ask_followup", enabled: true, source: "mock" }],
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
  const showDebug = process.env.NODE_ENV !== "production";

  return (
    <article className="jag-card">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
        <div className="min-w-0">
          <div className={`jag-answer-badge ${cardTypeTone[cardType]}`}>
            {cardTypeLabels[cardType]} · {contentSource?.type === "content_library" ? "Content Library" : "Template"}
          </div>
          <h2 className="break-all text-2xl font-black tracking-normal text-[var(--jag-color-ink)] sm:break-normal">
            {safeCard.title}
          </h2>
          <p className="mt-2 text-sm leading-6 text-[var(--jag-color-muted)]">{safeCard.subtitle}</p>
          <p className="mt-3 max-w-3xl text-sm leading-7 text-[var(--jag-color-muted)]">
            {safeCard.description}
          </p>
        </div>

        <div className="w-full rounded-2xl bg-[var(--jag-color-audio)] p-4 text-white lg:w-72">
          <div className="flex min-w-0 items-center gap-3 text-sm font-bold">
            <span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-blue-500">▶</span>
            语音讲解占位 · 未接入真实 TTS
          </div>
          <div className="mt-4 h-2 overflow-hidden rounded-full bg-white/15">
            <div className="h-full w-2/5 rounded-full bg-blue-400" />
          </div>
          <p className="mt-3 text-xs leading-5 text-white/65">
            {safeCard.audio?.text ?? "audio 字段已预留，后续可接入音频 URL。"}
          </p>
        </div>
      </div>

      <section className="jag-panel mt-6">
        <h3 className="text-sm font-black text-[var(--jag-color-ink)]">故事讲解</h3>
        <p className="mt-2 text-sm leading-7 text-[var(--jag-color-muted)]">{safeCard.story}</p>
      </section>

      <div className="mt-4 grid gap-4 lg:grid-cols-3">
        <ListPanel title="附近推荐" empty="暂无附近推荐。" items={nearby.map((item) => `${item.name}${item.distance_text ? ` · ${item.distance_text}` : ""}`)} />
        <ListPanel title="美食推荐" empty="暂无美食推荐。" items={foods.map((item) => `${item.name}${item.area ? ` · ${item.area}` : ""}`)} />
        <ListPanel title="住宿建议" empty="暂无住宿建议。" items={hotels.map((item) => `${item.name}${item.area ? ` · ${item.area}` : ""}`)} />
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
        <div className="mt-4 rounded-2xl border border-dashed border-blue-200 bg-blue-50 p-3 text-xs font-bold leading-5 text-blue-800">
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

      <div className="mt-4 text-xs font-semibold leading-5 text-[var(--jag-color-muted)]">
        metadata: {safeCard.metadata?.mock ? "mock" : "live"} · sources: {(safeCard.metadata?.sources ?? []).join(", ")}
      </div>
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
