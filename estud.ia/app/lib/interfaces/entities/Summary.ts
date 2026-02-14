export default interface Summary {
  id: number;
  title: string;
  text: string;
  notebook_id: number;
  created_at?: string | null;
  updated_at?: string | null;
}