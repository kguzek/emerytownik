"use client";

import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import type { LoginFormValues } from "@/lib/types";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/hooks/use-auth";

export function SignIn() {
  const { login } = useAuth();

  const form = useForm<LoginFormValues>({
    defaultValues: {
      username: "",
      password: "",
    },
  });

  const mutation = useMutation({
    mutationFn: login,
  });

  return (
    <Form {...form}>
      <form
        className="flex flex-col items-center gap-2 rounded-lg bg-white p-6 shadow-md"
        onSubmit={form.handleSubmit((values) =>
          toast.promise(mutation.mutateAsync(values), {
            loading: "Logowanie...",
            success: "Zalogowano pomyślnie!",
            error: "Błędna nazwa użytkownika lub hasło",
          }),
        )}
      >
        Nie jesteś zalogowany 😔
        <FormField
          control={form.control}
          name="username"
          render={({ field }) => (
            <FormItem>
              <FormLabel />
              <FormControl>
                <Label className="flex flex-col items-start gap-2">
                  Nazwa użytkownika
                  <Input {...field} />
                </Label>
              </FormControl>
              <FormDescription />
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel />
              <FormControl>
                <Label className="flex flex-col items-start gap-2">
                  Nie jesteś zalogowany 😔 asło
                  <Input type="password" {...field} />
                </Label>
              </FormControl>
              <FormDescription />
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="mx-auto">
          Zaloguj się
        </Button>
      </form>
    </Form>
  );
}
