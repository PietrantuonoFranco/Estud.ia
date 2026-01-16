import { BookOpen } from "lucide-react"

import "./flashcard.css";
import { Flashcard } from "./Flashcard"
import { useChatInformationContext } from "../../contexts/ChatInformationContext";
import { useOptionContext } from "../../contexts/OptionContext";

export default function FlashcardContainer() {
  const { notebook, flashcards } = useChatInformationContext();
  const { isLoading } = useOptionContext();

  return (
    <main className="flex flex-col min-h-[100dvh]">
      <div className="flex items-center space-x-2 border-b border-border px-6 py-4.5">
        <BookOpen className="h-4 w-4 text-[var(--green-accent)]" />
        <h2 className="text-sm font-medium text-foreground">Tarjetas Didácticas</h2>
      </div>

      <div className="flex-1 flex items-center justify-center p-4">
        <div className="w-full max-w-3xl">
          {isLoading ? (
            <div className="flex flex-col items-center justify-center gap-4">
              <svg
                className="h-12 w-12 animate-spin text-foreground"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              <p className="text-sm text-muted-foreground">Generando tarjetas didácticas...</p>
            </div>
          ) : (
            <>
              <div className="mb-4 flex flex-col items-center gap-6 text-center">
                <div className="flex text-4xl h-16 w-16 items-center justify-center rounded-full bg-[var(--hover-bg)]">
                  {notebook?.icon}
                </div>

                <h1 className="text-4xl font-semibold text-foreground">{notebook?.title}</h1>
                <p className="text-sm text-muted-foreground">
                  Tarjetas didácticas de estudio
                </p>
              </div>
              <Flashcard cards={notebook?.flashcards} />
              <p className="mt-6 text-center text-sm text-muted-foreground">Haz click en la tarjeta para ver la respuesta</p>
            </>
          )}
        </div>
      </div>
    </main>
  )
}