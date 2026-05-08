type QuickQuestionButtonsProps = {
  isLoading: boolean;
  onSelect: (question: string) => void;
};

const quickQuestions = [
  "清水寺有什么故事？",
  "大阪一日游怎么安排？",
  "伏见稻荷大社怎么玩？",
  "奈良公园适合半日游吗？",
  "神社和寺庙有什么区别？",
  "第一次来日本怎么玩？",
];

export function QuickQuestionButtons({ isLoading, onSelect }: QuickQuestionButtonsProps) {
  return (
    <div className="mt-7 flex max-w-full flex-wrap justify-center gap-3 overflow-hidden">
      {quickQuestions.map((question) => (
        <button
          key={question}
          className="jag-button-secondary min-w-0 max-w-[calc(100vw-2rem)] whitespace-normal break-words px-4 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-60"
          type="button"
          disabled={isLoading}
          onClick={() => onSelect(question)}
        >
          {question}
        </button>
      ))}
    </div>
  );
}
