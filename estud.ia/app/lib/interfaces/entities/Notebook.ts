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
  date: string

  messages: Message[]
  summaries: Summary[]
  flashcards: Flashcard[]
  quizzes: Quiz[]
  sources: Source[]

  user_id: number
}