export type IntentType =
  | "spot_query"
  | "city_query"
  | "food_query"
  | "route_query"
  | "culture_query"
  | "hotel_query"
  | "generic_query"
  | "unknown";

export type IntentResult = {
  intent_type: IntentType;
  entity?: string | null;
  city?: string | null;
  language: string;
  confidence: number;
};
