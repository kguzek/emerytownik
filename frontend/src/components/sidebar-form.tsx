"use client";

import { useForm } from "react-hook-form";
import { toast } from "sonner";

import { Button } from "./ui/button";
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

interface DetailsFormValues {
  yearOfBirth: number;
  gender: "male" | "female";
  salary: number;
  employedSinceYear: number;
  expectedEmployedUntilYear: number;
  nationalRetirementAge: number;
  savings?: number;
}

export function SidebarForm() {
  const form = useForm<DetailsFormValues>({
    defaultValues: {
      yearOfBirth: 1990,
      gender: "male",
      salary: 30.5 * 178,
      employedSinceYear: 2015,
      expectedEmployedUntilYear: 2050,
      nationalRetirementAge: 67,
      savings: 10000,
    },
  });

  return (
    <Form {...form}>
      <form
        className="flex flex-col items-stretch gap-2 rounded-md bg-white p-4"
        onSubmit={form.handleSubmit(() => {
          toast.success("Dane zapisane (nie naprawdę, to tylko demo)");
        })}
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
        <Button type="submit" className="mx-auto">
          Prześlij dane
        </Button>
      </form>
    </Form>
  );
}
