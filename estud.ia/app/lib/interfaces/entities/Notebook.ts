import Message from "./Message";
import Summary from "./Summary";
import Flashcard from "./Flashcard";
import Quiz from "./Quiz";


export default interface Notebook {
  id: number
  title: string
  description: string
  icon: string
  date: string
  sourcesCount: number

  messages: Message[]
  summaries: Summary[]
  flashcards: Flashcard[]
  quizzes: Quiz[]

  user_id: number
}