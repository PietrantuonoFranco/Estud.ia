"use client"

import { HelpCircle } from "lucide-react"

import { useState, useCallback } from "react"
import { QuizQuestion } from "./QuizQuestion"
import { ArrowRight, RotateCcw, Trophy } from "lucide-react"

import { useChatInformationContext } from "../../contexts/ChatInformationContext";
import { useOptionContext } from "../../contexts/OptionContext";

import QuestionsAndAnswers from "@/app/lib/interfaces/entities/QuestionsAndAnswers"


interface QuizContainerProps {
  questions?: QuestionsAndAnswers[]
  quizTitle?: string
  onQuizComplete?: (score: number, total: number) => void
}

export default function QuizContainer({ 
  questions = sampleQuestions,
  quizTitle = "Quiz", 
  onQuizComplete 
}: QuizContainerProps) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [score, setScore] = useState(0)
  const [answeredCurrent, setAnsweredCurrent] = useState(false)
  const [isComplete, setIsComplete] = useState(false)

  const { quizzes } = useChatInformationContext();
  const { isLoading } = useOptionContext();

  const totalQuestions = questions.length
  const progress = ((currentIndex + (answeredCurrent ? 1 : 0)) / totalQuestions) * 100

  const handleAnswerSelected = useCallback((isCorrect: boolean) => {
    if (isCorrect) {
      setScore(prev => prev + 1)
    }
    setAnsweredCurrent(true)
  }, [])

  const handleNextQuestion = () => {
    if (currentIndex < totalQuestions - 1) {
      setCurrentIndex(prev => prev + 1)
      setAnsweredCurrent(false)
    } else {
      setIsComplete(true)
      onQuizComplete?.(score, totalQuestions)
    }
  }

  const handleRestart = () => {
    setCurrentIndex(0)
    setScore(0)
    setAnsweredCurrent(false)
    setIsComplete(false)
  }

  const getScoreMessage = () => {
    const percentage = (score / totalQuestions) * 100
    if (percentage === 100) return "Excelente! Puntuacion perfecta!"
    if (percentage >= 80) return "Muy bien! Gran desempeno!"
    if (percentage >= 60) return "Buen trabajo! Sigue practicando."
    if (percentage >= 40) return "Puedes mejorar. Intenta de nuevo!"
    return "No te rindas! Practica mas."
  }

  if (isComplete) {
    return (
      <main className="flex flex-col items-center justify-center">
        <div className="w-full max-w-3xl flex-1 flex items-center justify-center p-4">
          <div className="w-full max-w-2xl mx-auto border border-border rounded-lg bg-card shadow-sm overflow-hidden">
            <div className="px-6 py-4 text-center">
              <div className="mx-auto w-16 h-16 bg-amber-100 rounded-full flex items-center justify-center mb-4">
                <Trophy className="w-8 h-8 text-amber-600" />
              </div>
              <h2 className="text-2xl font-bold text-foreground">
                Quiz Completado!
              </h2>
            </div>
            <div className="p-6 text-center space-y-6">
              <div className="py-6">
                <div className="text-6xl font-bold text-primary mb-2">
                  {score}/{totalQuestions}
                </div>
                <p className="text-muted-foreground text-lg">
                  {getScoreMessage()}
                </p>
              </div>
              
              <div className="bg-secondary/50 rounded-lg p-4">
                <div className="flex justify-between text-sm text-muted-foreground mb-2">
                  <span>Correctas</span>
                  <span className="text-emerald-600 font-medium">{score}</span>
                </div>
                <div className="flex justify-between text-sm text-muted-foreground">
                  <span>Incorrectas</span>
                  <span className="text-red-600 font-medium">{totalQuestions - score}</span>
                </div>
              </div>

              <button 
                onClick={handleRestart} 
                className="w-full text-sm text-black font-semibold flex items-center justify-center gap-2 bg-gradient-to-br from-[var(--purple-accent)] to-[var(--sidebar-border)] hover:from-[var(--purple-accent)] hover:to-[var(--sidebar-border)]/85 py-3 px-6 rounded-full transition-all duration-300 ease-in-out cursor-pointer hover:shadow-lg"
              >
                <RotateCcw className="w-4 h-4" strokeWidth={2.5} />
                Reiniciar Quiz
              </button>
            </div>
          </div>
        </div>
      </main>
    )
  }

  return (
    <main className="flex-1 flex flex-col items-center">
      <div className="w-full max-w-3xl flex-1 flex items-center justify-center p-4">
        <div className="w-full">
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
              <p className="text-sm text-muted-foreground">Generando preguntas...</p>
            </div>
          ) : (
            <>
              {totalQuestions === 0 ? (
                <div className="w-full max-w-2xl mx-auto text-center">
                  <div className="border border-border rounded-lg bg-card shadow-sm p-6">
                    <p className="text-muted-foreground">No hay preguntas disponibles</p>
                  </div>
                </div>
              ) : (
              <div className="w-full mx-auto space-y-4 bg-card border border-border rounded-lg shadow-sm p-4">
                <div className="space-y-2 py-1 px-4">
                  <div className="flex justify-between items-center text-sm text-muted-foreground">
                    <span className="font-medium">Cuestionario</span>
                    <span>
                      Pregunta {currentIndex + 1} de {totalQuestions}
                    </span>
                  </div>
                  <div className="w-full h-2 bg-secondary rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-primary transition-all duration-300"
                      style={{ width: `${progress}%` }}
                    />
                  </div>
                </div>

                <QuizQuestion
                    key={currentIndex}
                    questionData={questions[currentIndex]}
                    onAnswerSelected={handleAnswerSelected}
                />

                {answeredCurrent && (
                    <div className="flex justify-end">
                    <button 
                        onClick={handleNextQuestion}
                        className="text-sm text-black font-semibold flex items-center justify-center gap-2 bg-gradient-to-br from-[var(--purple-accent)] to-[var(--sidebar-border)] hover:from-[var(--purple-accent)] hover:to-[var(--sidebar-border)]/85 py-3 px-6 rounded-full transition-all duration-300 ease-in-out cursor-pointer hover:shadow-lg"
                    >
                        {currentIndex < totalQuestions - 1 ? (
                        <>
                            Siguiente
                            <ArrowRight className="w-4 h-4" strokeWidth={2.5}/>
                        </>
                        ) : (
                        "Ver Resultados"
                        )}
                    </button>
                    </div>
                )}

                <div className="flex justify-center gap-2 pt-2">
                    {questions.map((_, index) => (
                    <div
                        key={index}
                        className={`w-2.5 h-2.5 rounded-full transition-colors ${
                        index === currentIndex
                            ? "bg-primary"
                            : index < currentIndex
                            ? "bg-primary/40"
                            : "bg-secondary"
                        }`}
                    />
                    ))}
                </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </main>
  )
}