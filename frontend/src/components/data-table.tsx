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
import { downloadFile } from "@/lib/download";
import { cn } from "@/lib/utils";

import { Button } from "./ui/button";

export function DataTable({ data }: { data: ApiResult }) {
  return (
    <Table>
      <TableCaption>
        <Button
          className="mx-auto w-fit"
          onClick={() => {
            downloadFile([data]);
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
        {Object.entries(data).map(([key, value], index) => (
          <TableRow
            key={key}
            className={cn(index % 2 === 0 ? "bg-white" : "bg-orange/25")}
          >
            <TableCell className="w-lg font-medium">{key}</TableCell>
            <TableCell>
              {["stopa_zastapienia", "inflacja_cum"].includes(key)
                ? `${value.toFixed(2)}%`
                : new Intl.NumberFormat("pl-PL", {
                    style: "currency",
                    currency: "PLN",
                  }).format(value)}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
