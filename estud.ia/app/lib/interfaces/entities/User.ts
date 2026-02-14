export default interface User {
    id: number;
    email: string;
    name: string;
    lastname: string;
    profile_image_url?: string;
    created_at: string;
    updated_at?: string | null;
}  