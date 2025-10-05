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
}
