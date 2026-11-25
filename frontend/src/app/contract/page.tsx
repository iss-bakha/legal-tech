export const metadata = { title: "Сфоткай договор" };

export default function ContractPage() {
  return (
    <div className="space-y-3">
      <h1 className="text-2xl font-semibold">Сфоткай договор</h1>
      <p className="text-sm text-slate-600">
        Загрузите фото страниц договора, и мы подсветим рискованные пункты со ссылками на статьи
        закона.
      </p>
      {/* TODO (хакатон): загрузка 1–10 фото с камеры, отчёт с подсветкой пунктов */}
      <label className="block rounded-xl border-2 border-dashed border-slate-300 bg-white p-8 text-center text-sm text-slate-500">
        <input type="file" accept="image/*,application/pdf" capture="environment" multiple disabled className="hidden" />
        Скоро здесь можно будет сфотографировать договор
      </label>
    </div>
  );
}
