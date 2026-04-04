"use client";

import { useState } from "react";
import { Card, Input } from "@/components/common";
import { useDesignerStore } from "@/store/designerStore";

export function OrganismSelector() {
  const [query, setQuery] = useState("");
  const selectedOrganism = useDesignerStore((state) => state.selectedOrganism);
  const setSelectedOrganism = useDesignerStore((state) => state.setSelectedOrganism);

  return (
    <Card title="Target Organism">
      <Input
        label="Search organisms"
        placeholder="e.g. Homo sapiens, E. coli..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      {selectedOrganism && (
        <div className="mt-3 p-2 bg-genbit-50 rounded text-sm">
          <p className="font-medium">{selectedOrganism.scientific_name}</p>
          {selectedOrganism.common_name && (
            <p className="text-gray-500">{selectedOrganism.common_name}</p>
          )}
        </div>
      )}
      {/* TODO: Search results dropdown with useOrganismSearch hook */}
    </Card>
  );
}
