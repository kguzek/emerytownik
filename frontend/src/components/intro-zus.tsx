"use client";

import Link from "next/link";
import React from "react";
import { motion } from "framer-motion";
import { GraduationCap, Target, TrendingUp, Wallet } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const cardVariants = {
  hiddenLeft: { opacity: 0, x: -50 },
  hiddenRight: { opacity: 0, x: 50 },
  visible: { opacity: 1, x: 0 },
};

export default function IntroZUS() {
  const cards = [
    {
      icon: <GraduationCap className="h-6 w-6 text-blue-600" />,
      text: "💡 Zrozum, czym są ubezpieczenia społeczne i dlaczego są ważne.",
    },
    {
      icon: <TrendingUp className="h-6 w-6 text-blue-600" />,
      text: "📊 Zobacz, jak z czasem zmienia się wartość Twoich zarobków.",
    },
    {
      icon: <Wallet className="h-6 w-6 text-blue-600" />,
      text: "💰 Sprawdź, jaką realną siłę nabywczą może mieć Twoja emerytura.",
    },
    {
      icon: <Target className="h-6 w-6 text-blue-600" />,
      text: "🎯 Uświadom sobie, jak decyzje dziś wpływają na bezpieczeństwo finansowe jutro.",
    },
  ];

  return (
    <div className="flex min-h-[calc(100vh-106px)] items-center justify-center bg-gradient-to-b from-white to-blue-50 p-6">
      <Card className="w-full max-w-3xl rounded-2xl shadow-lg">
        <CardContent className="space-y-6 p-8 text-center">
          {/* Heading */}
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-3xl font-bold"
          >
            👋 Witaj w aplikacji „Emerytownik ZUS”
          </motion.h1>

          {/* First button */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <Button asChild variant="link">
              <Link href="/emerytownik">Przejdź do kalkulatora emerytury</Link>
            </Button>
          </motion.div>

          {/* Intro paragraph */}
          <motion.p
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="mx-auto max-w-2xl text-lg text-gray-600"
          >
            Dowiedz się, jak mogą wyglądać Twoje finanse w przyszłości! Zrozum, jak Twoje
            decyzje dziś wpływają na Twoją emeryturę jutro.
          </motion.p>

          {/* Cards */}
          <div className="mx-auto grid max-w-2xl gap-4 text-left sm:grid-cols-2">
            {cards.map((card, index) => (
              <motion.div
                key={index}
                initial={index % 2 === 0 ? { opacity: 0, x: -50 } : { opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.6 + index * 0.2 }}
                whileHover={{ scale: 1.05 }}
                className="bg-blue/15 flex items-start gap-3 rounded-xl p-4"
              >
                {card.icon}
                <span>{card.text}</span>
              </motion.div>
            ))}
          </div>

          {/* "Nie potrzebujesz wiedzy..." paragraph */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.6 }}
            className="mx-auto max-w-2xl text-gray-500"
          >
            Nie potrzebujesz wiedzy ekonomicznej — wszystko pokazujemy{" "}
            <strong>prosto, czytelnie i wizualnie</strong>.
          </motion.p>

          {/* Main "Rozpocznij" button */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.8 }}
          >
            <Button className="rounded-xl px-10 py-8 text-3xl" size="lg" asChild>
              <Link href="/emerytownik">Rozpocznij</Link>
            </Button>
          </motion.div>

          {/* Footer text */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 2.4, duration: 1 }}
            className="mt-6 text-sm text-gray-400"
          >
            ZUS – zrozumieć dziś, by być spokojnym jutro.
          </motion.div>
        </CardContent>
      </Card>
    </div>
  );
}
