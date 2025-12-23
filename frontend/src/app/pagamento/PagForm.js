"use client";

import { useState } from "react";
import "@/styles/pageInicio.css";

export default function PagForm() {
  const [valor, setValor] = useState("");
  const [token, setToken] = useState("");
  const [wallet, setWallet] = useState("");
  const [loading, setLoading] = useState(false);
  const [paymentUrl, setPaymentUrl] = useState(null);
  const [error, setError] = useState(null);

  const isValid =
    Number(valor) > 0 &&
    token.trim().length > 0 &&
    wallet.trim().length > 0;

  async function handleSubmit(e) {
    e.preventDefault();
    if (!isValid) return;

    setLoading(true);
    setError(null);

    try {
      const accessToken = localStorage.getItem("access_token");

      const response = await fetch(
        "http://localhost:8000/v1/merchants/payments",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
          },
          body: JSON.stringify({
            Valor: Number(valor),
            descricao: `Pagamento em ${token}`,
            token_recebido: token,
            wallet_recebimento: wallet,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Erro ao criar cobrança");
      }

      const data = await response.json();
      setPaymentUrl(data.payment_url);
    } catch (err) {
      setError("Erro ao gerar cobrança. Verifique os dados.");
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
        <input
          type="number"
          min="0"
          step="any"
          placeholder="Valor"
          className="login-input"
          value={valor}
          onChange={(e) => setValor(e.target.value)}
          required
        />

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
