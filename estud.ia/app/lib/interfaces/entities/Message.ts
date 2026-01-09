export default interface Message {
  id: number;
  notebook_id: number;
  is_user_message: boolean;
  text: string;
}