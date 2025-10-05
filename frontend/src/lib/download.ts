import xlsx from "json-as-xlsx";

import type { ApiResult } from "./types";

let data = [
  {
    sheet: "Adults",
    columns: [
      { label: "User", value: "user" }, // Top level data
      { label: "Age", value: " years" }, // Custom format
      { label: "Phone", value: "telefon" }, // Run functions
    ],
    content: [
      { user: "Andrea", age: 20, more: { phone: "11111111" } },
      { user: "Luis", age: 21, more: { phone: "12345678" } },
    ],
  },
  {
    sheet: "Children",
    columns: [
      { label: "User", value: "user" }, // Top level data
      { label: "Age", value: "age", format: '# "years"' }, // Column format
      { label: "Phone", value: "more.phone", format: "(###) ###-####" }, // Deep props and column format
    ],
    content: [
      { user: "Manuel", age: 16, more: { phone: 9999999900 } },
      { user: "Ana", age: 17, more: { phone: 8765432135 } },
    ],
  },
];

let settings = {
  fileName: "raport_1", // Name of the resulting spreadsheet
  extraLength: 3, // A bigger number means that columns will be wider
  writeMode: "writeFile", // The available parameters are 'WriteFile' and 'write'. This setting is optional. Useful in such cases https://docs.sheetjs.com/docs/solutions/output#example-remote-file
  writeOptions: {}, // Style options from https://docs.sheetjs.com/docs/api/write-options
};

export function downloadFile(data: ApiResult[]) {
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
