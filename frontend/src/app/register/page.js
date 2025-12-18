"use client";

import RegisterForm from "./RegisterForm";
import "@/styles/pageInicio.css";

export default function RegisterPage() {
  return (
    <div className="page">
      <div className="card">
        <h1 className="title">Registrar</h1>
        <p className="subtitle">Crie sua conta para continuar</p>
        <RegisterForm />
      </div>
    </div>
  );
}
