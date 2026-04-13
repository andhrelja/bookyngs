import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin-ext"] });

export const metadata: Metadata = {
  title: "Bookyngs — Admin",
  description: "Upravljajte svojom web prodavaonom, rezervacijama i loyalty programom.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="hr">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
