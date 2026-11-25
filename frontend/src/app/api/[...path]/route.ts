// Прокси: браузер шлёт /api/* на фронтенд, а сервер Next.js пересылает запрос в FastAPI.
// Так не нужен CORS, а адрес бэкенда (BACKEND_URL) читается при запуске, а не при сборке.
import type { NextRequest } from "next/server";

export const dynamic = "force-dynamic";

async function proxy(req: NextRequest, { params }: { params: Promise<{ path: string[] }> }) {
  const backendUrl = process.env.BACKEND_URL ?? "http://localhost:8000";
  const { path } = await params;
  const target = `${backendUrl}/api/${path.join("/")}${req.nextUrl.search}`;

  const headers = new Headers(req.headers);
  headers.delete("host");

  const hasBody = !["GET", "HEAD"].includes(req.method);
  try {
    const res = await fetch(target, {
      method: req.method,
      headers,
      body: hasBody ? await req.arrayBuffer() : undefined,
      cache: "no-store",
    });
    const resHeaders = new Headers(res.headers);
    // fetch уже распаковал тело, поэтому эти заголовки больше не верны
    resHeaders.delete("content-encoding");
    resHeaders.delete("content-length");
    return new Response(res.body, { status: res.status, headers: resHeaders });
  } catch {
    return Response.json({ detail: "Бэкенд недоступен" }, { status: 502 });
  }
}

export { proxy as GET, proxy as POST, proxy as PUT, proxy as PATCH, proxy as DELETE };
