import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";

import { Nav } from "@/components/Nav";
import "./globals.css";

const inter = Inter({ subsets: ["latin", "cyrillic"] });

export const metadata: Metadata = {
  title: { default: "Право в кармане — ИИ-юрист", template: "%s · Право в кармане" },
  description: "ИИ-помощник по законодательству Республики Казахстан для молодёжи",
};

export const viewport: Viewport = { themeColor: "#0f172a" };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ru">
      <body className={`${inter.className} min-h-screen bg-slate-50 text-slate-900 antialiased`}>
        <Nav />
        <main className="mx-auto max-w-3xl px-4 py-6">{children}</main>
      </body>
    </html>
  );
}
