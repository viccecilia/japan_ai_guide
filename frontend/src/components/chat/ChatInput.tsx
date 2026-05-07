"use client";

type ChatInputProps = {
  value: string;
  isLoading: boolean;
  onChange: (value: string) => void;
  onSubmit: () => void;
};

export function ChatInput({ value, isLoading, onChange, onSubmit }: ChatInputProps) {
  return (
    <div className="border-t border-[var(--jag-color-line)] bg-white/90 p-3 backdrop-blur sm:p-4">
      <div className="jag-input-shell">
        <label className="sr-only" htmlFor="jag-question">
          旅行问题输入
        </label>
        <textarea
          id="jag-question"
          data-testid="chat-input"
          className="max-h-40 min-h-14 flex-1 resize-none border-0 bg-transparent px-3 py-3 text-base leading-6 text-[var(--jag-color-ink)] outline-none placeholder:text-slate-400 disabled:opacity-70"
          placeholder="问我任何日本旅行问题，例如：清水寺、京都半日路线、交通和美食..."
          rows={1}
          value={value}
          disabled={isLoading}
          onChange={(event) => onChange(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              onSubmit();
            }
          }}
        />
        <button
          data-testid="send-button"
          className="jag-button-primary shrink-0 rounded-2xl px-5 py-3 disabled:cursor-not-allowed disabled:opacity-60"
          type="button"
          disabled={isLoading}
          onClick={onSubmit}
        >
          {isLoading ? "请求中" : "发送"}
        </button>
      </div>
      <div className="mx-auto mt-2 max-w-4xl px-1 text-xs font-semibold text-[var(--jag-color-muted)]">
        Enter 发送，Shift + Enter 换行
      </div>
    </div>
  );
}
