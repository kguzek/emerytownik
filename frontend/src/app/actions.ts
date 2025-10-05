"use server";

import type { ApiResult, DetailsFormValues } from "@/lib/types";

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
