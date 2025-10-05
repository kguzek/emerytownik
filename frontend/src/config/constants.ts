import type { ApiResult } from "@/lib/types";

export const USER_CREDENTIALS = {
  username: "konrad",
  password: "password",
};

export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export const API_RESULT_LABELS: Partial<
  Record<keyof ApiResult & "srednia_emerytura", string>
> = {
  emerytura_nominalna: "Emerytura nominalna",
  emerytura_urealniona: "Emerytura urealniona",
  konto: "Stan konta",
  subkonto: "Stan subkonta",
  suma_skladek: "Suma składek",
  srednia_emerytura: "Średnia emerytura",
};

export const AVERAGE_EMERYTURA = 3986.91;
