"use client";

import { Card } from "@/components/common";

interface SequenceViewerProps {
  sequence?: string;
  annotations?: { type: string; label: string; start: number; end: number }[];
}

const NUCLEOTIDE_COLORS: Record<string, string> = {
  A: "text-dna-adenine",
  T: "text-dna-thymine",
  G: "text-dna-guanine",
  C: "text-dna-cytosine",
};

export function SequenceViewer({ sequence, annotations = [] }: SequenceViewerProps) {
  if (!sequence) {
    return (
      <Card title="Sequence Viewer">
        <p className="text-gray-400 text-sm">No sequence to display. Build a construct to see the assembled sequence.</p>
      </Card>
    );
  }

  return (
    <Card title="Sequence Viewer">
      <div className="font-mono text-sm leading-6 break-all bg-gray-50 p-3 rounded max-h-64 overflow-y-auto">
        {sequence.split("").map((char, i) => (
          <span key={i} className={NUCLEOTIDE_COLORS[char.toUpperCase()] || "text-gray-700"}>
            {char}
          </span>
        ))}
      </div>
      {annotations.length > 0 && (
        <div className="mt-3 flex gap-2 flex-wrap">
          {annotations.map((ann, i) => (
            <span key={i} className="text-xs bg-genbit-100 text-genbit-700 px-2 py-1 rounded">
              {ann.label} ({ann.start}-{ann.end})
            </span>
          ))}
        </div>
      )}
    </Card>
  );
}
