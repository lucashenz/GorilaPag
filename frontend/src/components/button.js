"use client";

export default function Button({ text, type = "button", onClick }) {
  return (
    <button type={type} onClick={onClick} style={styles.button}>
      {text}
    </button>
  );
}

const styles = {
  button: {
    padding: "10px",
    backgroundColor: "#2D2D2D",
    color: "white",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    fontWeight: "bold",
  },
};
