import type { Metadata } from "next";
import { Space_Grotesk } from "next/font/google";

import { QueryProvider } from "@/lib/query-client";

import "./globals.css";

import { SidebarProvider } from "@/components/ui/sidebar";
import { Toaster } from "@/components/ui/sonner";
import { AuthProvider } from "@/hooks/use-auth";

const space_grotesk = Space_Grotesk({
  variable: "--font-space-grotesk",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Emerytownik ZUS",
  description: "Planuj i wizualizuj swoją emeryturę z ZUS",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <QueryProvider>
        <AuthProvider>
          <body className={`${space_grotesk.variable} font-sans antialiased`}>
            <SidebarProvider>
              {children}
              <Toaster />
            </SidebarProvider>
          </body>
        </AuthProvider>
      </QueryProvider>
    </html>
  );
}
