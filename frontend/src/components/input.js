export default function Input({ label, ...props }) {
  return (
    <div className="flex flex-col">
      <label className="mb-1 font-medium">{label}</label>
      <input
        {...props}
        className="border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>
  );
}
