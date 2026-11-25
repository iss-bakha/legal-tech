import type { MetadataRoute } from "next";

// Манифест PWA: сайт можно «установить» на главный экран телефона.
export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Право в кармане — ИИ-юрист",
    short_name: "Право в кармане",
    description: "ИИ-помощник по законодательству РК",
    start_url: "/",
    display: "standalone",
    background_color: "#f8fafc",
    theme_color: "#0f172a",
    icons: [{ src: "/favicon.ico", sizes: "any", type: "image/x-icon" }],
  };
}
