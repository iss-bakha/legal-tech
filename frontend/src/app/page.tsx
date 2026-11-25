"use client";

import { useState } from "react";

import { AnswerCard } from "@/components/AnswerCard";
import { askLawyer, type ChatResponse } from "@/lib/api";

type Turn = { question: string; response?: ChatResponse; error?: string };

const EXAMPLES = [
  "Я работаю без договора, и мне не выплатили зарплату. Что делать?",
  "Хозяин квартиры не возвращает депозит после выезда",
];

export default function ChatPage() {
  const [turns, setTurns] = useState<Turn[]>([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  async function send(q: string) {
    const text = q.trim();
    if (text.length < 3 || loading) return;
    setQuestion("");
    setLoading(true);
    setTurns((t) => [...t, { question: text }]);
    try {
      const response = await askLawyer(text);
      setTurns((t) => t.map((turn, i) => (i === t.length - 1 ? { ...turn, response } : turn)));
    } catch (e) {
      const error = e instanceof Error ? e.message : "Неизвестная ошибка";
      setTurns((t) => t.map((turn, i) => (i === t.length - 1 ? { ...turn, error } : turn)));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col gap-4">
      <div>
        <h1 className="text-2xl font-semibold">ИИ-юрист</h1>
        <p className="text-sm text-slate-600">
          Отвечаю простым языком строго по законам Республики Казахстан, со ссылками на статьи.
        </p>
      </div>

      {turns.length === 0 && (
        <div className="flex flex-col gap-2">
          {EXAMPLES.map((ex) => (
            <button
              key={ex}
              type="button"
              onClick={() => send(ex)}
              className="rounded-xl border border-slate-200 bg-white p-3 text-left text-sm hover:border-slate-400"
            >
              {ex}
            </button>
          ))}
        </div>
      )}

      {turns.map((turn, i) => (
        <div key={i} className="flex flex-col gap-2">
          <div className="self-end rounded-xl bg-slate-900 px-4 py-2 text-sm text-white">
            {turn.question}
          </div>
          {turn.response && <AnswerCard res={turn.response} />}
          {turn.error && <p className="text-sm text-red-600">{turn.error}</p>}
          {!turn.response && !turn.error && <p className="text-sm text-slate-500">Ищу в законах…</p>}
        </div>
      ))}

      <form
        onSubmit={(e) => {
          e.preventDefault();
          send(question);
        }}
        className="sticky bottom-0 flex gap-2 bg-slate-50 py-3"
      >
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Опишите ситуацию своими словами"
          rows={2}
          className="flex-1 resize-none rounded-xl border border-slate-300 bg-white p-3 text-sm"
        />
        <button
          type="submit"
          disabled={loading}
          className="rounded-xl bg-slate-900 px-4 text-sm text-white disabled:opacity-50"
        >
          Спросить
        </button>
      </form>
    </div>
  );
}
