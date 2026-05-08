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
  orchestration?: {
    strategy?: string;
    section_order?: string[];
    deduped_count?: number;
    reason?: string;
  };
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

export type ItineraryStop = {
  title: string;
  subtitle?: string | null;
  stop_type?: string;
  estimated_time?: string | null;
  transport_notes?: string | null;
  narrative?: string | null;
};

export type ItineraryBlock = {
  block_title: string;
  time_of_day: string;
  stops: ItineraryStop[];
  narrative?: string | null;
};

export type Itinerary = {
  title: string;
  city?: string | null;
  duration: string;
  route_type: string;
  persona?: string | null;
  persona_label?: string | null;
  pace?: string | null;
  journey_style?: string | null;
  stops: ItineraryStop[];
  foods?: ItineraryStop[];
  culture?: ItineraryStop[];
  hotel?: ItineraryStop | null;
  blocks: ItineraryBlock[];
  transport_notes?: string | null;
  estimated_time?: string | null;
  narrative?: string | null;
};

export type JourneyBlock = {
  block_type: string;
  title: string;
  time_of_day: string;
  stops: ItineraryStop[];
  narrative?: string | null;
};

export type JourneyTransition = {
  from_city: string;
  to_city: string;
  recommended_transport: string;
  estimated_travel_time: string;
  estimated_transition_time?: string;
  transition_type?: string;
  transition_load?: string;
  narrative: string;
};

export type JourneyDay = {
  day_number: number;
  title: string;
  city: string;
  date_label?: string | null;
  blocks: JourneyBlock[];
  hotel?: ItineraryStop | null;
  daily_narrative: string;
  pace: string;
};

export type JourneyTimeline = {
  timeline_id: string;
  title: string;
  days: JourneyDay[];
  cities: string[];
  hotels: ItineraryStop[];
  transitions: JourneyTransition[];
  total_duration: string;
  journey_style: string;
};

export type TimelineConstraint = {
  timeline_id: string;
  timeline_feasibility: "easy" | "balanced" | "tight" | "overloaded" | string;
  feasibility_reason: string;
  walking_load: string;
  transition_load: string;
  daily_density: string;
  hotel_distance: string;
  estimated_fatigue: string;
  daily_constraints?: Array<Record<string, unknown>>;
  transition_constraints?: Array<Record<string, unknown>>;
  hotel_constraints?: Array<Record<string, unknown>>;
};

export type AdaptiveSuggestion = {
  adaptation_type: string;
  title: string;
  description: string;
  trigger_reason: string;
  day_number?: number | null;
  priority: number;
};

export type JourneyAdaptation = {
  adaptation_type: string;
  trigger_reason: string;
  before_feasibility: string;
  after_feasibility: string;
  removed_stops: string[];
  reordered_stops: string[];
  transition_reduction: number;
  fatigue_reduction: string;
  narrative: string;
};

export type AdaptiveJourney = {
  applied: boolean;
  before_feasibility: string;
  after_feasibility: string;
  suggestions: AdaptiveSuggestion[];
  adaptations: JourneyAdaptation[];
  optimized_timeline?: JourneyTimeline | null;
  optimized_constraint?: TimelineConstraint | null;
  fatigue_reduction: string;
  transition_reduction: number;
  adaptation_count: number;
  narrative: string;
};

export type ContextualSuggestion = {
  suggestion_type: string;
  title: string;
  description: string;
  trigger_context: string;
  priority: number;
};

export type TravelContext = {
  weather: {
    condition: "sunny" | "rainy" | "hot" | "crowded" | string;
    summary: string;
    outdoor_pressure: string;
  };
  time: {
    time_of_day: "morning" | "afternoon" | "evening" | "late" | string;
    summary: string;
    long_transition_allowed: boolean;
  };
  fatigue: {
    travel_fatigue: string;
    accumulated_dense_days: number;
    summary: string;
  };
  condition: {
    daily_density: string;
    context_level: "calm" | "watch" | "adjust" | "urgent" | string;
    adaptation_reason: string;
  };
  suggestions: ContextualSuggestion[];
  context_optimized_timeline?: JourneyTimeline | null;
  contextual_adaptation_count: number;
  narrative: string;
};

export type TravelMemorySnapshot = {
  session_id: string;
  preference: {
    preferred_pace: string;
    preferred_cities: string[];
    preferred_persona: string;
    preferred_journey_style: string;
    crowd_tolerance: string;
    walking_tolerance: string;
    fatigue_preference: string;
    last_journey_style: string;
  };
  summary: string;
  evolution: Array<{
    field: string;
    before?: string | null;
    after: string;
    reason: string;
  }>;
};

export type RecommendationSection = {
  section_type: string;
  title: string;
  section_intro?: string | null;
  section_narrative?: string | null;
  cards: AnswerCard[];
  prompts?: string[];
  itineraries?: Itinerary[];
};

export type MultiCardResponse = {
  main_card: AnswerCard;
  related_cards: AnswerCard[];
  sections: RecommendationSection[];
  metadata: {
    orchestration?: {
      strategy?: string;
      section_order?: string[];
      deduped_count?: number;
      reason?: string;
    };
    analytics?: {
      session_id?: string;
      event_count?: number;
      query_chain?: string[];
      intent_evolution?: string[];
      recommendation_source?: string;
      itinerary_generated?: boolean;
      itinerary_type?: string | null;
      stop_count?: number;
      persona?: string | null;
      pace?: string | null;
      journey_style?: string | null;
      journey_flow?: {
        flow_type?: string;
        title?: string;
        summary?: string;
        itineraries?: Itinerary[];
        journey_prompts?: string[];
      } | null;
      timeline_days?: number;
      city_transition_count?: number;
      hotel_insertions?: number;
      timeline_regenerations?: number;
      timeline_feasibility?: string | null;
      fatigue_level?: string | null;
      transition_count?: number;
      walking_load?: string | null;
      weather_context?: string | null;
      fatigue_context?: string | null;
      dynamic_regenerations?: number;
      contextual_adaptation_count?: number;
      memory_updates?: number;
      preference_changes?: number;
      memory_based_regenerations?: number;
    };
    governance?: Record<string, unknown>;
    operator?: Record<string, unknown>;
    persona?: Record<string, unknown>;
    attribution?: {
      utm_source?: string | null;
      utm_campaign?: string | null;
      referrer?: string | null;
      landing_page?: string | null;
      device?: string;
      language?: string;
      country?: string | null;
    };
    timeline?: JourneyTimeline | null;
    timeline_constraint?: TimelineConstraint | null;
    adaptive_journey?: AdaptiveJourney | null;
    travel_context?: TravelContext | null;
    travel_memory?: TravelMemorySnapshot | null;
    [key: string]: unknown;
  };
};
