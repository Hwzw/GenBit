"use client";

import { useState } from "react";
import { Card, Button } from "@/components/common";

interface SequenceInputProps {
  onSubmit: (sequence: string, type: "dna" | "protein") => void;
}

export function SequenceInput({ onSubmit }: SequenceInputProps) {
  const [input, setInput] = useState("");
  const [seqType, setSeqType] = useState<"dna" | "protein">("protein");

  return (
    <Card title="Paste Sequence">
      <div className="space-y-3">
        <div className="flex gap-2">
          <button
            className={`px-3 py-1 text-sm rounded ${seqType === "protein" ? "bg-genbit-600 text-white" : "bg-gray-100"}`}
            onClick={() => setSeqType("protein")}
          >
            Protein
          </button>
          <button
            className={`px-3 py-1 text-sm rounded ${seqType === "dna" ? "bg-genbit-600 text-white" : "bg-gray-100"}`}
            onClick={() => setSeqType("dna")}
          >
            DNA
          </button>
        </div>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={`Paste ${seqType === "protein" ? "amino acid" : "nucleotide"} sequence (FASTA or plain)...`}
          className="w-full h-32 font-mono text-sm p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-genbit-500"
        />
        <Button onClick={() => onSubmit(input, seqType)} disabled={!input.trim()}>
          Use Sequence
        </Button>
      </div>
    </Card>
  );
}
