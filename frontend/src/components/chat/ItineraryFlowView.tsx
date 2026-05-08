"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import type { Itinerary, ItineraryStop } from "../../../types/answer-card";
import {
  createJourney,
  deleteSavedJourney,
  type EditableJourneyResponse,
  listSavedJourneys,
  regenerateJourney as regenerateJourneyRequest,
  removeJourneyStop,
  replaceJourneyStop,
  restoreSavedJourney,
  type SavedJourneyListItem,
  saveJourney,
  switchJourneyPace,
  switchJourneyPersona,
} from "../../lib/journey-api";
import { PersonaBadge } from "./PersonaBadge";
import { SavedJourneyPanel } from "./SavedJourneyPanel";

const personaOptions = [
  { value: "first_time", label: "第一次" },
  { value: "family", label: "亲子" },
  { value: "couple", label: "情侣" },
  { value: "elder", label: "老人" },
  { value: "foodie", label: "美食" },
];

const paceOptions = [
  { value: "slow", label: "慢" },
  { value: "normal", label: "标准" },
  { value: "dense", label: "紧凑" },
];

const replacementPool = ["金阁寺", "岚山", "祗园", "黑门市场", "梅田蓝天大厦"];

export function ItineraryFlowView({ itineraries }: { itineraries: Itinerary[] }) {
  if (itineraries.length === 0) return null;

  return (
    <div className="grid gap-4">
      {itineraries.map((itinerary) => (
        <EditableItineraryCard key={`${itinerary.title}-${itinerary.route_type}`} itinerary={itinerary} />
      ))}
    </div>
  );
}

