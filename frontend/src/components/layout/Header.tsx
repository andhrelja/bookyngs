"use client";

export default function Header() {
  const kratosUrl = process.env.NEXT_PUBLIC_KRATOS_URL ?? "http://localhost:4433";

  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-end px-6">
      <a
        href={`${kratosUrl}/self-service/logout/browser`}
        className="text-sm text-gray-500 hover:text-gray-900 transition-colors"
      >
        Odjava
      </a>
    </header>
  );
}
