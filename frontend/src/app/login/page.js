"use client";

import LoginForm from "./LoginForm";

export default function LoginPage() {
  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Entrar no GorilaPag 🦍</h1>
      <LoginForm />
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    height: "100vh",
    backgroundColor: "#707070ff",
  },
  title: {
    fontSize: "2rem",
    marginBottom: "20px",
  },
};
