"use client";

import { AVERAGE_EMERYTURA } from "@/config/constants";
import { useCalculator } from "@/hooks/use-calculator";
import { formatCurrency } from "@/lib/helpers";

import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";

export function RetirementPlanner() {
  const { target, setTarget, setTargetSkipped } = useCalculator();

  return (
    <div className="flex flex-col items-stretch gap-2 rounded-md bg-white p-4">
      <p>Jaka jest Twoja wymarzona emerytura?</p>
      <p>Obecna średnia emerytura wynosi {formatCurrency(AVERAGE_EMERYTURA)}</p>
      <Label className="mt-4 mb-2 flex flex-col items-start gap-1">
        Wpisz kwotę w PLN
        <Input
          value={target ?? ""}
          onChange={(event_) => {
            setTarget(
              event_.target.value === "" || isNaN(Number(event_.target.value))
                ? null
                : Number(event_.target.value),
            );
          }}
        />
      </Label>
      <div className="flex gap-2">
        <Button
          variant="outline"
          onClick={() => {
            setTarget(null);
            setTargetSkipped(true);
          }}
        >
          Pomiń
        </Button>
        <Button disabled={target == null} onClick={() => setTargetSkipped(true)}>
          Zapisz
        </Button>
      </div>
    </div>
  );
}
