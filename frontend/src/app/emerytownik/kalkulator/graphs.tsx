import { DataTable } from "@/components/data-table";
import { Spinner } from "@/components/spinner";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useCalculator } from "@/hooks/use-calculator";
import { cn } from "@/lib/utils";

function FullscreenSpinner({ label }: { label: string }) {
  return (
    <div className="flex h-[620px] w-full items-center justify-center">
      <Spinner label={label} />
    </div>
  );
}

export function Graphs() {
  const { state } = useCalculator();

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
  );
}
