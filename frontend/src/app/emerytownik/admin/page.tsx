import { Navbar } from "@/components/navbar";
import { API_URL } from "@/config/constants";

import { Panel } from "./panel";

// this ensures the route is marked as non-static to prevent build errors
export const dynamic = "force-dynamic";

export default async function AdminPage() {
  let data = [];
  try {
    const response = await fetch(`${API_URL}/records`, {
      cache: "no-store",
    });
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