function EditableItineraryCard({ itinerary }: { itinerary: Itinerary }) {
  const sessionId = useMemo(() => `jag-journey-${stableId(itinerary.title)}`, [itinerary.title]);
  const [persona, setPersona] = useState(itinerary.persona ?? "first_time");
  const [pace, setPace] = useState(itinerary.pace ?? "normal");
  const [stops, setStops] = useState<ItineraryStop[]>(itinerary.stops);
  const [history, setHistory] = useState<string[]>([]);
  const [savedJourneys, setSavedJourneys] = useState<SavedJourneyListItem[]>([]);
  const [isSyncing, setIsSyncing] = useState(false);
  const [apiNotice, setApiNotice] = useState<string | null>(null);
  const activeStops = useMemo(() => applyPace(stops, pace), [stops, pace]);
  const title = titleFor(itinerary, persona, pace);
  const narrative = narrativeFor(title, persona, pace, history[0] ?? itinerary.narrative);

  const applyJourneyResponse = useCallback((response: EditableJourneyResponse) => {
    const editable = response.editable_itinerary;
    if (!editable) return;
    const nextItinerary = editable.itinerary;
    setPersona(editable.current_persona ?? nextItinerary.persona ?? "first_time");
    setPace(editable.current_pace ?? nextItinerary.pace ?? "normal");
    setStops(editable.active_stops.length > 0 ? editable.active_stops : nextItinerary.stops);
    setHistory(response.interaction_history.map((item) => item.narrative).reverse().slice(0, 5));
  }, []);

  const refreshSavedJourneys = useCallback(async () => {
    try {
      setSavedJourneys(await listSavedJourneys());
    } catch {
      setApiNotice("暂时无法读取已保存路线。");
    }
  }, []);

  useEffect(() => {
    let isMounted = true;
    createJourney(sessionId, itinerary)
      .then((response) => {
        if (!isMounted) return;
        applyJourneyResponse(response);
        setApiNotice("已同步到后端 Journey Session");
        void refreshSavedJourneys();
      })
      .catch(() => {
        if (isMounted) setApiNotice("后端暂不可用，已保留本地编辑。");
      });
    return () => {
      isMounted = false;
    };
  }, [applyJourneyResponse, itinerary, refreshSavedJourneys, sessionId]);

  async function runApiAction(action: () => Promise<EditableJourneyResponse>, fallbackNotice = "后端暂不可用，已保留本地编辑。") {
    setIsSyncing(true);
    try {
      const response = await action();
      applyJourneyResponse(response);
      setApiNotice("已同步到后端 Journey Session");
      return response;
    } catch {
      setApiNotice(fallbackNotice);
      return null;
    } finally {
      setIsSyncing(false);
    }
  }

  function appendHistory(message: string) {
    setHistory((current) => [message, ...current].slice(0, 5));
  }

  function handlePersona(nextPersona: string) {
    setPersona(nextPersona);
    appendHistory(`已调整为${personaLabel(nextPersona)}的路线。`);
    void runApiAction(() => switchJourneyPersona(sessionId, nextPersona));
  }

  function handlePace(nextPace: string) {
    setPace(nextPace);
    appendHistory(`已切换为${paceLabel(nextPace)}，路线节奏已重新整理。`);
    void runApiAction(() => switchJourneyPace(sessionId, nextPace));
  }

  function removeStop(titleToRemove: string) {
    setStops((current) => current.filter((stop) => stop.title !== titleToRemove));
    appendHistory(`已移除 ${titleToRemove}，路线会更轻松一些。`);
    void runApiAction(() => removeJourneyStop(sessionId, titleToRemove));
  }

  function replaceStop(titleToReplace: string) {
    const replacement = replacementPool.find((item) => !stops.some((stop) => stop.title === item)) ?? "替代景点";
    setStops((current) =>
      current.map((stop) =>
        stop.title === titleToReplace
          ? { ...stop, title: replacement, narrative: `这里替换成${replacement}，让路线保持新鲜感。` }
          : stop,
      ),
    );
    appendHistory(`已将 ${titleToReplace} 替换为 ${replacement}。`);
    void runApiAction(() => replaceJourneyStop(sessionId, titleToReplace));
  }

  function regenerateJourney() {
    const nextPace = pace === "slow" ? "normal" : "slow";
    setPace(nextPace);
    appendHistory(nextPace === "slow" ? "已重新生成更轻松的路线。" : "已重新生成更均衡的路线。");
    void runApiAction(() => regenerateJourneyRequest(sessionId, nextPace === "slow" ? "更轻松一点" : "更均衡一点"));
  }

  async function handleSave() {
    setIsSyncing(true);
    try {
      await saveJourney(sessionId, title);
      setApiNotice("路线已保存，可以稍后从下方恢复。");
      await refreshSavedJourneys();
    } catch {
      setApiNotice("保存失败：当前只支持后端内存会话。");
    } finally {
      setIsSyncing(false);
    }
  }

  async function handleRestore(journeyId: string) {
    setIsSyncing(true);
    try {
      const restored = await restoreSavedJourney(journeyId);
      const editable = restored.saved_journey.editable_itinerary;
      if (editable) {
        applyJourneyResponse({
          journey_state: { session_id: restored.restored_session_id, persona: editable.current_persona, pace: editable.current_pace },
          editable_itinerary: editable,
          interaction_history: restored.saved_journey.interaction_history,
          analytics: restored.saved_journey.analytics,
          replay: restored.replay,
        });
      }
      setApiNotice("已恢复保存的路线。");
      await refreshSavedJourneys();
    } catch {
      setApiNotice("恢复失败：保存记录可能已不存在。");
    } finally {
      setIsSyncing(false);
    }
  }

  async function handleDelete(journeyId: string) {
    setIsSyncing(true);
    try {
      await deleteSavedJourney(journeyId);
      setApiNotice("已删除保存的路线。");
      await refreshSavedJourneys();
    } catch {
      setApiNotice("删除失败：保存记录可能已不存在。");
    } finally {
      setIsSyncing(false);
    }
  }

  return (
    <article className="rounded-2xl border border-blue-100 bg-white p-4 shadow-[var(--jag-shadow-lg)] sm:p-5">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <div className="text-xs font-black uppercase tracking-normal text-blue-600">Travel Flow</div>
          <h3 className="mt-1 text-xl font-black leading-tight text-[var(--jag-color-ink)]">{title}</h3>
          <p className="mt-2 text-sm leading-6 text-[var(--jag-color-muted)]">{narrative}</p>
          <div className="mt-3">
            <PersonaBadge label={personaLabel(persona)} pace={pace} />
          </div>
        </div>
        <div className="flex shrink-0 flex-wrap gap-2 text-xs font-black text-blue-700">
          <span className="rounded-full bg-blue-50 px-3 py-1">{durationLabel(itinerary.duration)}</span>
          <span className="rounded-full bg-emerald-50 px-3 py-1 text-emerald-700">{routeTypeLabel(persona)}</span>
          <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-700">{timeLabel(pace)}</span>
        </div>
      </div>

      <JourneyControls
        persona={persona}
        pace={pace}
        isSyncing={isSyncing}
        onPersona={handlePersona}
        onPace={handlePace}
        onRegenerate={regenerateJourney}
        onSave={() => void handleSave()}
      />

      <section className="mt-5 rounded-2xl bg-slate-50 p-4">
        <div className="text-sm font-black text-[var(--jag-color-ink)]">上午 · 协同调整后的路线</div>
        <p className="mt-2 text-xs leading-5 text-[var(--jag-color-muted)]">
          当前停留点会按 persona 和 pace 做轻量调整，你可以继续移除、替换、保存或恢复。
        </p>
        <StopList stops={activeStops} onRemove={removeStop} onReplace={replaceStop} />
      </section>

      {history.length > 0 ? (
        <div className="mt-4 rounded-2xl bg-blue-50 px-4 py-3 text-xs font-bold leading-5 text-blue-800">
          <div className="mb-1 text-blue-900">协同调整记录</div>
          {history.map((item) => (
            <div key={item}>{item}</div>
          ))}
        </div>
      ) : null}

      <SavedJourneyPanel
        journeys={savedJourneys}
        isLoading={isSyncing}
        onRestore={(journeyId) => void handleRestore(journeyId)}
        onDelete={(journeyId) => void handleDelete(journeyId)}
      />

      {apiNotice ? (
        <p className="mt-3 rounded-2xl bg-emerald-50 px-4 py-3 text-xs font-bold leading-5 text-emerald-800">
          {apiNotice}
        </p>
      ) : null}

      <p className="mt-4 rounded-2xl bg-amber-50 px-4 py-3 text-xs font-bold leading-5 text-amber-800">
        当前保存层仍是后端内存协议；未接真实账号、PostgreSQL 或 Redis。
      </p>
    </article>
  );
}

