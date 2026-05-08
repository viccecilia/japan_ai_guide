import type { TravelContext } from "../../../types/answer-card";

export function TravelContextCard({
  context,
  onApplyContext,
}: {
  context?: TravelContext | null;
  onApplyContext: () => void;
}) {
  if (!context || context.suggestions.length === 0) return null;

  return (
    <div className="rounded-2xl border border-sky-100 bg-sky-50 p-4 text-sky-950">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-xs font-black uppercase tracking-[0.12em] text-sky-600">Live Context</p>
          <h4 className="mt-1 text-base font-black">今日旅行状态</h4>
          <p className="mt-1 text-sm leading-6">{context.narrative}</p>
        </div>
        {context.context_optimized_timeline ? (
          <button
            type="button"
            onClick={onApplyContext}
            className="rounded-full bg-sky-700 px-4 py-2 text-sm font-black text-white hover:bg-sky-800"
          >
            根据当前状态优化
          </button>
        ) : null}
      </div>

      <div className="mt-3 grid gap-2 sm:grid-cols-3">
        <StatusPill label="天气" value={weatherLabel(context.weather.condition)} />
        <StatusPill label="时间" value={timeLabel(context.time.time_of_day)} />
        <StatusPill label="疲劳" value={loadLabel(context.fatigue.travel_fatigue)} />
      </div>

      <div className="mt-3 grid gap-2">
        {context.suggestions.slice(0, 3).map((suggestion) => (
          <div key={`${suggestion.suggestion_type}-${suggestion.title}`} className="rounded-xl bg-white/80 p-3">
            <div className="text-sm font-black">{suggestion.title}</div>
            <p className="mt-1 text-sm leading-6 text-sky-800">{suggestion.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function StatusPill({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl bg-white/80 px-3 py-2">
      <div className="text-xs font-black text-sky-500">{label}</div>
      <div className="text-sm font-black text-sky-950">{value}</div>
    </div>
  );
}

function weatherLabel(value: string) {
  return {
    sunny: "稳定",
    rainy: "雨天",
    hot: "偏热",
    crowded: "拥挤",
  }[value] ?? "稳定";
}

function timeLabel(value: string) {
  return {
    morning: "上午",
    afternoon: "下午",
    evening: "晚上",
    late: "偏晚",
  }[value] ?? "当前";
}

function loadLabel(value: string) {
  return {
    easy: "轻松",
    normal: "正常",
    high: "偏累",
    overload: "过载",
  }[value] ?? "正常";
}
