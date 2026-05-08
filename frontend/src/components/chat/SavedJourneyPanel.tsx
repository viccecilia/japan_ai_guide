import type { SavedJourneyListItem } from "../../lib/journey-api";

export function SavedJourneyPanel({
  journeys,
  isLoading,
  onRestore,
  onDelete,
}: {
  journeys: SavedJourneyListItem[];
  isLoading: boolean;
  onRestore: (journeyId: string) => void;
  onDelete: (journeyId: string) => void;
}) {
  return (
    <section className="mt-4 rounded-2xl border border-slate-200 bg-slate-50 p-4">
      <div className="flex items-center justify-between gap-3">
        <div>
          <h4 className="text-sm font-black text-[var(--jag-color-ink)]">已保存路线</h4>
          <p className="mt-1 text-xs leading-5 text-[var(--jag-color-muted)]">
            保存后可以从这里恢复继续编辑。本轮仍是内存存储。
          </p>
        </div>
        {isLoading ? <span className="text-xs font-bold text-blue-700">同步中</span> : null}
      </div>

      {journeys.length === 0 ? (
        <p className="mt-3 text-xs font-bold text-[var(--jag-color-muted)]">还没有保存的路线。</p>
      ) : (
        <div className="mt-3 grid gap-2">
          {journeys.map((journey) => (
            <article key={journey.journey_id} className="rounded-2xl bg-white p-3 shadow-[var(--jag-shadow-sm)]">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <div className="min-w-0">
                  <div className="truncate text-sm font-black text-[var(--jag-color-ink)]">{journey.title}</div>
                  <div className="mt-1 flex flex-wrap gap-2 text-xs font-bold text-[var(--jag-color-muted)]">
                    <span>{journey.city ?? "日本"}</span>
                    <span>{personaLabel(journey.persona)}</span>
                    <span>{paceLabel(journey.pace)}</span>
                    <span>{formatDate(journey.updated_at)}</span>
                  </div>
                </div>
                <div className="flex shrink-0 gap-2">
                  <button className="jag-button-secondary px-3 py-1.5 text-xs" type="button" onClick={() => onRestore(journey.journey_id)}>
                    恢复
                  </button>
                  <button className="jag-button-secondary px-3 py-1.5 text-xs" type="button" onClick={() => onDelete(journey.journey_id)}>
                    删除
                  </button>
                </div>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}

function personaLabel(persona?: string | null) {
  const labels: Record<string, string> = {
    first_time: "第一次",
    family: "亲子",
    couple: "情侣",
    elder: "老人",
    foodie: "美食",
  };
  return persona ? labels[persona] ?? persona : "未设置";
}

function paceLabel(pace?: string | null) {
  const labels: Record<string, string> = { slow: "慢", normal: "标准", dense: "紧凑" };
  return pace ? labels[pace] ?? pace : "标准";
}

function formatDate(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "刚刚";
  return date.toLocaleString("zh-CN", { month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" });
}
