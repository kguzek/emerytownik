import { Download } from "lucide-react";

import type { ApiResult } from "@/lib/types";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { API_RESULT_LABELS, AVERAGE_EMERYTURA } from "@/config/constants";
import { downloadFile } from "@/lib/download";
import { formatCurrency } from "@/lib/helpers";
import { cn } from "@/lib/utils";

import { Button } from "./ui/button";

const hasLabel = (key: string): key is keyof typeof API_RESULT_LABELS =>
  key in API_RESULT_LABELS;

export function DataTable({
  data,
  addAverage = false,
}: {
  data: ApiResult | Record<string, string | number>;
  addAverage?: boolean;
}) {
  const additionalEntries = addAverage
    ? [["srednia_emerytura", AVERAGE_EMERYTURA] as const]
    : [];
  return (
    <Table>
      <TableCaption>
        <div className="mb-4">Więcej danych można pobrać klikając poniższy przycisk.</div>
        <Button
          className="mx-auto w-fit"
          onClick={() => {
            downloadFile([data], "raport_1");
          }}
        >
          <Download /> Pobierz
        </Button>
      </TableCaption>
      <TableHeader>
        <TableRow>
          <TableHead>Parametr</TableHead>
          <TableHead>Wartość</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {[...Object.entries(data), ...additionalEntries]

          .filter(([key]) => hasLabel(key) || !addAverage)
          .map(([key, value], index) => (
            <TableRow
              key={key}
              className={cn(index % 2 === 0 ? "bg-white" : "bg-orange/25")}
            >
              <TableCell className="w-lg font-medium">
                {API_RESULT_LABELS[key as keyof typeof API_RESULT_LABELS] ?? key}
              </TableCell>
              <TableCell>
                {["stopa_zastapienia", "inflacja_cum"].includes(key)
                  ? `${value.toFixed(2)}%`
                  : typeof value === "number"
                    ? formatCurrency(value)
                    : value}
              </TableCell>
            </TableRow>
          ))}
      </TableBody>
    </Table>
  );
}
