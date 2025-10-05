import { createContext, useContext, useState } from "react";

import type { ApiResult } from "@/lib/types";

type State = "graph" | "loading" | "error" | { endYear: number; data: ApiResult }[];

interface CalculatorContextType {
  state: State;
  setState: (state: State) => void;
  target: number | null;
  setTarget: (target: number | null) => void;
  targetSkipped: boolean;
  setTargetSkipped: (skipped: boolean) => void;
}

const CalculatorContext = createContext<CalculatorContextType | undefined>(undefined);

export const CalculatorProvider = ({ children }: { children: React.ReactNode }) => {
  const [state, setState] = useState<State>("graph");
  const [target, setTarget] = useState<number | null>(null);
  const [targetSkipped, setTargetSkipped] = useState(false);

  return (
    <CalculatorContext.Provider
      value={{ state, setState, target, setTarget, targetSkipped, setTargetSkipped }}
    >
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
