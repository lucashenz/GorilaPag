"use client";

import { useState } from "react";
import "@/styles/pageInicio.css";

export default function PagForm() {
  const [valor, setValor] = useState("");          // para exibir formatado
  const [valorNumber, setValorNumber] = useState(0); // para enviar para a API
  const [token, setToken] = useState("");
  const [network, setNetwork] = useState("");
  const [wallet, setWallet] = useState("");
  const [loading, setLoading] = useState(false);
  const [paymentUrl, setPaymentUrl] = useState(null);
  const [error, setError] = useState(null);

  const TOKEN_NETWORKS = {
    USDT: ["ETH", "BSC", "POLYGON"],
    USDC: ["ETH", "POLYGON"],
    ETH: ["ETH"],
    BTC: ["BTC"],
  };

  // validação simples
  const isValid =
    valorNumber > 0 &&
    token.trim().length > 0 &&
    wallet.trim().length > 0 &&
    network.trim().length > 0;

  // formata USD para exibição
  function formatUSD(value) {
    const numeric = value.replace(/[^\d]/g, "");
    const number = Number(numeric) / 100;
    return `$${number.toFixed(2)}`;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!isValid) return;

    setLoading(true);
    setError(null);
    setPaymentUrl(null);

    try {
      const accessToken = localStorage.getItem("access_token");
      console.log("Access token:", accessToken);

      // ajuste aqui se estiver usando proxy Next.js
      const response = await fetch("/api/v1/merchants/payments", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
          Valor: valorNumber,
          token_recebido: token,
          rede: network,
          wallet_recebimento: wallet,
          expires_in: 900, // 15 minutos
        }),
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => null);
        throw new Error(errData?.error?.message || "Erro ao criar cobrança");
      }

      const data = await response.json();
      setPaymentUrl(data.link || null); // pega link do JSON retornado

    } catch (err) {
      console.error("Erro ao gerar pagamento:", err);
      setError(err.message || "Erro ao gerar cobrança. Verifique os dados.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card">
      <h1 className="title">Criar Pagamento</h1>
      <p className="subtitle">
        Informe os dados para gerar a cobrança cripto
      </p>

      <form className="login-form" onSubmit={handleSubmit}>

        <select
          className="login-input"
          value={token}
          onChange={(e) => setToken(e.target.value)}
          required
        >
          <option value="">Selecione o token</option>
          <option value="USDT">USDT</option>
          <option value="USDC">USDC</option>
          <option value="ETH">ETH</option>
          <option value="BTC">BTC</option>
        </select>

        <select
          className="login-input"
          value={network}
          onChange={(e) => setNetwork(e.target.value)}
          disabled={!token}
          required
        >
          <option value="">Selecione a rede</option>
          {token &&
            TOKEN_NETWORKS[token]?.map((net) => (
              <option key={net} value={net}>
                {net}
              </option>
            ))}
        </select>

        <input
          type="text"
          value={valor}
          onChange={(e) => {
            const numeric = e.target.value.replace(/[^\d]/g, "");
            const number = Number(numeric) / 100;
            setValorNumber(number);
            setValor(`$${number.toFixed(2)}`);
          }}
          placeholder="$0.00"
          required
        />

        <input
          type="text"
          placeholder="Carteira de recebimento"
          className="login-input"
          value={wallet}
          onChange={(e) => setWallet(e.target.value)}
          required
        />

        <button
          type="submit"
          className="button-login"
          disabled={!isValid || loading}
        >
          {loading ? "Gerando..." : "Gerar Pagamento"}
        </button>
      </form>

      {error && (
        <p style={{ color: "red", marginTop: 16, fontSize: 14 }}>
          {error}
        </p>
      )}

      {paymentUrl && (
        <div style={{ marginTop: 20 }}>
          <p style={{ fontSize: 13, marginBottom: 6 }}>
            Link de pagamento:
          </p>
          <a
            href={paymentUrl}
            target="_blank"
            rel="noreferrer"
            style={{
              fontSize: 13,
              wordBreak: "break-all",
              color: "#5b2dab",
              textDecoration: "underline",
            }}
          >
            {paymentUrl}
          </a>
        </div>
      )}
    </div>
  );
}
