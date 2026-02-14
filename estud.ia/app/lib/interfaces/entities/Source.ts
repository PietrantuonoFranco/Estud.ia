export default interface Source {
  id: number;
  name: string;
  notebook_id: number;
  created_at?: string | null;
  updated_at?: string | null;
}