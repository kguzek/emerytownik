"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Toaster } from "sonner";

import { AppSidebar } from "@/components/app-sidebar";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { useAuth } from "@/hooks/use-auth";

export default function Home() {
  const auth = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!auth.isAuthenticated) {
      console.log("No session, redirecting to login");
      router.push("/login");
    }
  }, [auth]);

  if (!auth.isAuthenticated) {
    return null;
  }

  return (
    <>
      <AppSidebar />
      <main>
        <SidebarTrigger />
        <div className="p-10">Hello {auth.user.username}</div>
      </main>
    </>
  );
}
