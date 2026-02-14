import Message from "./Message";
import Summary from "./Summary";
import Flashcard from "./Flashcard";
import Quiz from "./Quiz";
import Source from "./Source";

export default interface Notebook {
  id: number
  title: string
  description: string
  icon: string
  created_at?: string | null
  updated_at?: string | null

  messages: Message[]
  summaries: Summary[]
  flashcards: Flashcard[]
  quizzes: Quiz[]
  sources: Source[]

  user_id: number
}