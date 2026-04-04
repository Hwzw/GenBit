"use client";

import { useState } from "react";
import { Card, Input } from "@/components/common";

export function ProteinLookup() {
  const [query, setQuery] = useState("");

  return (
    <Card title="Protein Lookup">
      <div className="space-y-3">
        <Input
          placeholder="Search by protein name or accession..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        {/* TODO: integrate useProteinSearch hook and display results */}
        {!query && (
          <p className="text-xs text-gray-400">Search UniProt and NCBI Protein.</p>
        )}
      </div>
    </Card>
  );
}
