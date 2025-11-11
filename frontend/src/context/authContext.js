"use client";
import { createContext, useState } from "react";

export const AuthContext = createContext({
  user: null,
  login: async () => {},
  logout: () => {},
});

export default function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  const login = async (email, password) => {
    // Aqui você faria fetch para a API
    console.log("Login:", email, password);
    setUser({ email });
  };

  const logout = () => setUser(null);

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
