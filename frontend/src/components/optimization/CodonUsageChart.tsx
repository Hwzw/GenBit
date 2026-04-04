"use client";

import { Card } from "@/components/common";

interface Props {
  codonTable?: Record<string, Record<string, number>>;
}

export function CodonUsageChart({ codonTable }: Props) {
  if (!codonTable) {
    return (
      <Card title="Codon Usage">
        <p className="text-gray-400 text-sm">Select an organism to view codon usage frequencies.</p>
      </Card>
    );
  }

  return (
    <Card title="Codon Usage">
      <div className="max-h-64 overflow-y-auto text-xs font-mono">
        {Object.entries(codonTable).map(([aa, codons]) => (
          <div key={aa} className="mb-2">
            <span className="font-bold text-genbit-700">{aa}: </span>
            {Object.entries(codons).map(([codon, freq]) => (
              <span key={codon} className="mr-2">
                {codon}={typeof freq === "number" ? freq.toFixed(2) : freq}
              </span>
            ))}
          </div>
        ))}
      </div>
    </Card>
  );
}
