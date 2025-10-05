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
import { cn } from "@/lib/utils";

export function DataTable({ data }: { data: ApiResult }) {
  return (
    <Table>
      <TableCaption>Wyniki pracy</TableCaption>
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
            <TableCell className="">
              {new Intl.NumberFormat("pl-PL", {
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
