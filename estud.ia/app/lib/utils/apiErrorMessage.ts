import axios from "axios";

type ApiErrorData = {
  detail?: string;
  message?: string;
};

const DEFAULT_PERMISSION_MESSAGE = "No tienes permiso para realizar esta accion.";

export function getPermissionErrorMessage(error: unknown): string | null {
  if (!axios.isAxiosError(error)) {
    return null;
  }

  const status = error.response?.status;
  if (status !== 401 && status !== 403) {
    return null;
  }

  const data = error.response?.data as ApiErrorData | undefined;
  const detail = typeof data?.detail === "string" ? data.detail : null;
  const message = typeof data?.message === "string" ? data.message : null;

  return detail || message || DEFAULT_PERMISSION_MESSAGE;
}
