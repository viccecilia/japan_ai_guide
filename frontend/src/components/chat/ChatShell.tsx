"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { queryChat } from "../../../services/chat-api";
import type { MultiCardResponse } from "../../../types/answer-card";
import { ChatInput } from "./ChatInput";
import { ChatHistoryItem, HistorySidebar } from "./HistorySidebar";
import { LanguageSelector } from "./LanguageSelector";
import { MultiCardResponseView } from "./MultiCardResponseView";
import { QuickQuestionButtons } from "./QuickQuestionButtons";

type ChatTurn = ChatHistoryItem & {
  streamText: string;
  createdAt: number;
  response: MultiCardResponse | null;
};

const STREAM_TEXT = "正在整理景点背景、参观建议和旅行提示...";

export function ChatShell() {
  const [prompt, setPrompt] = useState("");
  const [turns, setTurns] = useState<ChatTurn[]>([]);
  const [activeTurnId, setActiveTurnId] = useState<string | null>(null);
  const scrollAreaRef = useRef<HTMLDivElement | null>(null);
  const bottomRef = useRef<HTMLDivElement | null>(null);

  const activeTurn = useMemo(
    () => turns.find((turn) => turn.id === activeTurnId) ?? null,
    [activeTurnId, turns],
  );

  const isBusy = activeTurn?.status === "loading" || activeTurn?.status === "streaming";

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [turns, activeTurnId, activeTurn?.streamText, activeTurn?.status]);

  function startNewChat() {
    setPrompt("");
    setActiveTurnId(null);
  }

  function restoreTurn(id: string) {
    const selected = turns.find((turn) => turn.id === id);
    if (!selected) return;
    setActiveTurnId(id);
    setPrompt(selected.question);
  }

  async function runQuery(question: string) {
    const nextQuestion = question.trim();
    if (!nextQuestion || isBusy) return;

    const turnId = createTurnId();
    const draft: ChatTurn = {
      id: turnId,
      question: nextQuestion,
      card: null,
      response: null,
      status: "loading",
      streamText: "",
      createdAt: Date.now(),
    };

    setPrompt(nextQuestion);
    setActiveTurnId(turnId);
    setTurns((current) => [draft, ...current]);

    try {
      const [response] = await Promise.all([queryChat(nextQuestion), delay(500)]);
      setTurns((current) =>
        updateTurn(current, turnId, {
          status: "streaming",
          card: response?.main_card ?? null,
          response,
          streamText: "",
        }),
      );
      await playStreamingMock(turnId);
      setTurns((current) =>
        updateTurn(current, turnId, {
          status: "success",
          streamText: STREAM_TEXT,
        }),
      );
    } catch (error) {
      setTurns((current) =>
        updateTurn(current, turnId, {
          status: "error",
          card: null,
          response: null,
          streamText: "",
          error: error instanceof Error ? error.message : "请求失败，请检查后端服务。",
        }),
      );
    }
  }

  async function playStreamingMock(turnId: string) {
    for (let index = 1; index <= STREAM_TEXT.length; index += 1) {
      await delay(18);
      setTurns((current) =>
        updateTurn(current, turnId, {
          streamText: STREAM_TEXT.slice(0, index),
        }),
      );
    }
  }

  return (
    <main className="jag-page">
      <div className="flex h-screen min-h-0 min-w-0">
        <HistorySidebar
          items={turns}
          activeId={activeTurnId}
          onSelect={restoreTurn}
          onNew={startNewChat}
        />

        <section className="flex min-h-0 min-w-0 flex-1 flex-col overflow-x-hidden">
          <header className="flex h-16 min-w-0 shrink-0 items-center justify-between gap-3 border-b border-transparent px-4 sm:px-8">
            <button className="jag-button-compact lg:hidden" type="button" onClick={startNewChat}>
              新对话
            </button>
            <LanguageSelector />
          </header>

          <div ref={scrollAreaRef} className="min-h-0 min-w-0 flex-1 overflow-y-auto overflow-x-hidden px-4 pb-6 pt-4 sm:px-8 sm:pt-6">
            <MobileHistoryStrip
              items={turns}
              activeId={activeTurnId}
              onSelect={restoreTurn}
            />

            {!activeTurn ? (
              <WelcomePanel isLoading={isBusy} onSelect={(question) => void runQuery(question)} />
            ) : (
              <section className="mx-auto w-full max-w-4xl">
                <div className="mb-4 flex justify-end">
                  <div className="max-w-[86%] whitespace-pre-wrap break-words rounded-[18px] rounded-br-md bg-[var(--jag-color-primary)] px-4 py-3 text-left text-sm font-bold leading-6 text-white shadow-[var(--jag-shadow-primary)]">
                    {activeTurn.question}
                  </div>
                </div>

                {activeTurn.status === "loading" ? <LoadingCard /> : null}
                {activeTurn.status === "streaming" ? <StreamingCard text={activeTurn.streamText} /> : null}
                {activeTurn.status === "error" ? (
                  <ErrorCard message={activeTurn.error ?? "请求失败，请检查后端服务。"} />
                ) : null}
                {activeTurn.status === "success" && activeTurn.response ? (
                  <MultiCardResponseView response={activeTurn.response} />
                ) : null}
              </section>
            )}

            <div ref={bottomRef} />
          </div>

          <ChatInput
            value={prompt}
            isLoading={isBusy}
            onChange={setPrompt}
            onSubmit={() => void runQuery(prompt)}
          />
        </section>
      </div>
    </main>
  );
}