function JourneyControls({
  persona,
  pace,
  isSyncing,
  onPersona,
  onPace,
  onRegenerate,
  onSave,
}: {
  persona: string;
  pace: string;
  isSyncing: boolean;
  onPersona: (persona: string) => void;
  onPace: (pace: string) => void;
  onRegenerate: () => void;
  onSave: () => void;
}) {
  return (
    <div className="mt-5 grid gap-3 rounded-2xl border border-slate-200 bg-slate-50 p-3">
      <div className="flex flex-wrap gap-2">
        {personaOptions.map((option) => (
          <button
            key={option.value}
            type="button"
            className={option.value === persona ? "jag-button-primary px-3 py-2 text-xs" : "jag-button-secondary px-3 py-2 text-xs"}
            disabled={isSyncing}
            onClick={() => onPersona(option.value)}
          >
            {option.label}
          </button>
        ))}
      </div>
      <div className="flex flex-wrap items-center gap-2">
        {paceOptions.map((option) => (
          <button
            key={option.value}
            type="button"
            className={option.value === pace ? "jag-button-primary px-3 py-2 text-xs" : "jag-button-secondary px-3 py-2 text-xs"}
            disabled={isSyncing}
            onClick={() => onPace(option.value)}
          >
            {option.label}
          </button>
        ))}
        <button type="button" className="jag-button-secondary px-3 py-2 text-xs" disabled={isSyncing} onClick={onRegenerate}>
          {isSyncing ? "同步中" : "重新生成"}
        </button>
        <button type="button" className="jag-button-primary px-3 py-2 text-xs" disabled={isSyncing} onClick={onSave}>
          保存路线
        </button>
      </div>
    </div>
  );
}

