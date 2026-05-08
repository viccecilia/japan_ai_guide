import type { MultiCardResponse } from "../../../types/answer-card";
import { canShowInternalDebug, getFrontendMode } from "../../lib/frontendMode";

export function AnalyticsDebugPanel({ response }: { response: MultiCardResponse }) {
  if (!canShowInternalDebug()) return null;

  const analytics = response.metadata.analytics;
  const attribution = response.metadata.attribution;
  const governance = response.metadata.governance as
    | {
        principle?: string;
        external_jump_tracking?: { active?: boolean };
      }
    | undefined;
  const mode = getFrontendMode();

  return (
    <div className="jag-internal-debug">
      <div>Analytics Debug ({mode})</div>
      <div>Session ID: {analytics?.session_id ?? "-"}</div>
      <div>Traffic Source: {attribution?.utm_source ?? attribution?.referrer ?? "direct/mock"}</div>
      <div>Event Count: {analytics?.event_count ?? 0}</div>
      <div>Query Chain: {(analytics?.query_chain ?? []).join(" -> ") || "-"}</div>
      <div>Recommendation Source: {analytics?.recommendation_source ?? "-"}</div>
      <div>Governance: {governance?.principle ?? "relevance first"}</div>
      <div>Partner Boost: {governance?.external_jump_tracking?.active ? "tracked" : "disabled"}</div>
    </div>
  );
}
