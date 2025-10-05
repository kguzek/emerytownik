"use client";

import { Download } from "lucide-react";

import type { AdminRecord } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { downloadFile } from "@/lib/download";

export function DownloadRecords({ data }: { data: AdminRecord[] }) {
  return (
    <Button
      onClick={() => {
        downloadFile(data, "wpisy_wszystkie");
      }}
    >
      <Download /> Pobierz wpisy
    </Button>
  );
}