function WelcomePanel({
  isLoading,
  onSelect,
}: {
  isLoading: boolean;
  onSelect: (question: string) => void;
}) {
  return (
    <section className="mx-auto flex min-h-[calc(100vh-12rem)] w-full max-w-4xl flex-col items-center justify-center text-center">
      <div className="mb-6 inline-flex items-center gap-3 rounded-full border border-[var(--jag-color-line)] bg-white px-5 py-3 shadow-[var(--jag-shadow-md)]">
        <span className="grid h-9 w-9 place-items-center rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 text-sm font-black text-white">
          AI
        </span>
        <span className="font-black">Japan AI Guide</span>
      </div>
      <h1 className="max-w-2xl text-4xl font-black tracking-normal text-[var(--jag-color-ink)] sm:text-5xl">
        像 ChatGPT 一样问日本旅行
      </h1>
      <p className="mx-auto mt-4 max-w-2xl text-base leading-7 text-[var(--jag-color-muted)]">
        输入景点、文化、美食或路线问题。当前版本会调用本地 FastAPI，并返回 Mock AnswerCard。
      </p>
      <QuickQuestionButtons isLoading={isLoading} onSelect={onSelect} />
      <div className="mt-6 grid w-full gap-3 text-left sm:grid-cols-3">
        <WelcomeHint title="当前会话历史" body="连续提问会保存到左侧历史栏，点击即可恢复对应回答。" />
        <WelcomeHint title="键盘输入" body="Enter 发送，Shift + Enter 保留换行，体验接近聊天工具。" />
        <WelcomeHint title="Mock Streaming" body="请求成功后先展示短文本流式效果，再渲染最终卡片。" />
      </div>
    </section>
  );
}

function MobileHistoryStrip({
  items,
  activeId,
  onSelect,
}: {
  items: ChatHistoryItem[];
  activeId: string | null;
  onSelect: (id: string) => void;
}) {
  if (items.length === 0) return null;
  return (
    <div className="mx-auto mb-4 flex w-full max-w-4xl gap-2 overflow-x-auto pb-2 lg:hidden">
      {items.map((item) => (
        <button
          key={item.id}
          className={`shrink-0 rounded-full border px-3 py-2 text-xs font-bold ${
            item.id === activeId
              ? "border-blue-300 bg-blue-50 text-blue-700"
              : "border-[var(--jag-color-line)] bg-white text-[var(--jag-color-muted)]"
          }`}
          type="button"
          onClick={() => onSelect(item.id)}
        >
          {item.question}
        </button>
      ))}
    </div>
  );
}

function WelcomeHint({ title, body }: { title: string; body: string }) {
  return (
    <div className="rounded-2xl border border-[var(--jag-color-line)] bg-white/85 p-4 shadow-[var(--jag-shadow-sm)]">
      <div className="text-sm font-black text-[var(--jag-color-ink)]">{title}</div>
      <p className="mt-2 text-sm leading-6 text-[var(--jag-color-muted)]">{body}</p>
    </div>
  );
}

function LoadingCard() {
  return (
    <div className="rounded-2xl border border-blue-100 bg-blue-50 p-5 text-blue-800 shadow-[var(--jag-shadow-sm)]">
      <div className="flex items-center gap-3 text-sm font-black">
        <span className="flex gap-1">
          <span className="h-2 w-2 animate-bounce rounded-full bg-blue-500" />
          <span className="h-2 w-2 animate-bounce rounded-full bg-blue-500 [animation-delay:120ms]" />
          <span className="h-2 w-2 animate-bounce rounded-full bg-blue-500 [animation-delay:240ms]" />
        </span>
        正在请求后端 Mock API
      </div>
      <p className="mt-2 text-sm leading-6">正在等待 AnswerCard 数据返回。</p>
    </div>
  );
}

function StreamingCard({ text }: { text: string }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-[var(--jag-shadow-sm)]">
      <div className="text-sm font-black text-[var(--jag-color-ink)]">Japan AI Guide</div>
      <p className="mt-3 min-h-7 text-sm leading-7 text-[var(--jag-color-muted)]">
        {text}
        <span className="ml-1 inline-block h-4 w-1 animate-pulse rounded bg-blue-500 align-middle" />
      </p>
    </div>
  );
}

function ErrorCard({ message }: { message: string }) {
  return (
    <div className="rounded-2xl border border-red-200 bg-red-50 p-5 text-red-800 shadow-[var(--jag-shadow-sm)]">
      <div className="text-sm font-black">请求失败</div>
      <p className="mt-2 text-sm leading-6">{message}</p>
      <p className="mt-3 text-xs font-semibold leading-5 text-red-700">
        请确认后端 `http://127.0.0.1:8000` 正在运行；本提示是前端错误态占位，不包含真实业务兜底。
      </p>
    </div>
  );
}

function updateTurn(turns: ChatTurn[], id: string, patch: Partial<ChatTurn>) {
  return turns.map((turn) => (turn.id === id ? { ...turn, ...patch } : turn));
}

function createTurnId() {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function delay(ms: number) {
  return new Promise((resolve) => {
    window.setTimeout(resolve, ms);
  });
}
