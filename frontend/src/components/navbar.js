"use client";

import { useRouter } from "next/navigation";

export default function Navbar() {
  const router = useRouter();

  return (
    <header className="navbar">
      <div className="logo">
        <span className="logo-icon">🦍</span>
        <span className="logo-text">Pag</span>
      </div>

      <nav className="nav-links">
        <button className="nav-button-secondary" onClick={() => router.push("/docs")}>
          Documentação
        </button>
        <button className="nav-button-secondary" onClick={() => router.push("/about")}>
          Sobre
        </button>
        <button className="nav-button-secondary" onClick={() => router.push("/fees")}>
          Taxas
        </button>
        <button className="nav-button-secondary" onClick={() => router.push("/login")}>
          Entrar
        </button>
        <button className="nav-button" onClick={() => router.push("/register")}>
          Registrar
        </button>
      </nav>
    </header>
  );
}
