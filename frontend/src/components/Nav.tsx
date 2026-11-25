import Link from "next/link";

const links = [
  { href: "/", label: "ИИ-юрист" },
  { href: "/contract", label: "Сфоткай договор" },
  { href: "/documents", label: "Документы" },
];

export function Nav() {
  return (
    <header className="border-b border-slate-200 bg-white">
      <nav className="mx-auto flex max-w-3xl items-center gap-4 overflow-x-auto px-4 py-3 text-sm">
        <span className="font-semibold whitespace-nowrap text-slate-900">Право в кармане</span>
        {links.map((l) => (
          <Link key={l.href} href={l.href} className="whitespace-nowrap text-slate-600 hover:text-slate-900">
            {l.label}
          </Link>
        ))}
      </nav>
    </header>
  );
}
