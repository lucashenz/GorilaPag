"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import Button from "../../components/button";

export default function LoginForm() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [error, setError] = useState(null);

  const { login } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

  try {
    const response = await fetch("http://127.0.0.1:8000/v1/merchants/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email,
        password: senha
      }),
    });

    const data = await response.json(); 

    if (!response.ok) {
       setError(data?.detail?.error?.message || "Erro desconhecido");
      return;
    } 

    router.push("/dashboard");

  } catch (err) {
    console.error("Erro da API:", err);
    setError(err.message); 
  }
  };

  return (
    <form onSubmit={handleSubmit} className="login-form">
      <input
        type="email"
        placeholder="E-mail"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="login-input"
        required
      />

      <input
        type="password"
        placeholder="Senha"
        value={senha}
        onChange={(e) => setSenha(e.target.value)}
        className="login-input"
        required
      />

      {error && <p className="login-error">{error}</p>}

      <Button text="Entrar" type="submit" />
    </form>
  );
}
