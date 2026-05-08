export function PersonaBadge({
  label,
  pace,
}: {
  label?: string | null;
  pace?: string | null;
}) {
  if (!label && !pace) return null;

  return (
    <div className="flex flex-wrap gap-2">
      {label ? (
        <span className="rounded-full bg-rose-50 px-3 py-1 text-xs font-black text-rose-700">
          {label}
        </span>
      ) : null}
      {pace ? (
        <span className="rounded-full bg-indigo-50 px-3 py-1 text-xs font-black text-indigo-700">
          {paceLabel(pace)}
        </span>
      ) : null}
    </div>
  );
}

function paceLabel(pace: string) {
  const labels: Record<string, string> = {
    slow: "慢节奏",
    normal: "标准节奏",
    dense: "紧凑节奏",
  };
  return labels[pace] ?? pace;
}
