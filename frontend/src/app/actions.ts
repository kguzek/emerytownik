import type { ApiResult, DetailsFormValuesWithTarget } from "@/lib/types";
import { API_URL } from "@/config/constants";

export async function generateSyntheticData(data: DetailsFormValuesWithTarget) {
  const response = await fetch(`${API_URL}/calculate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  const result = await response.json();
  if (result.error != null) {
    throw new Error(result.error);
  }
  return result as ApiResult;
}