function StopList({
  stops,
  onRemove,
  onReplace,
}: {
  stops: ItineraryStop[];
  onRemove: (title: string) => void;
  onReplace: (title: string) => void;
}) {
  return (
    <ol className="mt-3 grid gap-3">
      {stops.map((stop, index) => (
        <li key={`${stop.title}-${index}`} className="flex gap-3 rounded-2xl bg-white p-3">
          <span className="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-blue-600 text-xs font-black text-white">
            {index + 1}
          </span>
          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <h4 className="break-words text-sm font-black text-[var(--jag-color-ink)]">{stop.title}</h4>
              {stop.estimated_time ? (
                <span className="rounded-full bg-slate-100 px-2 py-1 text-[11px] font-bold text-slate-600">
                  {stop.estimated_time}
                </span>
              ) : null}
            </div>
            {stop.subtitle ? <p className="mt-1 text-xs leading-5 text-[var(--jag-color-muted)]">{stop.subtitle}</p> : null}
            {stop.narrative ? <p className="mt-1 text-xs leading-5 text-slate-600">{stop.narrative}</p> : null}
            <div className="mt-3 flex flex-wrap gap-2">
              <button type="button" className="jag-button-secondary px-3 py-1.5 text-xs" onClick={() => onRemove(stop.title)}>
                移除
              </button>
              <button type="button" className="jag-button-secondary px-3 py-1.5 text-xs" onClick={() => onReplace(stop.title)}>
                替换
              </button>
            </div>
          </div>
        </li>
      ))}
    </ol>
  );
}

function applyPace(stops: ItineraryStop[], pace: string) {
  if (pace === "slow") return stops.slice(0, 3);
  if (pace === "dense") return stops.slice(0, 6);
  return stops.slice(0, 5);
}

function titleFor(itinerary: Itinerary, persona: string, pace: string) {
  const city = itinerary.city ?? "日本";
  if (persona === "elder") return `${city}慢节奏安心路线`;
  if (persona === "family") return `${city}亲子轻松路线`;
  if (persona === "couple") return `${city}情侣散步路线`;
  if (persona === "foodie") return `${city}美食探索路线`;
  return pace === "dense" ? `${city}紧凑一日路线` : itinerary.title;
}

function narrativeFor(title: string, persona: string, pace: string, fallback?: string | null) {
  if (persona === "elder") return `${title}会减少连续步行，把休息和交通便利放在前面。`;
  if (persona === "family") return `${title}会控制停留密度，优先保留轻松和互动感。`;
  if (persona === "couple") return `${title}会保留散步和拍照空间，让节奏更松弛。`;
  if (pace === "dense") return `${title}会增加停留密度，但仍保留必要的用餐和休息点。`;
  return fallback ?? `${title}已按当前偏好重新组织。`;
}

function durationLabel(duration: string) {
  return duration === "one_day" ? "一日" : "半日";
}

function routeTypeLabel(persona: string) {
  const labels: Record<string, string> = {
    first_time: "经典",
    family: "亲子",
    couple: "情侣",
    elder: "慢节奏",
    foodie: "美食",
  };
  return labels[persona] ?? "路线";
}

function personaLabel(persona: string) {
  const labels: Record<string, string> = {
    first_time: "适合第一次来日本",
    family: "适合亲子家庭",
    couple: "适合情侣散步",
    elder: "适合带老人慢慢体验",
    foodie: "适合美食探索",
  };
  return labels[persona] ?? persona;
}

function paceLabel(pace: string) {
  return { slow: "慢节奏", normal: "标准节奏", dense: "紧凑节奏" }[pace] ?? pace;
}

function timeLabel(pace: string) {
  if (pace === "slow") return "约3-5小时";
  if (pace === "dense") return "约6-8小时";
  return "约4-6小时";
}

function stableId(input: string) {
  let hash = 0;
  for (let index = 0; index < input.length; index += 1) {
    hash = (hash * 31 + input.charCodeAt(index)) >>> 0;
  }
  return hash.toString(16);
}
