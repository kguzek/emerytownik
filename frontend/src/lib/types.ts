export interface LoginFormValues {
  username: string;
  password: string;
}

export interface DetailsFormValues {
  yearOfBirth: number;
  gender: "male" | "female";
  salary: number;
  employedSinceYear: number;
  expectedEmployedUntilYear: number;
  nationalRetirementAge: number;
  savings?: number;
  allowAbsences: boolean;
  postCode?: string;
  ignore: "true" | "false";
}

export interface ApiResult {
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

export type AdminRecord = ApiResult & {
  generated_at: string;
} & DetailsFormValues;

export interface DetailsFormValuesWithTarget extends DetailsFormValues {
  targetEmerytura: number | null;
}
