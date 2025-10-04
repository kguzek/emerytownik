"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";

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

  return <div>Hello {auth.user.username}</div>;
}
