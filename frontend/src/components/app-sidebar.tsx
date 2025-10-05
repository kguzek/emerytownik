"use client";

import Link from "next/link";
import { Home, Settings, SquareSigma } from "lucide-react";

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { useCalculator } from "@/hooks/use-calculator";

import { RetirementPlanner } from "./retirement-planner";
import { SidebarForm } from "./sidebar-form";

// Menu items.
const items = [
  {
    title: "Strona Główna",
    url: "/",
    icon: Home,
  },
  {
    title: "Kalkulator Emerytury",
    url: "/emerytownik/kalkulator",
    icon: SquareSigma,
  },
  {
    title: "Ustawienia",
    url: "#",
    icon: Settings,
  },
];

export function AppSidebar() {
  const { targetSkipped } = useCalculator();
  return (
    <Sidebar>
      <SidebarContent className="bg-gray/30">
        <SidebarGroup>
          <SidebarGroupLabel>Nawigacja</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <Link href={item.url}>
                      <item.icon />
                      <span>{item.title}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
        <SidebarGroup>
          <SidebarGroupLabel>Dane użytkownika</SidebarGroupLabel>
          <SidebarGroupContent>
            {targetSkipped ? <SidebarForm /> : <RetirementPlanner />}
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
