"use client";

import { useState } from "react";

const languages = ["中文", "English", "日本語", "한국어", "ไทย"];

export function LanguageSelector() {
  const [language, setLanguage] = useState("中文");

  return (
    <div className="ml-auto flex min-w-0 items-center gap-3">
      <span className="hidden text-sm font-bold text-[var(--jag-color-muted)] sm:inline">
        Language
      </span>
      <label className="sr-only" htmlFor="language-select">
        选择语言
      </label>
      <select
        id="language-select"
        data-testid="language-select"
        className="w-24 rounded-full border border-[var(--jag-color-line)] bg-white px-3 py-2 text-sm font-bold text-[var(--jag-color-ink-soft)] shadow-[var(--jag-shadow-sm)] outline-none transition hover:border-blue-200 sm:w-auto sm:px-4"
        value={language}
        onChange={(event) => setLanguage(event.target.value)}
      >
        {languages.map((item) => (
          <option key={item} value={item}>
            {item}
          </option>
        ))}
      </select>
    </div>
  );
}
