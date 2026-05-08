import type { TravelMemorySnapshot } from "../../../types/answer-card";

export function TravelPreferenceCard({ memory }: { memory?: TravelMemorySnapshot | null }) {
  if (!memory) return null;
  const preference = memory.preference;
  return (
    <div className="rounded-2xl border border-violet-100 bg-violet-50 p-4 text-violet-950">
      <p className="text-xs font-black uppercase tracking-[0.12em] text-violet-600">Travel Memory</p>
      <h4 className="mt-1 text-base font-black">AI 旅行偏好</h4>
      <p className="mt-1 text-sm leading-6">{memory.summary}</p>
      <div className="mt-3 grid gap-2 sm:grid-cols-3">
        <MemoryPill label="节奏" value={paceLabel(preference.preferred_pace)} />
        <MemoryPill label="风格" value={personaLabel(preference.preferred_persona)} />
        <MemoryPill label="步行" value={toleranceLabel(preference.walking_tolerance)} />
      </div>
      {memory.evolution.length > 0 ? (
        <p className="mt-3 rounded-xl bg-white/75 p-3 text-sm font-semibold text-violet-800">
          AI 已根据最近的路线选择更新偏好：{memory.evolution[memory.evolution.length - 1]?.field}
        </p>
      ) : null}
    </div>
  );
}

function MemoryPill({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl bg-white/80 px-3 py-2">
      <div className="text-xs font-black text-violet-500">{label}</div>
      <div className="text-sm font-black text-violet-950">{value}</div>
    </div>
  );
}

function paceLabel(value: string) {
  return { slow: "慢节奏", normal: "均衡", dense: "充实" }[value] ?? "均衡";
}

function personaLabel(value: string) {
  return {
    first_time: "首次日本",
    culture: "文化路线",
    foodie: "美食路线",
    elder: "少步行",
    family: "亲子",
    couple: "情侣",
  }[value] ?? "旅行路线";
}

function toleranceLabel(value: string) {
  return { low: "少走路", medium: "适中", high: "可多走" }[value] ?? "适中";
}
