import type { IntentResult } from "./intent";

export type AnswerCardType =
  | "spot_card"
  | "city_card"
  | "food_card"
  | "route_card"
  | "culture_card"
  | "generic_card";

export type AnswerCardFieldSource = "ai" | "database" | "mock" | "computed";

export type AnswerCardAudio = {
  text?: string;
  voice?: string;
  audio_url?: string;
  duration_seconds?: number;
  source?: AnswerCardFieldSource;
};

export type AnswerCardNearby = {
  id?: string;
  name: string;
  type?: "spot" | "station" | "shop" | "restaurant" | "hotel" | "other";
  distance_text?: string;
  description?: string;
  source?: AnswerCardFieldSource;
};

export type AnswerCardFood = {
  name: string;
  description?: string;
  area?: string;
  source?: AnswerCardFieldSource;
};

export type AnswerCardHotel = {
  name: string;
  description?: string;
  area?: string;
  source?: AnswerCardFieldSource;
};

export type AnswerCardAction = {
  label: string;
  action: "ask_followup" | "create_route" | "save_to_trip" | "open_map" | "play_audio" | "open_charter";
  enabled: boolean;
  payload?: Record<string, string | number | boolean>;
  source?: AnswerCardFieldSource;
};

export type AnswerCardMetadata = {
  language: string;
  mock: boolean;
  sources: AnswerCardFieldSource[];
  ai_fields?: string[];
  database_fields?: string[];
  intent?: IntentResult | null;
  ai_runtime?: {
    allow_realtime_ai?: boolean;
    mode?: string;
    reason?: string;
    fallback_level?: string;
    realtime_ai_used?: boolean;
  };
  content_source?: {
    type?: "content_library" | "template" | string;
    slug?: string;
    language?: string;
  };
  cache?: {
    hit?: boolean;
    key?: string;
    source?: string;
    ttl_seconds?: number;
  };
  ranking?: {
    slug?: string | null;
    score?: number;
    matched_by?: string;
    content_type?: string | null;
    priority?: number;
  };
  related_candidates?: Array<{
    slug?: string | null;
    score?: number;
    matched_by?: string;
    content_type?: string | null;
    priority?: number;
  }>;
  card_groups?: Record<string, number>;
};

export type AnswerCard = {
  id: string;
  card_type: AnswerCardType;
  title: string;
  subtitle: string;
  description: string;
  story: string;
  audio: AnswerCardAudio;
  nearby: AnswerCardNearby[];
  foods: AnswerCardFood[];
  hotels: AnswerCardHotel[];
  actions: AnswerCardAction[];
  metadata: AnswerCardMetadata;
  card_group?: "main" | "related" | string;
  display_priority?: number;
  display_style?: "large" | "compact" | string;
  recommendation_reason?: string | null;
};

export type RecommendationSection = {
  section_type: string;
  title: string;
  cards: AnswerCard[];
};

export type MultiCardResponse = {
  main_card: AnswerCard;
  related_cards: AnswerCard[];
  sections: RecommendationSection[];
  metadata: Record<string, unknown>;
};
