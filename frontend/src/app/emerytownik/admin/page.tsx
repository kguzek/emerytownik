import { Navbar } from "@/components/navbar";

import { Panel } from "./panel";

export default async function AdminPage() {
  const response = await fetch("http://localhost:8000/records");
  const data = await response.json();

  return (
    <>
      <div className="px-90">
        <Navbar />
      </div>
      <div className="mt-10 flex h-full w-full flex-col gap-4 px-90">
        <h2 className="text-2xl font-bold">Panel administracyjny</h2>
        <Panel data={data} />
      </div>
    </>
  );
}
