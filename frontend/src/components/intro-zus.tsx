"use client";

import Link from "next/link";
import React from "react";
import { motion } from "framer-motion";
import { GraduationCap, Target, TrendingUp, Wallet } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

export default function IntroZUS() {
  return (
    <div className="flex min-h-[calc(100vh-106px)] items-center justify-center bg-gradient-to-b from-white to-blue-50 p-6">
      <Card className="w-full max-w-3xl rounded-2xl shadow-lg">
        <CardContent className="space-y-6 p-8 text-center">
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-3xl font-bold"
          >
            👋 Witaj w aplikacji „Twoja Przyszłość z ZUS”
          </motion.h1>

          <p className="mx-auto max-w-2xl text-lg text-gray-600">
            Dowiedz się, jak mogą wyglądać Twoje finanse w przyszłości! Zrozum, jak Twoje
            decyzje dziś wpływają na Twoją emeryturę jutro.
          </p>

          <div className="mx-auto grid max-w-2xl gap-4 text-left sm:grid-cols-2">
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="flex items-start gap-3 rounded-xl bg-blue-50 p-4"
            >
              <GraduationCap className="h-6 w-6 text-blue-600" />
              <span>💡 Zrozum, czym są ubezpieczenia społeczne i dlaczego są ważne.</span>
            </motion.div>

            <motion.div
              whileHover={{ scale: 1.05 }}
              className="flex items-start gap-3 rounded-xl bg-blue-50 p-4"
            >
              <TrendingUp className="h-6 w-6 text-blue-600" />
              <span>📊 Zobacz, jak z czasem zmienia się wartość Twoich zarobków.</span>
            </motion.div>

            <motion.div
              whileHover={{ scale: 1.05 }}
              className="flex items-start gap-3 rounded-xl bg-blue-50 p-4"
            >
              <Wallet className="h-6 w-6 text-blue-600" />
              <span>
                💰 Sprawdź, jaką realną siłę nabywczą może mieć Twoja emerytura.
              </span>
            </motion.div>

            <motion.div
              whileHover={{ scale: 1.05 }}
              className="flex items-start gap-3 rounded-xl bg-blue-50 p-4"
            >
              <Target className="h-6 w-6 text-blue-600" />
              <span>
                🎯 Uświadom sobie, jak decyzje dziś wpływają na bezpieczeństwo finansowe
                jutro.
              </span>
            </motion.div>
          </div>

          <p className="mx-auto max-w-2xl text-gray-500">
            Nie potrzebujesz wiedzy ekonomicznej — wszystko pokazujemy{" "}
            <strong>prosto, czytelnie i wizualnie</strong>.
          </p>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
          >
            <Button asChild variant="link">
              <Link href="/emerytownik">Przejdź do kalkulatora emerytury</Link>
            </Button>
          </motion.div>

          <div className="mt-6 text-sm text-gray-400">
            ZUS – zrozumieć dziś, by być spokojnym jutro.
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
