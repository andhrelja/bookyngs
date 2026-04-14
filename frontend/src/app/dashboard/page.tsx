function StatCard({ title, value, subtitle }: { title: string; value: string; subtitle?: string }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6 flex flex-col justify-between">
      <h3 className="text-sm font-medium text-gray-500">{title}</h3>
      <div className="mt-2 flex items-baseline gap-2">
        <span className="text-3xl font-bold text-gray-900">{value}</span>
        {subtitle && <span className="text-sm font-medium text-green-600">{subtitle}</span>}
      </div>
    </div>
  );
}

export default function DashboardPage() {
  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">Pregled</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <StatCard title="Narudžbe danas" value="0" subtitle="+0%" />
        <StatCard title="Rezervacije ovaj tjedan" value="0" subtitle="+0%" />
        <StatCard title="Aktivne loyalty kartice" value="0" />
      </div>
      
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Nedavna aktivnost</h2>
        <div className="text-center py-12">
          <p className="text-gray-500 text-sm">Trenutačno nema novih aktivnosti.</p>
        </div>
      </div>
    </div>
  );
}
