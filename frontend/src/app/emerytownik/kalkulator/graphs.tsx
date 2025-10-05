import { DataTable } from "@/components/data-table";
import { Spinner } from "@/components/spinner";
import { useCalculator } from "@/hooks/use-calculator";

export function Graphs() {
  const { state } = useCalculator();

  return state === "graph" ? (
    <iframe src="/pension_dashboard.html" className="h-[620px] w-10/12" />
  ) : state === "loading" ? (
    <div className="flex h-[620px] w-full items-center justify-center">
      <Spinner />
    </div>
  ) : (
    <div className="bg-gray/20 mx-20 rounded-md p-2">
      <DataTable data={state} />
    </div>
  );
}
