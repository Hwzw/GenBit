import Link from "next/link";

export function Header() {
  return (
    <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between">
      <Link href="/" className="text-xl font-bold text-genbit-700">
        GenBit
      </Link>
      <nav className="flex gap-6">
        <Link href="/designer" className="text-gray-600 hover:text-genbit-600 transition">
          Designer
        </Link>
        <Link href="/projects" className="text-gray-600 hover:text-genbit-600 transition">
          Projects
        </Link>
      </nav>
    </header>
  );
}
