import type { TimelineConstraint } from "../../../types/answer-card";

const badgeCopy: Record<string, { label: string; tone: string }> = {
  easy: { label: "轻松路线", tone: "bg-emerald-50 text-emerald-700 border-emerald-100" },
  balanced: { label: "节奏均衡", tone: "bg-blue-50 text-blue-700 border-blue-100" },
  tight: { label: "行程偏紧", tone: "bg-amber-50 text-amber-700 border-amber-100" },
  overloaded: { label: "建议减负", tone: "bg-rose-50 text-rose-700 border-rose-100" },
};

export function TimelineConstraintBadge({ constraint }: { constraint?: TimelineConstraint | null }) {
  if (!constraint) return null;
  const copy = badgeCopy[constraint.timeline_feasibility] ?? badgeCopy.balanced;
  return (
    <div className={`rounded-2xl border px-4 py-3 ${copy.tone}`}>
      <div className="text-sm font-black">{copy.label}</div>
      <p className="mt-1 text-sm leading-6">{constraint.feasibility_reason}</p>
      <div className="mt-2 flex flex-wrap gap-2 text-xs font-bold">
        <span>步行：{loadLabel(constraint.walking_load)}</span>
        <span>跨城：{loadLabel(constraint.transition_load)}</span>
        <span>疲劳：{loadLabel(constraint.estimated_fatigue)}</span>
      </div>
    </div>
  );
}

function loadLabel(level?: string) {
  return {
    easy: "轻松",
    normal: "正常",
    tight: "偏紧",
    overload: "过载",
    overloaded: "过载",
  }[level ?? "normal"] ?? "正常";
}
