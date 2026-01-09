export default interface QuestionsAndAnswers {
    id: number;
    question: string;
    answer: string;
    incorrect_answers_1: string;
    incorrect_answers_2: string;
    incorrect_answers_3: string;
    quiz_id: number;
}