const COMPLEMENT: Record<string, string> = {
  A: "T", T: "A", G: "C", C: "G",
  a: "t", t: "a", g: "c", c: "g",
};

export function reverseComplement(sequence: string): string {
  return sequence
    .split("")
    .reverse()
    .map((c) => COMPLEMENT[c] || c)
    .join("");
}

export function calculateGCContent(sequence: string): number {
  if (!sequence) return 0;
  const upper = sequence.toUpperCase();
  const gc = (upper.match(/[GC]/g) || []).length;
  return gc / upper.length;
}

export function detectSequenceType(sequence: string): "dna" | "protein" | "unknown" {
  const clean = sequence.toUpperCase().replace(/\s/g, "");
  if (!clean) return "unknown";
  if (/^[ATCGN]+$/.test(clean)) return "dna";
  return "protein";
}

export function formatFasta(header: string, sequence: string, lineWidth = 80): string {
  const lines = [`>${header}`];
  for (let i = 0; i < sequence.length; i += lineWidth) {
    lines.push(sequence.slice(i, i + lineWidth));
  }
  return lines.join("\n");
}
