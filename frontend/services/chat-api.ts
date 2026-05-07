import type { AnswerCard, MultiCardResponse, RecommendationSection } from "../types/answer-card";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

type ApiError = {
  code: string;
  message: string;
};

type ApiResponse<T> = {
  ok: boolean;
  data: T | null;
  error: ApiError | null;
  meta: Record<string, string | number | boolean>;
};

type ChatQueryData = {
  question: string;
  answer_card: AnswerCard | null;
  main_card?: AnswerCard | null;
  related_cards?: AnswerCard[];
  sections?: RecommendationSection[];
  metadata?: Record<string, unknown>;
};

export async function queryChat(question: string, language = "zh"): Promise<MultiCardResponse | null> {
  const response = await fetch(`${API_BASE_URL}/api/chat/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question, language }),
  });

  let payload: ApiResponse<ChatQueryData>;
  try {
    payload = (await response.json()) as ApiResponse<ChatQueryData>;
  } catch {
    throw new Error("后端返回内容无法解析。");
  }

  if (!response.ok || !payload.ok) {
    throw new Error(payload.error?.message ?? `请求失败：HTTP ${response.status}`);
  }

  const data = payload.data;
  if (!data?.answer_card) return null;

  return {
    main_card: data.main_card ?? data.answer_card,
    related_cards: data.related_cards ?? [],
    sections: data.sections ?? [],
    metadata: data.metadata ?? {},
  };
}
