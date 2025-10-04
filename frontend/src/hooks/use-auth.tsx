"use client";

import type { ReactNode } from "react";
import { useRouter } from "next/navigation";
import { createContext, useContext, useState } from "react";
import { toast } from "sonner";

import type { LoginFormValues } from "@/lib/types";
import { USER_CREDENTIALS } from "@/config/constants";

interface User {
  username: string;
}

interface AuthContextBase {
  login: (values: LoginFormValues) => Promise<void>;
  logout: () => void;
}

interface AuthContextLoggedIn extends AuthContextBase {
  isAuthenticated: true;
  user: User;
}

interface AuthContextLoggedOut extends AuthContextBase {
  isAuthenticated: false;
  user: null;
}

type AuthContextType = AuthContextLoggedIn | AuthContextLoggedOut;

const AuthContext = createContext<AuthContextType | null>(null);

export function useAuth() {
  const context = useContext(AuthContext);

  if (context == null) {
    throw new Error("useAuth must be used within an AuthProvider");
  }

  return context;
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();

  async function login(values: LoginFormValues) {
    if (
      values.username === USER_CREDENTIALS.username &&
      values.password === USER_CREDENTIALS.password
    ) {
      toast.success("Zalogowano pomyślnie!");
      setUser({ username: values.username });
      router.push("/");
      return;
    }

    await new Promise<void>((resolve) => {
      setTimeout(resolve, Math.random() * 1000 + 500);
    });
    throw new Error("Invalid credentials");
  }

  function logout() {
    setUser(null);
    toast.success("Wylogowano pomyślnie!");
  }

  return (
    <AuthContext.Provider
      value={
        {
          isAuthenticated: user != null,
          user,
          login,
          logout,
        } as AuthContextType
      }
    >
      {children}
    </AuthContext.Provider>
  );
}
