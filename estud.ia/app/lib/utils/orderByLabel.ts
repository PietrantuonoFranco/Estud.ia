export function getOrderByLabel(orderBy: "most-recently" | "title"): string {
  const labels: Record<"most-recently" | "title", string> = {
    "most-recently": "Más reciente",
    "title": "Título"
  };

  return labels[orderBy];
}
