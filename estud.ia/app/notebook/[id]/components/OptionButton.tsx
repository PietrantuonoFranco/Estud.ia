"use client"

import { useOptionContext } from "../contexts/OptionContext"

interface OptionButtonProps {
  optionName: string;
  icon: React.ComponentType<any>;
  label: string;
  colorClasses?: string;
  openPanel: boolean;
}

export default function OptionButton({ optionName, icon: Icon, label, colorClasses, openPanel }: OptionButtonProps) {
  const { setOption, createFlashcard, createQuiz, isLoading, setIsLoading } = useOptionContext();

  const handleClick = async () => {
    // Create new entity based on option
    if (optionName === "flashcards") {
      setIsLoading(true);
      await createFlashcard();
      setIsLoading(false);
    } else if (optionName === "quiz") {
      setIsLoading(true);
      await createQuiz();
      setIsLoading(false);
    }
    
    // Then change to the option
    setOption(optionName);
  };

  return (
    <button
      onClick={handleClick}
      disabled={isLoading}
      className={`cursor-pointer flex flex-col w-full gap-2 rounded-lg p-3 text-left transition-colors hover:bg-[var(--hover-bg)] disabled:opacity-50 ${colorClasses}`}
    >
      <Icon className="h-4 w-4" />
      <span className={`${ openPanel ? "text-sm font-medium" : "hidden"}`}>{label}</span>
    </button>
  )
}