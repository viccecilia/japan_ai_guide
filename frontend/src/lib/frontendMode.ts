export type FrontendMode = "public" | "debug" | "operator";

export function getFrontendMode(): FrontendMode {
  if (process.env.NEXT_PUBLIC_OPERATOR_MODE === "true") return "operator";
  if (process.env.NEXT_PUBLIC_DEBUG_MODE === "true") return "debug";
  return "public";
}

export function canShowInternalDebug(): boolean {
  return getFrontendMode() !== "public";
}
