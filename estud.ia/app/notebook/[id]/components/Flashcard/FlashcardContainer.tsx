import { BookOpen } from "lucide-react"

import "./flashcard.css";
import { Flashcard } from "./Flashcard"
import { useChatInformationContext } from "../../contexts/ChatInformationContext";

const flashcards = [
  {
    question: "¿Qué es React?",
    answer: "Una biblioteca de JavaScript para construir interfaces de usuario",
  },
  {
    question: "¿Qué es un componente en React?",
    answer: "Una pieza reutilizable de código que devuelve elementos de React",
  },
  {
    question: "¿Qué es JSX?",
    answer: "Una extensión de sintaxis de JavaScript que permite escribir HTML en React",
  },
  {
    question: "¿Qué son los hooks en React?",
    answer: "Funciones que permiten usar estado y otras características en componentes funcionales",
  },
]

export default function FlashcardContainer() {
  const { notebook } = useChatInformationContext();

  return (
    <main className="flex flex-col min-h-[100dvh]">
      <div className="flex items-center space-x-2 border-b border-border px-6 py-4.5">
        <BookOpen className="h-4 w-4 text-[var(--green-accent)]" />
        <h2 className="text-sm font-medium text-foreground">Flashcards</h2>
      </div>

      <div className="flex-1 flex items-center justify-center p-4">
        <div className="w-full max-w-3xl">
          <div className="mb-4 flex flex-col items-center gap-6 text-center">
            <div className="flex text-4xl h-16 w-16 items-center justify-center rounded-full bg-[var(--hover-bg)]">
              {notebook?.icon}
            </div>

            <h1 className="text-4xl font-semibold text-foreground">{notebook?.title}</h1>
            <p className="text-sm text-muted-foreground">
              Flashcards de estudio
            </p>
          </div>
          <Flashcard cards={flashcards} />
          <p className="mt-6 text-center text-sm text-muted-foreground">Haz click en la tarjeta para ver la respuesta</p>
        </div>
      </div>
    </main>
  )
}