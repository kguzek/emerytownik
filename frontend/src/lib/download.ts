import xlsx from "json-as-xlsx";

import type { AdminRecord, ApiResult } from "./types";

export function downloadFile(
  data: (AdminRecord | ApiResult | Record<string, string | number>)[],
  filename: string,
) {
  const settings = {
    fileName: filename, // Name of the resulting spreadsheet
    extraLength: 3, // A bigger number means that columns will be wider
    writeMode: "writeFile", // The available parameters are 'WriteFile' and 'write'. This setting is optional. Useful in such cases https://docs.sheetjs.com/docs/solutions/output#example-remote-file
    writeOptions: {}, // Style options from https://docs.sheetjs.com/docs/api/write-options
  };

  xlsx(
    data.map((item, index) => ({
      sheet: `Wyniki ${index + 1}`,
      columns: [
        { label: "Parametr", value: "parametr" },
        { label: "Wartość", value: "wartosc" },
      ],
      content: Object.entries(item).map(([key, value]) => ({
        parametr: key,
        wartosc: value,
      })),
    })),
    settings,
  );
}
