"use client";

import Image from "next/image";
import Navbar from "@/components/navbar";
import PrimaryCTA from "@/components/primaryCTA";
import "@/styles/pageInicio.css";

export default function HomePage() {
  return (
    <div className="home">
      <Navbar/>

      <main className="hero">
        <div className="hero-text">
          <h1>
            Sem intermediários. Apenas você e <span>a blockchain.</span>
          </h1>

          <p>
            Crie cobranças em segundos e receba direto na sua carteira, sem
            intermediários e sem burocracia.
          </p>

          <div>
          <PrimaryCTA/>
          </div>
        </div>

        <div className="hero-image">
          <Image src="/gorila.jpg" alt="GorilaPag" width={450} height={450} />
        </div>
      </main>
    </div>
  );
}
