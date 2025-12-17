"use client";

import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";

export default function PrimaryCTA() {
  const router = useRouter();
  const { user } = useAuth();

  function handleClick() {
    if (user) {
      router.push("/home/gerar-pagamento");
    } else {
      router.push("/login");
    }
  }

  return (
    <button className="primary-cta" onClick={handleClick}>
      gerar pagamento
    </button>
  );
}
