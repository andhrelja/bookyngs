export default function PostavkePage() {
  return (
    <div className="max-w-3xl">
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">Postavke</h1>

      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden mb-6">
        <div className="px-6 py-5 border-b border-gray-200 bg-gray-50/50">
          <h2 className="text-lg font-medium text-gray-900">Podaci o tvrtki</h2>
          <p className="text-sm text-gray-500 mt-1">Osnovni podaci za račune i fiskalizaciju.</p>
        </div>
        <div className="p-6 space-y-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Naziv tvrtke</label>
              <input type="text" className="w-full rounded-lg border-gray-300 border px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="npr. Moj obrt" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">OIB</label>
              <input type="text" className="w-full rounded-lg border-gray-300 border px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="11 znamenki" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Valuta</label>
              <input type="text" className="w-full rounded-lg border-gray-300 border px-4 py-2 bg-gray-50 text-gray-500 outline-none cursor-not-allowed" value="EUR" readOnly />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">PDV (%)</label>
              <input type="text" className="w-full rounded-lg border-gray-300 border px-4 py-2 bg-gray-50 text-gray-500 outline-none cursor-not-allowed" value="25" readOnly />
            </div>
          </div>
          <div className="flex justify-end pt-4">
             <button className="bg-blue-600 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-blue-700 transition-colors">
               Spremi promjene
             </button>
          </div>
        </div>
      </div>
      
    </div>
  );
}
