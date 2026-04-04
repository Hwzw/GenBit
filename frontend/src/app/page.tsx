import Link from "next/link";

export default function HomePage() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-8">
      <h1 className="text-5xl font-bold text-genbit-700 mb-4">GenBit</h1>
      <p className="text-xl text-gray-600 mb-8 text-center max-w-2xl">
        Design genetic sequences for heterologous protein expression. Codon optimization,
        Kozak sequences, promoter selection, and construct assembly — all in one workspace.
      </p>
      <div className="flex gap-4">
        <Link
          href="/designer"
          className="px-6 py-3 bg-genbit-600 text-white rounded-lg hover:bg-genbit-700 transition"
        >
          Start Designing
        </Link>
        <Link
          href="/projects"
          className="px-6 py-3 border border-genbit-600 text-genbit-600 rounded-lg hover:bg-genbit-50 transition"
        >
          My Projects
        </Link>
      </div>
    </main>
  );
}
