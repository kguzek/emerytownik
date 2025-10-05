"use client";

import Link from "next/link";

import type { AdminRecord } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/hooks/use-auth";

import { DownloadRecords } from "./download-records";

export function Panel({ data }: { data: AdminRecord[] }) {
  const auth = useAuth();

  return auth.isAuthenticated ? (
    <>
      <p>Liczba zapytań użytkowników: {data.length}</p>
      <div className="">
        <DownloadRecords data={data} filename="records.json" />
      </div>
    </>
  ) : (
    <div>
      <p>Nie masz uprawnień do przeglądania tego panelu.</p>
      <Button asChild variant="link" className="px-0">
        <Link href="/login">Zaloguj się</Link>
      </Button>
    </div>
  );
}
