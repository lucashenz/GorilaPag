"use client";

import LoginForm from "./LoginForm";
import "@/styles/pageInicio.css";

export default function LoginPage() {
  return (
    <div className="page">
      <div className="card">
        <h1 className="title">Entrar</h1>
        <p className="subtitle">Faça login para continuar</p>
        <LoginForm />
      </div>
    </div>
  );
}
