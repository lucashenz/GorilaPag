"use client";

import Image from "next/image";
import LoginForm from "./LoginForm";
import "@/styles/pageInicio.css";

export default function LoginPage() {
  return (
    <div className="page">
      <div className="card login-card">
        
        {/* Logo / Mascote */}
        <div className="login-logo">
          <Image
            src="/gorila.jpg"
            alt="GorilaPag"
            width={72}
            height={72}
          />
        </div>

        <h1 className="title">Entrar</h1>
        <p className="subtitle">Faça login para continuar</p>

        <LoginForm />
      </div>
    </div>
  );
}
