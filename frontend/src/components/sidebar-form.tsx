"use client";

import { useForm } from "react-hook-form";

import type { DetailsFormValues } from "@/lib/types";
import { generateSyntheticData } from "@/app/actions";
import { useCalculator } from "@/hooks/use-calculator";

import { Button } from "./ui/button";
import { Checkbox } from "./ui/checkbox";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "./ui/form";
import { Input } from "./ui/input";
import { Label } from "./ui/label";

export function SidebarForm() {
  const { setState } = useCalculator();

  const form = useForm<DetailsFormValues>({
    defaultValues: {
      yearOfBirth: 1990,
      gender: "male",
      salary: 30.5 * 178,
      employedSinceYear: 2015,
      expectedEmployedUntilYear: 2050,
      nationalRetirementAge: 67,
      savings: 10000,
      allowAbsences: false,
    },
  });

  async function handleSubmit(data: DetailsFormValues) {
    setState("loading");
    const result = await generateSyntheticData(data);
    console.log({ result });
    setState("calculate");
  }

  return (
    <Form {...form}>
      <form
        className="flex flex-col items-stretch gap-2 rounded-md bg-white p-4"
        onSubmit={form.handleSubmit(handleSubmit)}
      >
        <FormField
          control={form.control}
          name="yearOfBirth"
          render={({ field }) => (
            <FormItem>
              <FormLabel />
              <FormControl>
                <Label className="flex flex-col items-start gap-2">
                  Rok urodzenia
                  <Input type="number" min={1900} step={1} required {...field} />
                </Label>
              </FormControl>
              <FormDescription />
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="employedSinceYear"
          render={({ field }) => (
            <FormItem>
              <FormLabel />
              <FormControl>
                <Label className="flex flex-col items-start gap-2">
                  Rok rozpoczęcia pracy
                  <Input type="number" min={1900} step={1} required {...field} />
                </Label>
              </FormControl>
              <FormDescription />
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="salary"
          render={({ field }) => (
            <FormItem>
              <FormLabel />
              <FormControl>
                <Label className="flex flex-col items-start gap-2">
                  Wysokość miesięcznego wynagrodzenia (brutto, zł)
                  <Input type="number" min={0} step={0.01} required {...field} />
                </Label>
              </FormControl>
              <FormDescription />
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="expectedEmployedUntilYear"
          render={({ field }) => (
            <FormItem>
              <FormLabel />
              <FormControl>
                <Label className="flex flex-col items-start gap-2">
                  Przewidywany rok zakończenia pracy
                  <Input type="number" min={1900} step={1} required {...field} />
                </Label>
              </FormControl>
              <FormDescription />
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="nationalRetirementAge"
          render={({ field }) => (
            <FormItem>
              <FormLabel />
              <FormControl>
                <Label className="flex flex-col items-start gap-2">
                  Przewidywany wiek emerytalny
                  <Input type="number" min={50} max={100} step={1} required {...field} />
                </Label>
              </FormControl>
              <FormDescription />
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="savings"
          render={({ field }) => (
            <FormItem>
              <FormLabel />
              <FormControl>
                <Label className="flex flex-col items-start gap-2">
                  Oszczędności na start (opcjonalne, zł)
                  <Input type="number" min={0} step={1} {...field} />
                </Label>
              </FormControl>
              <FormDescription />
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="allowAbsences"
          render={({ field }) => (
            <FormItem>
              <FormLabel />
              <FormControl>
                <Label className="flex items-start gap-2">
                  <Checkbox checked={field.value} onCheckedChange={field.onChange} />
                  Uwzględnij możliwość zwolnień lekarskich
                </Label>
              </FormControl>
              <FormDescription />
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="mx-auto">
          Oblicz emeryturę
        </Button>
      </form>
    </Form>
  );
}
