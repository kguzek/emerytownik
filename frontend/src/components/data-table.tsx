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

export function DataTable({ data }: { data: ApiResult }) {
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
        {[...Object.entries(data), ["srednia_emerytura", AVERAGE_EMERYTURA] as const]
          .filter(([key]) => hasLabel(key))
          .map(([key, value], index) =>
            hasLabel(key) ? (
              <TableRow
                key={key}
                className={cn(index % 2 === 0 ? "bg-white" : "bg-orange/25")}
              >
                <TableCell className="w-lg font-medium">
                  {API_RESULT_LABELS[key]}
                </TableCell>
                <TableCell>
                  {["stopa_zastapienia", "inflacja_cum"].includes(key)
                    ? `${value.toFixed(2)}%`
                    : formatCurrency(value)}
                </TableCell>
              </TableRow>
            ) : null,
          )}
      </TableBody>
    </Table>
  );
}
