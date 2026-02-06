"use client"

import { useState } from "react"
import { ChevronLeft, ChevronRight } from "lucide-react"

import cn from "@/app/lib/utils/cn"
import type Flashcard from "@/app/lib/interfaces/entities/Flashcard"

interface FlashcardProps {
  cards?: Flashcard[]
  className?: string
}

export function Flashcard({ cards, className }: FlashcardProps) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isFlipped, setIsFlipped] = useState(false)

  if (!cards || cards.length === 0) {
    return (
      <div className={cn("flex flex-col items-center justify-center gap-4", className)}>
        <p className="text-sm text-muted-foreground">No hay tarjetas disponibles</p>
      </div>
    )
  }

  const handlePrevious = () => {
    setIsFlipped(false)
    setCurrentIndex((prev) => (prev > 0 ? prev - 1 : cards.length - 1))
  }

  const handleNext = () => {
    setIsFlipped(false)
    setCurrentIndex((prev) => (prev < cards.length - 1 ? prev + 1 : 0))
  }

  const handleFlip = () => {
    setIsFlipped((prev) => !prev)
  }

  const currentCard = cards[currentIndex]

  return (
    <div className={cn("flex flex-col items-center gap-6", className)}>
      {/* Flashcard */}
      <div className="perspective-1000 w-full max-w-md">
        <div
          onClick={handleFlip}
          className={cn(
            "relative h-64 w-full cursor-pointer transition-transform duration-500 preserve-3d",
            isFlipped && "rotate-y-180",
          )}
          style={{
            transformStyle: "preserve-3d",
            transform: isFlipped ? "rotateY(-180deg)" : "rotateY(0deg)",
          }}
        >
          {/* Frente - Pregunta */}
          <div
            className="absolute inset-0 flex items-center justify-center rounded-lg border-2 border-primary bg-card p-8 backface-hidden"
            style={{ backfaceVisibility: "hidden" }}
          >
            <div className="text-center">
              <p className="mb-2 text-sm font-medium text-muted-foreground">Pregunta</p>
              <p className="text-xl font-semibold text-foreground">{currentCard?.question}</p>
            </div>
          </div>

          {/* Reverso - Respuesta */}
          <div
            className="absolute inset-0 flex items-center justify-center rounded-lg border-2 border-primary bg-primary p-8 backface-hidden"
            style={{
              backfaceVisibility: "hidden",
              transform: "rotateY(180deg)",
            }}
          >
            <div className="text-center">
              <p className="mb-2 text-sm font-medium text-primary-foreground/80">Respuesta</p>
              <p className="md:text-xl text-primary-foreground">{currentCard?.answer}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Botones de navegación */}
      <div className="flex items-center gap-4">
        <button onClick={handlePrevious} aria-label="Tarjeta anterior" className="cursor-pointer text-muted-foreground p-2 hover:bg-[var(--hover-bg)] hover:rounded-full hover:shadow-md transition-shadow duration-300">
          <ChevronLeft className="h-4 w-4" />
        </button>
        <span className="text-sm text-muted-foreground">
          {currentIndex + 1} / {cards.length}
        </span>
        <button onClick={handleNext} aria-label="Siguiente tarjeta" className="cursor-pointer text-muted-foreground p-2 hover:bg-[var(--hover-bg)] hover:rounded-full hover:shadow-md transition-shadow duration-300">
          <ChevronRight className="h-4 w-4" />
        </button>
      </div>
    </div>
  )
}
