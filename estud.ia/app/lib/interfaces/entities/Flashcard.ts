export default interface Flashcard {
  id: number;
  notebook_id: number;
  question: string;
  answer: string;
  created_at?: string | null;
  updated_at?: string | null;
}