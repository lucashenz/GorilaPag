"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import Button from "../../components/button";

export default function RegisterForm() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [callbackUrl, setCallbackUrl] = useState("");
  const [wallet, setWallet] = useState("");
  const [error, setError] = useState(null);

  const { register } = useAuth(); 
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {

      const response = await fetch("http://127.0.0.1:8000/v1/merchants/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password: senha,
          callback_url_default: callbackUrl,               
          wallet_address: wallet    
        }),
      });

      if (!response.ok) {
        throw new Error("Erro ao cadastrar");
      }

      router.push("/login");

    } catch (err) {
      setError("Erro ao cadastrar. Verifique os dados e tente novamente.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="register-form">
      <input
        type="email"
        placeholder="E-mail"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="register-input"
        required
      />

      <input
        type="password"
        placeholder="Senha"
        value={senha}
        onChange={(e) => setSenha(e.target.value)}
        className="register-input"
        required
      />

      <input
        type="url"
        placeholder="URL de callback"
        value={callbackUrl}
        onChange={(e) => setCallbackUrl(e.target.value)}
        className="register-input"
        required
      />

      <input
        type="text"
        placeholder="Endereço da wallet"
        value={wallet}
        onChange={(e) => setWallet(e.target.value)}
        className="register-input"
        required
      />



      {error && <p className="register-error">{error}</p>}

      <Button text="Cadastrar" type="submit" />
    </form>
  );
}
