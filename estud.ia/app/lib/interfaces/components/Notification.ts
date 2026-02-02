export type NotificationType = 'success' | 'error' | 'info';

export interface Notification {
    id: number;
    title: string;
    message: string;
    type: NotificationType;
    onClose?: () => void;
}