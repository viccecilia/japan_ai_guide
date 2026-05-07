type QuickQuestionButtonsProps = {
  isLoading: boolean;
  onSelect: (question: string) => void;
};

const quickQuestions = [
  "清水寺",
  "大阪城",
  "伏见稻荷大社",
  "奈良公园",
  "神社和寺庙区别",
  "第一次来日本怎么玩",
];

export function QuickQuestionButtons({ isLoading, onSelect }: QuickQuestionButtonsProps) {
  return (
    <div className="mt-7 flex max-w-full flex-wrap justify-center gap-3 overflow-hidden">
      {quickQuestions.map((question) => (
        <button
          key={question}
          className="jag-button-secondary min-w-0 max-w-[calc(100vw-2rem)] whitespace-normal break-all px-4 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-60 sm:break-words"
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
