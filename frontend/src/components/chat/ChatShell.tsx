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

const STREAM_TEXT = "我正在整理景点背景、路线建议和适合继续探索的方向...";

export function ChatShell() {
  const [prompt, setPrompt] = useState("");
  const [turns, setTurns] = useState<ChatTurn[]>([]);
  const [activeTurnId, setActiveTurnId] = useState<string | null>(null);
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
          error: error instanceof Error ? error.message : "请求失败，请检查后端服务是否正在运行。",
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

          <div className="min-h-0 min-w-0 flex-1 overflow-y-auto overflow-x-hidden px-4 pb-6 pt-4 sm:px-8 sm:pt-6">
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
                  <ErrorCard message={activeTurn.error ?? "请求失败，请检查后端服务是否正在运行。"} />
                ) : null}
                {activeTurn.status === "success" && activeTurn.response ? (
                  <MultiCardResponseView response={activeTurn.response} onPromptSelect={(question) => void runQuery(question)} />
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
        像问导游一样计划日本旅行
      </h1>
      <p className="mx-auto mt-4 max-w-2xl text-base leading-7 text-[var(--jag-color-muted)]">
        直接输入城市、景点、路线、美食或文化问题。我会先给你一版清晰回答，再推荐适合继续探索的方向。
      </p>
      <QuickQuestionButtons isLoading={isLoading} onSelect={onSelect} />
      <div className="mt-6 grid w-full gap-3 text-left sm:grid-cols-3">
        <WelcomeHint title="导游式回答" body="先讲重点，再补背景、路线和下一步建议。" />
        <WelcomeHint title="可连续追问" body="当前会话会保存历史，点击左侧记录可以恢复回答。" />
        <WelcomeHint title="仍是 Mock 阶段" body="本阶段不接真实 AI、数据库、地图或商业推荐。" />
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
        正在整理导览建议
      </div>
      <p className="mt-2 text-sm leading-6">我会先给出主回答，再补充相关推荐。</p>
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
        请确认后端服务正在 `http://127.0.0.1:8010` 运行，然后再试一次。
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
