export type Citation = {
  article_id: number;
  act_title: string;
  article_number: string;
  quote: string;
};

export type LegalAnswer = {
  summary: string;
  citations: Citation[];
  steps: string[];
  risks: string[];
  needs_lawyer: boolean;
};

export type ChatResponse = {
  status: "answered" | "not_found" | "unavailable";
  answer: LegalAnswer | null;
  message: string | null;
  disclaimer: string;
};

export async function askLawyer(question: string): Promise<ChatResponse> {
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) throw new Error(`Ошибка сервера: ${res.status}`);
  return res.json();
}
