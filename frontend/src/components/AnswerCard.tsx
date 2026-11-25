import type { ChatResponse } from "@/lib/api";

export function AnswerCard({ res }: { res: ChatResponse }) {
  if (!res.answer) {
    return (
      <div className="rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900">
        <p>{res.message}</p>
        <LawyerButton />
      </div>
    );
  }
  const a = res.answer;
  return (
    <div className="space-y-4 rounded-xl border border-slate-200 bg-white p-4 text-sm">
      <p className="text-base">{a.summary}</p>

      <Section title="На основании">
        {a.citations.map((c) => (
          <li key={`${c.article_id}-${c.quote}`}>
            <span className="font-medium">
              Ст. {c.article_number}, {c.act_title}
            </span>
            : «{c.quote}»
          </li>
        ))}
      </Section>

      <Section title="Что делать" ordered>
        {a.steps.map((s) => (
          <li key={s}>{s}</li>
        ))}
      </Section>

      {a.risks.length > 0 && (
        <Section title="Риски">
          {a.risks.map((r) => (
            <li key={r}>{r}</li>
          ))}
        </Section>
      )}

      <div className="flex flex-wrap gap-2 pt-2">
        <a href="/contract" className="rounded-lg border border-slate-300 px-3 py-2">
          Проверить мой договор
        </a>
        <a href="/documents" className="rounded-lg border border-slate-300 px-3 py-2">
          Составить претензию
        </a>
        <LawyerButton />
      </div>

      <p className="text-xs text-slate-500">{res.disclaimer}</p>
    </div>
  );
}

function Section({
  title,
  ordered,
  children,
}: {
  title: string;
  ordered?: boolean;
  children: React.ReactNode;
}) {
  const List = ordered ? "ol" : "ul";
  return (
    <div>
      <h3 className="mb-1 font-semibold">{title}</h3>
      <List className={`${ordered ? "list-decimal" : "list-disc"} space-y-1 pl-5`}>{children}</List>
    </div>
  );
}

function LawyerButton() {
  // TODO: форма связи с партнёрским юристом
  return (
    <button type="button" className="mt-2 rounded-lg bg-slate-900 px-3 py-2 text-white">
      Связаться с юристом
    </button>
  );
}
