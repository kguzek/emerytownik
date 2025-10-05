import { Navbar } from "@/components/navbar";
import { API_URL } from "@/config/constants";

import { Panel } from "./panel";

export default async function AdminPage() {
  let data = [];
  try {
    const response = await fetch(`${API_URL}/records`, { next: { revalidate: 5 } });
    data = await response.json();
  } catch (error) {
    console.error("Error fetching data:", error);
  }

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
