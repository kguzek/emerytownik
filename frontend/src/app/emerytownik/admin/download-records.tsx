"use client";

import { Download } from "lucide-react";

import type { AdminRecord } from "@/lib/types";
import { Button } from "@/components/ui/button";

export function DownloadRecords({
  data,
  filename,
}: {
  data: AdminRecord[];
  filename: string;
}) {
  const handleDownload = () => {
    // Convert JSON object to a string
    const jsonStr = JSON.stringify(data, null, 2);

    // Create a Blob with MIME type application/json
    const blob = new Blob([jsonStr], { type: "application/json" });

    // Create a temporary link element
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = filename;

    // Trigger click to download
    link.click();

    // Clean up
    URL.revokeObjectURL(link.href);
  };

  return (
    <Button onClick={handleDownload}>
      <Download /> Pobierz wpisy
    </Button>
  );
}
