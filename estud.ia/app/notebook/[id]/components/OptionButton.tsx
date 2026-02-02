"use client"

import { useOptionContext } from "../contexts/OptionContext"
import { useNotification } from "@/app/contexts/NotificationContext";

interface OptionButtonProps {
  optionName: string;
  icon: React.ComponentType<any>;
  label: string;
  colorClasses?: string;
  openPanel: boolean;
}

export default function OptionButton({ optionName, icon: Icon, label, colorClasses, openPanel }: OptionButtonProps) {
  const { setOption, createFlashcard, createQuiz, isLoading, setIsLoading } = useOptionContext();
  const { addNotification } = useNotification();

  const handleClick = async () => {
    // Create new entity based on option
    if (optionName === "flashcards") {
      try {
        setIsLoading(true);
        await createFlashcard();
        addNotification("Tarjetas creadas", "Las tarjetas didácticas se han creado exitosamente.", "success");
        setIsLoading(false);
      } catch (error) {
        addNotification("Error", "Hubo un error al crear las tarjetas didácticas.", "error");
        setIsLoading(false);
      }
    } else if (optionName === "quiz") {
      try {
        setIsLoading(true);
        await createQuiz();
        addNotification("Cuestionario creado", "El cuestionario se ha creado exitosamente.", "success");
        setIsLoading(false);
      } catch (error) {
        addNotification("Error", "Hubo un error al crear el cuestionario.", "error");
        setIsLoading(false);
      }
    }
    
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