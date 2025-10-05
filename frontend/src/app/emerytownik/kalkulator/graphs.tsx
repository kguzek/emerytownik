import { useEffect, useState } from "react";

import type { ApiResult, DetailsFormValues } from "@/lib/types";
import { generateSyntheticData } from "@/app/actions";
import { DataTable } from "@/components/data-table";
import { Spinner } from "@/components/spinner";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useCalculator } from "@/hooks/use-calculator";
import { formatCurrency } from "@/lib/helpers";
import { conjugateNumeric } from "@/lib/polish";
import { cn } from "@/lib/utils";

function FullscreenSpinner({ label }: { label: string }) {
  return (
    <div className="flex h-[620px] w-full items-center justify-center">
      <Spinner label={label} />
    </div>
  );
}
export function Graphs() {
  const { state, target, details, setTargetSkipped } = useCalculator();
  const [calculatedYears, setCalculatedYears] = useState<number | null>(null);
  const userDetails = details as DetailsFormValues;

  async function calculateYears(data: ApiResult): Promise<void> {
    for (let diff = 1; diff <= 120; diff++) {
      const res = await generateSyntheticData({
        ...data,
        targetEmerytura: target,
        ...userDetails,
        expectedEmployedUntilYear: userDetails.expectedEmployedUntilYear + diff,
        ignore: "true",
      });
      if (res.emerytura_nominalna >= target!) {
        setCalculatedYears(diff);
        return;
      }
    }
    setCalculatedYears(-1);
  }

  useEffect(() => {
    setCalculatedYears(null);
  }, [target]);

  useEffect(() => {
    if (!Array.isArray(state) || calculatedYears != null) {
      return;
    }

    calculateYears(state[0].data);
  }, [state, calculatedYears]);

  return state === "graph" ? (
    <>
      <iframe src="/pension_dashboard.html" className={cn("h-[620px] w-10/12")} />
    </>
  ) : state === "loading" ? (
    <FullscreenSpinner label="Trwa przetwarzanie..." />
  ) : state === "error" ? (
    <div className="flex h-[620px] w-full flex-col items-center justify-center">
      <p>Wystąpił błąd podczas generowania danych.</p>
      <p>Proszę spróbuj ponownie.</p>
    </div>
  ) : (
    <div>
      <div className="bg-gray/20 mx-20 rounded-md p-2">
        <Tabs
          defaultValue={String(Math.min(...state.map((data) => data.endYear)))}
          className=""
        >
          <TabsList>
            {state.map((data) => (
              <TabsTrigger key={`tab-${data.endYear}`} value={String(data.endYear)}>
                Emerytura w roku {data.endYear}
              </TabsTrigger>
            ))}
          </TabsList>
          {state.map((data) => (
            <TabsContent key={`table-${data.endYear}`} value={String(data.endYear)}>
              <DataTable data={data.data} />
            </TabsContent>
          ))}
        </Tabs>
      </div>
      <div className="mx-20 mt-10">
        {target == null ? null : (
          <div>
            {state[0].data.emerytura_nominalna >= target ? (
              <div>
                Brawo! Według prognozy osiągniesz swój cel emerytalny w wysokości {target}{" "}
                zł.
              </div>
            ) : calculatedYears == null ? (
              <Spinner label="Trwa obliczanie..." />
            ) : calculatedYears === -1 ? (
              <div>
                Nie udało się obliczyć wymaganej ilości lat do przepracowania, aby uzyskać
                Twój cel. Proszę spróbować ponownie innymi wartościami.
              </div>
            ) : (
              <div>
                Aby spełnić swój cel emerytalny w wysokości {formatCurrency(target)},
                musisz przepracować{" "}
                {conjugateNumeric(
                  calculatedYears,
                  "rok więcej",
                  "lata więcej",
                  "dodatkowych lat",
                )}
                , czyli do roku {userDetails.expectedEmployedUntilYear + calculatedYears}.
              </div>
            )}
          </div>
        )}
        <Button
          className="mt-4"
          onClick={() => {
            setTargetSkipped(false);
          }}
        >
          Zmień cel emerytalny
        </Button>
      </div>
    </div>
  );
}
