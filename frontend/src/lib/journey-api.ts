import type { Itinerary, ItineraryStop } from "../../types/answer-card";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

type ApiResponse<T> = {
  ok: boolean;
  data: T | null;
  error: { code: string; message: string } | null;
};

export type EditableStop = ItineraryStop & {
  active?: boolean;
  replaced_by?: string | null;
};

export type EditableJourneyResponse = {
  journey_state: {
    session_id: string;
    persona?: string | null;
    pace?: string | null;
  };
  editable_itinerary: {
    itinerary: Itinerary;
    current_persona?: string | null;
    current_pace?: string | null;
    active_stops: EditableStop[];
    removed_stops: EditableStop[];
    replaced_stops: Array<{ from: string; to: string }>;
    interaction_history: Array<{ interaction_type: string; narrative: string }>;
  } | null;
  interaction_history: Array<{ interaction_type: string; narrative: string }>;
  analytics: {
    journey_session_id: string;
    interaction_count: number;
    regeneration_count: number;
    persona_changes: number;
    pace_changes: number;
    latest_interaction_type?: string | null;
  };
  replay: Record<string, unknown>;
};

export type SavedJourneyListItem = {
  journey_id: string;
  session_id: string;
  user_id?: string | null;
  title: string;
  city?: string | null;
  persona?: string | null;
  pace?: string | null;
  updated_at: string;
  status: string;
};

export type SavedJourney = SavedJourneyListItem & {
  editable_itinerary: EditableJourneyResponse["editable_itinerary"];
  interaction_history: EditableJourneyResponse["interaction_history"];
  analytics: EditableJourneyResponse["analytics"];
  replay: Record<string, unknown>;
};

export type JourneyRestoreResponse = {
  saved_journey: SavedJourney;
  restored_session_id: string;
  analytics: Record<string, unknown>;
  replay: Record<string, unknown>;
};

export async function createJourney(sessionId: string, itinerary: Itinerary) {
  return postJourney("/api/journey/create", { session_id: sessionId, itinerary });
}

export async function switchJourneyPersona(sessionId: string, persona: string) {
  return postJourney("/api/journey/persona", { session_id: sessionId, persona });
}

export async function switchJourneyPace(sessionId: string, pace: string) {
  return postJourney("/api/journey/pace", { session_id: sessionId, pace });
}

export async function removeJourneyStop(sessionId: string, stopTitle: string) {
  return postJourney("/api/journey/remove-stop", { session_id: sessionId, stop_title: stopTitle });
}

export async function replaceJourneyStop(sessionId: string, stopTitle: string) {
  return postJourney("/api/journey/replace-stop", { session_id: sessionId, stop_title: stopTitle });
}

export async function regenerateJourney(sessionId: string, prompt: string) {
  return postJourney("/api/journey/regenerate", { session_id: sessionId, prompt });
}

export async function saveJourney(sessionId: string, title?: string) {
  return postJourneyStorage<SavedJourney>("/api/journey/save", { session_id: sessionId, title });
}

export async function listSavedJourneys() {
  return getJourneyStorage<SavedJourneyListItem[]>("/api/journey/saved");
}

export async function restoreSavedJourney(journeyId: string) {
  return getJourneyStorage<JourneyRestoreResponse>(`/api/journey/saved/${journeyId}`);
}

export async function deleteSavedJourney(journeyId: string) {
  return deleteJourneyStorage<{ deleted: boolean; journey_id: string }>(`/api/journey/saved/${journeyId}`);
}

async function postJourney(path: string, body: Record<string, unknown>): Promise<EditableJourneyResponse> {
  return postJourneyStorage<EditableJourneyResponse>(path, body);
}

async function postJourneyStorage<T>(path: string, body: Record<string, unknown>): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const payload = (await response.json()) as ApiResponse<EditableJourneyResponse>;
  if (!response.ok || !payload.ok || !payload.data) {
    throw new Error(payload.error?.message ?? `Journey API failed: ${response.status}`);
  }
  return payload.data as T;
}

async function getJourneyStorage<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);
  const payload = (await response.json()) as ApiResponse<T>;
  if (!response.ok || !payload.ok || !payload.data) {
    throw new Error(payload.error?.message ?? `Journey API failed: ${response.status}`);
  }
  return payload.data;
}

async function deleteJourneyStorage<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, { method: "DELETE" });
  const payload = (await response.json()) as ApiResponse<T>;
  if (!response.ok || !payload.ok || !payload.data) {
    throw new Error(payload.error?.message ?? `Journey API failed: ${response.status}`);
  }
  return payload.data;
}
