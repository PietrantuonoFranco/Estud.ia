export default function formatRelativeDate(dateStr: string): string {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    const diffMonths = Math.floor(diffDays / 30);
    const diffYears = Math.floor(diffMonths / 12);

    if (diffDays === 0) {
      return "Hoy";
    } else if (diffDays === 1) {
      return "Hace 1 día";
    } else if (diffDays < 30) {
      return `Hace ${diffDays} días`;
    } else if (diffMonths === 1) {
      return "Hace 1 mes";
    } else if (diffMonths < 12) {
      return `Hace ${diffMonths} meses`;
    } else if (diffYears === 1) {
      return "Hace 1 año";
    } else {
      return `Hace ${diffYears} años`;
    }
};