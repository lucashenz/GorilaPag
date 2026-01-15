'use client';

import { useRouter } from 'next/navigation';

export default function DashForm() {
  const router = useRouter();

  const handleClick = () => {

    router.push('/payments');
  };

  return (
    <div className="bg-gray-800 p-8 rounded-xl shadow-2xl border border-gray-700 w-full max-w-md text-center">
      <h2 className="text-2xl font-bold text-white mb-6">Pagamentos</h2>
      
      <button
        onClick={handleClick}
        className="w-full py-4 bg-purple-600 hover:bg-purple-500 text-white font-bold rounded-lg shadow-lg shadow-purple-900/50 transition-all uppercase tracking-wider"
      >
        Gerar Pagamento
      </button>
      
      <p className="mt-4 text-xs text-gray-500">
        Você será redirecionado para a página de pagamentos.
      </p>
    </div>
  );
}
