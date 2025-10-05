"use server";

import type { DetailsFormValues } from "@/lib/types";

interface ApiResult {
  S: number;
  emerytura_nominalna: number;
  emerytura_urealniona: number;
  inflacja_cum: number;
  konto: number;
  minimalna_emerytura: number;
  stopa_zastapienia: number;
  subkonto: number;
  suma_skladek: number;
}

export async function generateSyntheticData(data: DetailsFormValues) {
  const response = await fetch("http://localhost:8000/calculate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  const result = await response.json();
  return result as ApiResult;
}
