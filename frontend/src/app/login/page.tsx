export default function LoginPage() {
  const kratosUrl = process.env.NEXT_PUBLIC_KRATOS_URL ?? "http://localhost:4433";

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white rounded-2xl border border-gray-200 p-8 w-full max-w-sm shadow-sm">
        <div className="mb-8 text-center">
          <h1 className="text-2xl font-bold text-blue-700">bookyngs</h1>
          <p className="mt-2 text-sm text-gray-500">Prijavite se u administratorski panel</p>
        </div>
        <a
          href={`${kratosUrl}/self-service/login/browser`}
          className="block w-full bg-blue-600 text-white text-center py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
        >
          Prijava
        </a>
        <p className="mt-4 text-center text-xs text-gray-400">
          Nemate račun?{" "}
          <a
            href={`${kratosUrl}/self-service/registration/browser`}
            className="text-blue-600 hover:underline"
          >
            Registracija
          </a>
        </p>
      </div>
    </div>
  );
}
