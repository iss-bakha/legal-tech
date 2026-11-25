export const metadata = { title: "Документы" };

export default function DocumentsPage() {
  return (
    <div className="space-y-3">
      <h1 className="text-2xl font-semibold">Составить документ</h1>
      <p className="text-sm text-slate-600">
        Претензии, жалобы и заявления в правильном формате. Форму задаёт шаблон юриста, ИИ пишет
        только текст по существу.
      </p>
      {/* TODO (хакатон): список шаблонов из /api/documents/templates, анкета, скачивание DOCX */}
      <div className="rounded-xl border border-slate-200 bg-white p-4 text-sm">
        Досудебная претензия о возврате депозита <span className="text-slate-400">(скоро)</span>
      </div>
    </div>
  );
}
