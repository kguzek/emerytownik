"use client";

import { AppSidebar } from "@/components/app-sidebar";
import { Navbar } from "@/components/navbar";
import { RetirementPlanner } from "@/components/retirement-planner";
import { Button } from "@/components/ui/button";
import { SidebarProvider } from "@/components/ui/sidebar";
import { CalculatorProvider } from "@/hooks/use-calculator";

import { Graphs } from "./graphs";

export default function Emerytownik() {
  return (
    <CalculatorProvider>
      <SidebarProvider>
        <AppSidebar />
        <div className="w-full">
          <Navbar />

          <div className="p-10">
            <h1 className="text-4xl font-semibold">Witaj w Emerytowniku ZUS</h1>
            Uzupełnij dane po lewej, potem kliknij przycisk{" "}
            <Button disabled className="cursor-not-allowed">
              Oblicz emeryturę
            </Button>
            .
          </div>
          <Graphs />
        </div>
      </SidebarProvider>
    </CalculatorProvider>
  );
}
