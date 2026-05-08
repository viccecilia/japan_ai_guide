"use client";

import { useState } from "react";
import type {
  AdaptiveJourney,
  JourneyDay,
  JourneyTimeline,
  TimelineConstraint,
  TravelContext,
  TravelMemorySnapshot,
} from "../../../types/answer-card";
import { AdaptiveSuggestionCard } from "./AdaptiveSuggestionCard";
import { TimelineConstraintBadge } from "./TimelineConstraintBadge";
import { TravelContextCard } from "./TravelContextCard";
import { TravelPreferenceCard } from "./TravelPreferenceCard";

const paceOptions = [
  { value: "slow", label: "轻松" },
  { value: "normal", label: "均衡" },
  { value: "dense", label: "充实" },
];

export function JourneyTimelineView({
  timeline,
  constraint,
  adaptiveJourney,
  travelContext,
  travelMemory,
}: {
  timeline?: JourneyTimeline | null;
  constraint?: TimelineConstraint | null;
  adaptiveJourney?: AdaptiveJourney | null;
  travelContext?: TravelContext | null;
  travelMemory?: TravelMemorySnapshot | null;
}) {
  const [selectedDay, setSelectedDay] = useState(0);
  const [localTimeline, setLocalTimeline] = useState(timeline ?? null);
  const [localConstraint, setLocalConstraint] = useState(constraint ?? null);
  const [notice, setNotice] = useState<string | null>(null);

  if (!localTimeline || localTimeline.days.length === 0) return null;

  const day = localTimeline.days[Math.min(selectedDay, localTimeline.days.length - 1)];
  const transition = transitionForDay(localTimeline, day.day_number);

  function updateDay(nextDay: JourneyDay, message: string) {
    setLocalTimeline((current) => {
      if (!current) return current;
      return {
        ...current,
        days: current.days.map((item) => (item.day_number === nextDay.day_number ? nextDay : item)),
      };
    });
    setNotice(message);
  }

  function applySmartOptimize() {
    if (!adaptiveJourney?.optimized_timeline) return;
    setLocalTimeline(adaptiveJourney.optimized_timeline);
    setLocalConstraint(adaptiveJourney.optimized_constraint ?? localConstraint);
    setSelectedDay(0);
    setNotice(adaptiveJourney.narrative || "已智能优化路线。");
  }

  function applyContextOptimize() {
    if (!travelContext?.context_optimized_timeline) return;
    setLocalTimeline(travelContext.context_optimized_timeline);
    setSelectedDay(0);
    setNotice(travelContext.narrative || "已根据当前状态优化路线。");
  }

  function removeStop(title: string) {
    const nextBlocks = day.blocks.map((block) => ({
      ...block,
      stops: block.stops.filter((stop) => stop.title !== title),
    }));
    updateDay(
      {
        ...day,
        blocks: nextBlocks,
        daily_narrative: `已从 Day ${day.day_number} 移除「${title}」，这一天会更轻松。`,
      },
      "已更新当天路线",
    );
  }

  function changePace(pace: string) {
    const paceLabel = paceOptions.find((item) => item.value === pace)?.label ?? pace;
    updateDay(
      {
        ...day,
        pace,
        daily_narrative: `Day ${day.day_number} 已调整为${paceLabel}节奏，停留点会按体力重新安排。`,
      },
      `已切换为${paceLabel}节奏`,
    );
  }

  function regenerateDay() {
    updateDay(
      {
        ...day,
        daily_narrative: `已重新生成 Day ${day.day_number} 的旅行节奏，保留核心体验并减少重复停留。`,
      },
      "已重新生成当天路线",
    );
  }

  return (
    <section className="rounded-[22px] border border-slate-200 bg-white p-4 shadow-sm sm:p-5">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.12em] text-rose-500">Travel Timeline</p>
          <h3 className="mt-1 text-xl font-bold text-slate-950">{localTimeline.title}</h3>
          <p className="mt-1 text-sm text-slate-600">
            {localTimeline.cities.join(" → ")} · {localTimeline.total_duration} · {localTimeline.journey_style}
          </p>
        </div>
        <div className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">
          {localTimeline.days.length} 天 · {localTimeline.transitions.length} 次城市切换
        </div>
      </div>

      <div className="mt-4 grid gap-3">
        <TimelineConstraintBadge constraint={localConstraint} />
        <TravelPreferenceCard memory={travelMemory} />
        <TravelContextCard context={travelContext} onApplyContext={applyContextOptimize} />
        <AdaptiveSuggestionCard adaptiveJourney={adaptiveJourney} onOptimize={applySmartOptimize} />
      </div>

      <div className="mt-4 flex gap-2 overflow-x-auto pb-1">
        {localTimeline.days.map((item, index) => (
          <button
            key={item.day_number}
            type="button"
            onClick={() => setSelectedDay(index)}
            className={`shrink-0 rounded-full px-4 py-2 text-sm font-semibold transition ${
              selectedDay === index ? "bg-slate-950 text-white" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
            }`}
          >
            Day {item.day_number}
          </button>
        ))}
      </div>

      <div className="mt-5 grid gap-4 lg:grid-cols-[1fr_280px]">
        <div className="space-y-4">
          <div className="rounded-2xl bg-slate-50 p-4">
            <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h4 className="text-lg font-bold text-slate-950">{day.title}</h4>
                <p className="mt-1 text-sm leading-6 text-slate-600">{day.daily_narrative}</p>
              </div>
              <div className="flex gap-2">
                {paceOptions.map((option) => (
                  <button
                    key={option.value}
                    type="button"
                    onClick={() => changePace(option.value)}
                    className={`rounded-full px-3 py-1.5 text-xs font-semibold ${
                      day.pace === option.value ? "bg-emerald-600 text-white" : "bg-white text-slate-700"
                    }`}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {day.blocks.map((block) => (
            <div key={`${day.day_number}-${block.time_of_day}`} className="relative rounded-2xl border border-slate-200 p-4">
              <div className="mb-3 flex items-center justify-between gap-3">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.12em] text-slate-400">{block.time_of_day}</p>
                  <h5 className="text-base font-bold text-slate-900">{block.title}</h5>
                </div>
                <span className="rounded-full bg-amber-50 px-3 py-1 text-xs font-semibold text-amber-700">
                  {block.stops.length} stops
                </span>
              </div>
              {block.narrative ? <p className="mb-3 text-sm leading-6 text-slate-600">{block.narrative}</p> : null}
              <div className="space-y-3">
                {block.stops.map((stop, index) => (
                  <div key={`${stop.title}-${index}`} className="flex gap-3 rounded-xl bg-slate-50 p-3">
                    <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-white text-xs font-bold text-slate-700">
                      {index + 1}
                    </div>
                    <div className="min-w-0 flex-1">
                      <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                        <div>
                          <p className="font-bold text-slate-950">{stop.title}</p>
                          <p className="text-sm text-slate-600">{stop.subtitle ?? stop.estimated_time ?? "建议停留"}</p>
                        </div>
                        <button
                          type="button"
                          onClick={() => removeStop(stop.title)}
                          className="self-start rounded-full bg-white px-3 py-1 text-xs font-semibold text-slate-600 hover:bg-rose-50 hover:text-rose-700"
                        >
                          移除
                        </button>
                      </div>
                      {stop.narrative ? <p className="mt-2 text-sm leading-6 text-slate-600">{stop.narrative}</p> : null}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        <aside className="space-y-3">
          {day.hotel ? (
            <div className="rounded-2xl border border-slate-200 bg-slate-950 p-4 text-white">
              <p className="text-xs font-semibold uppercase tracking-[0.12em] text-slate-300">Hotel</p>
              <h5 className="mt-1 font-bold">{day.hotel.title}</h5>
              <p className="mt-2 text-sm leading-6 text-slate-200">{day.hotel.narrative}</p>
            </div>
          ) : null}

          {transition ? (
            <div className="rounded-2xl border border-slate-200 bg-white p-4">
              <p className="text-xs font-semibold uppercase tracking-[0.12em] text-slate-400">Transition</p>
              <h5 className="mt-1 font-bold text-slate-950">
                {transition.from_city} → {transition.to_city}
              </h5>
              <p className="mt-2 text-sm text-slate-600">
                {transition.recommended_transport} · {transition.estimated_transition_time ?? transition.estimated_travel_time}
              </p>
              <p className="mt-2 text-sm leading-6 text-slate-600">{transition.narrative}</p>
            </div>
          ) : null}

          <button
            type="button"
            onClick={regenerateDay}
            className="w-full rounded-full bg-emerald-600 px-4 py-3 text-sm font-bold text-white hover:bg-emerald-700"
          >
            重新生成这一天
          </button>
          {notice ? <p className="rounded-2xl bg-emerald-50 p-3 text-sm font-semibold text-emerald-800">{notice}</p> : null}
        </aside>
      </div>
    </section>
  );
}

function transitionForDay(timeline: JourneyTimeline, dayNumber: number) {
  const day = timeline.days.find((item) => item.day_number === dayNumber);
  const nextDay = timeline.days.find((item) => item.day_number === dayNumber + 1);
  if (!day || !nextDay || day.city === nextDay.city) return null;
  return timeline.transitions.find((transition) => transition.from_city === day.city && transition.to_city === nextDay.city) ?? null;
}
