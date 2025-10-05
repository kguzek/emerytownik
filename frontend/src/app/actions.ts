"use server";

import type { ApiResult, DetailsFormValues } from "@/lib/types";

export async function generateSyntheticData(data: DetailsFormValues) {
  console.log("fetching with", data);
  const response = await fetch("http://localhost:8000/calculate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  const result = await response.json();
  console.log("result:", result);
  if (result.error != null) {
    throw new Error(result.error);
  }
  return result as ApiResult;
}
