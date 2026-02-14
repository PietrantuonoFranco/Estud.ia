import QuestionsAndAnswers from "./QuestionsAndAnswers";

export default interface Quiz {
    id: number;
    title: string;
    notebook_id: number;
    created_at?: string | null;
    updated_at?: string | null;
    questions_and_answers: QuestionsAndAnswers[];
}