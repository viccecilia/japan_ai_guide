import type { AdaptiveJourney } from "../../../types/answer-card";

export function AdaptiveSuggestionCard({
  adaptiveJourney,
  onOptimize,
}: {
  adaptiveJourney?: AdaptiveJourney | null;
  onOptimize: () => void;
}) {
  if (!adaptiveJourney || adaptiveJourney.suggestions.length === 0) return null;

  return (
    <div className="rounded-2xl border border-emerald-100 bg-emerald-50 p-4 text-emerald-950">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-xs font-black uppercase tracking-[0.12em] text-emerald-600">Smart Optimize</p>
          <h4 className="mt-1 text-base font-black">自动优化建议</h4>
          <p className="mt-1 text-sm leading-6">{adaptiveJourney.narrative}</p>
        </div>
        {adaptiveJourney.optimized_timeline ? (
          <button
            type="button"
            onClick={onOptimize}
            className="rounded-full bg-emerald-700 px-4 py-2 text-sm font-black text-white hover:bg-emerald-800"
          >
            智能优化路线
          </button>
        ) : null}
      </div>
      <div className="mt-3 grid gap-2">
        {adaptiveJourney.suggestions.slice(0, 3).map((suggestion) => (
          <div key={`${suggestion.adaptation_type}-${suggestion.title}`} className="rounded-xl bg-white/75 p-3">
            <div className="text-sm font-black">{suggestion.title}</div>
            <p className="mt-1 text-sm leading-6 text-emerald-800">{suggestion.description}</p>
          </div>
        ))}
      </div>
      {adaptiveJourney.applied ? (
        <div className="mt-3 flex flex-wrap gap-2 text-xs font-black text-emerald-700">
          <span>{labelFor(adaptiveJourney.before_feasibility)} → {labelFor(adaptiveJourney.after_feasibility)}</span>
          <span>疲劳：{adaptiveJourney.fatigue_reduction === "reduced" ? "已降低" : "已稳定"}</span>
          <span>跨城减少：{adaptiveJourney.transition_reduction}</span>
        </div>
      ) : null}
    </div>
  );
}

function labelFor(value: string) {
  return {
    easy: "轻松",
    balanced: "均衡",
    tight: "偏紧",
    overloaded: "过载",
  }[value] ?? value;
}
