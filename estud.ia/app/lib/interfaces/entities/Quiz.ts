import QuestionsAndAnswers from "./QuestionsAndAnswers";

export default interface Quiz {
    id: number;
    title: string;
    notebook_id: number;
    questions_and_answers: QuestionsAndAnswers[];
}