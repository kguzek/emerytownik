import { createContext, useContext, useState } from "react";

import type { ApiResult } from "@/lib/types";

type State = "graph" | "loading" | "error" | { endYear: number; data: ApiResult }[];

interface CalculatorContextType {
  state: State;
  setState: (state: State) => void;
}

const CalculatorContext = createContext<CalculatorContextType | undefined>(undefined);

export const CalculatorProvider = ({ children }: { children: React.ReactNode }) => {
  const [state, setState] = useState<State>("graph");

  return (
    <CalculatorContext.Provider value={{ state, setState }}>
      {children}
    </CalculatorContext.Provider>
  );
};

export const useCalculator = () => {
  const context = useContext(CalculatorContext);
  if (context === undefined) {
    throw new Error("useCalculator must be used within a CalculatorProvider");
  }
  return context;
};
