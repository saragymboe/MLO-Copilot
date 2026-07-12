import { createContext, useContext, useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";
import { getCurrentUser, signInWithRedirect, signOut } from "@aws-amplify/auth";
import { configureAuth } from "./amplify";
import type { AuthUser } from "../types";

interface AuthContextValue {
  user: AuthUser | null;
  loading: boolean;
  signIn: () => Promise<void>;
  signOutUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    configureAuth();
    const loadSession = async () => {
      try {
        const currentUser = await getCurrentUser();
        setUser({
          username: currentUser.username,
          email: currentUser.signInDetails?.loginId || currentUser.username,
        });
      } catch {
        setUser(null);
      } finally {
        setLoading(false);
      }
    };
    loadSession();
  }, []);

  const signIn = async () => {
    await signInWithRedirect();
  };

  const signOutUser = async () => {
    await signOut();
    setUser(null);
  };

  const value = useMemo(
    () => ({ user, loading, signIn, signOutUser }),
    [user, loading],
  );
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
}
