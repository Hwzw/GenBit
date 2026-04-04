"use client";

import { useState } from "react";
import { Card, Input } from "@/components/common";
import { LookupResultCard } from "./LookupResultCard";

export function GeneLookup() {
  const [query, setQuery] = useState("");

  return (
    <Card title="Gene Lookup">
      <div className="space-y-3">
        <Input
          placeholder="Search by gene symbol, name, or ID..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        {/* TODO: integrate useGeneSearch hook and display results */}
        {!query && (
          <p className="text-xs text-gray-400">Search NCBI Gene for coding sequences.</p>
        )}
      </div>
    </Card>
  );
}
