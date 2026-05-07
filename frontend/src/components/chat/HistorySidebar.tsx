import type { AnswerCard } from "../../../types/answer-card";

export type ChatHistoryItem = {
  id: string;
  question: string;
  card: AnswerCard | null;
  status: "loading" | "streaming" | "success" | "error";
  error?: string;
};

type HistorySidebarProps = {
  items: ChatHistoryItem[];
  activeId: string | null;
  onSelect: (id: string) => void;
  onNew: () => void;
};

export function HistorySidebar({ items, activeId, onSelect, onNew }: HistorySidebarProps) {
  return (
    <aside className="jag-sidebar">
      <div className="mb-7 flex items-center justify-between gap-3">
        <div className="min-w-0">
          <div className="truncate text-base font-black text-[var(--jag-color-ink)]">
            Japan AI Guide
          </div>
          <div className="mt-1 text-xs font-semibold text-[var(--jag-color-muted)]">
            当前会话历史
          </div>
        </div>
        <button
          className="jag-button-secondary shrink-0 px-3 py-2 text-sm text-blue-700"
          type="button"
          onClick={onNew}
        >
          新对话
        </button>
      </div>

      <div className="mb-3 text-xs font-black uppercase tracking-wide text-[var(--jag-color-muted)]">
        历史记录 · {items.length}
      </div>

      <div className="min-h-0 flex-1 space-y-3 overflow-y-auto pr-1">
        {items.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-[var(--jag-color-line)] bg-white/70 p-4 text-sm leading-6 text-[var(--jag-color-muted)]">
            连续提问后，当前会话的记录会保存在这里。点击记录可恢复对应回答。
          </div>
        ) : null}
        {items.map((item) => (
          <button
            key={item.id}
            className={`w-full rounded-2xl border bg-white p-4 text-left shadow-[var(--jag-shadow-sm)] transition hover:border-blue-200 hover:bg-blue-50 ${
              item.id === activeId ? "border-blue-300 bg-blue-50" : "border-[var(--jag-color-line)]"
            }`}
            type="button"
            onClick={() => onSelect(item.id)}
          >
            <div className="line-clamp-2 font-bold text-[var(--jag-color-ink)]">{item.question}</div>
            <div className="mt-1 text-sm leading-6 text-[var(--jag-color-muted)]">
              {getSummary(item)}
            </div>
          </button>
        ))}
      </div>

      <div className="jag-panel mt-5">
        <div className="text-sm font-black text-[var(--jag-color-ink)]">Mock 状态</div>
        <p className="mt-2 text-sm leading-6 text-[var(--jag-color-muted)]">
          历史只保存在当前浏览器会话内，刷新页面后会清空；本轮不接数据库。
        </p>
      </div>
    </aside>
  );
}

function getSummary(item: ChatHistoryItem) {
  if (item.status === "loading") return "正在请求后端 Mock API";
  if (item.status === "streaming") return "正在生成 streaming mock";
  if (item.status === "error") return item.error ?? "请求失败";
  return item.card?.title ?? "已返回 AnswerCard";
}
