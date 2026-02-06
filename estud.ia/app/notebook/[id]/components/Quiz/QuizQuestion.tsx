"use client"

import { useState, useMemo } from "react"
import { CheckCircle2, XCircle } from "lucide-react"

import QuestionsAndAnswers from "@/app/lib/interfaces/entities/QuestionsAndAnswers"
import cn from "@/app/lib/utils/cn"

interface QuizQuestionProps {
  questionData: QuestionsAndAnswers
  onAnswerSelected?: (isCorrect: boolean) => void
}

export function QuizQuestion({ questionData, onAnswerSelected }: QuizQuestionProps) {
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null)
  const [hasAnswered, setHasAnswered] = useState(false)

  // Validar que questionData existe
  if (!questionData) {
    return (
      <div className="w-full max-w-2xl mx-auto border border-border rounded-lg bg-card shadow-sm overflow-hidden">
        <div className="p-6 text-center">
          <p className="text-muted-foreground">No hay preguntas disponibles</p>
        </div>
      </div>
    )
  }

  // Mezclar las respuestas aleatoriamente
  const shuffledAnswers = useMemo(() => {
    const answers = [
      { text: questionData.answer, isCorrect: true },
      { text: questionData.incorrect_answer_1, isCorrect: false },
      { text: questionData.incorrect_answer_2, isCorrect: false },
      { text: questionData.incorrect_answer_3, isCorrect: false },
    ]
    return answers.sort(() => Math.random() - 0.5)
  }, [questionData])

  const handleAnswerClick = (answer: { text: string; isCorrect: boolean }) => {
    if (hasAnswered) return

    setSelectedAnswer(answer.text)
    setHasAnswered(true)
    onAnswerSelected?.(answer.isCorrect)
  }

  const getAnswerStyle = (answer: { text: string; isCorrect: boolean }) => {
    if (!hasAnswered) {
      return "bg-card hover:bg-secondary border-border hover:border-primary/50 cursor-pointer"
    }

    if (answer.isCorrect) {
      return "bg-[var(--hover-bg)] border-emerald-500 text-emerald-500"
    }

    if (selectedAnswer === answer.text && !answer.isCorrect) {
      return "bg-[var(--hover-bg)] border-red-500 text-red-500"
    }

    return "bg-muted border-border opacity-50"
  }

  return (
    <div className="w-full max-w-2xl mx-auto border border-border rounded-lg bg-card shadow-sm overflow-hidden">
      <div className="px-6 py-3 border-b border-border">
        <h2 className="md:text-xl font-semibold text-foreground">
          {questionData.question}
        </h2>
      </div>
      <div className="p-6 space-y-3">
        {shuffledAnswers.map((answer, index) => (
          <button
            key={index}
            onClick={() => handleAnswerClick(answer)}
            disabled={hasAnswered}
            className={cn(
              "w-full p-4 rounded-lg border-2 text-left transition-all duration-200 flex items-center justify-between gap-3",
              getAnswerStyle(answer)
            )}
          >
            <span className="flex items-center gap-3">
              <span className="flex-shrink-0 w-8 h-8 rounded-full bg-secondary flex items-center justify-center text-xs md:text-sm font-medium">
                {String.fromCharCode(65 + index)}
              </span>
              <span className="text-sm md:text-md font-medium">{answer.text}</span>
            </span>
            {hasAnswered && answer.isCorrect && (
              <CheckCircle2 className="w-6 h-6 text-emerald-600 flex-shrink-0" />
            )}
            {hasAnswered && selectedAnswer === answer.text && !answer.isCorrect && (
              <XCircle className="w-6 h-6 text-red-600 flex-shrink-0" />
            )}
          </button>
        ))}

        {hasAnswered && (
          <div
            className={cn(
              "mt-4 p-4 rounded-lg text-sm md:text-md text-center font-medium",
              selectedAnswer === questionData.answer
                ? "bg-emerald-100 text-emerald-800"
                : "bg-red-100 text-red-800"
            )}
          >
            {selectedAnswer === questionData.answer
              ? "¡Correcto! 🎉"
              : `Incorrecto. La respuesta correcta era: ${questionData.answer}`}
          </div>
        )}
      </div>
    </div>
  )
}
