"use client";

import { ConstructBuilder } from "@/components/construct";
import { GeneLookup, ProteinLookup } from "@/components/lookup";
import { CodonOptimizer } from "@/components/optimization";
import { OrganismSelector } from "@/components/organism";
import { SequenceViewer } from "@/components/sequence";

export default function DesignerPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Construct Designer</h1>

      <div className="grid grid-cols-3 gap-6">
        {/* Left panel: lookups and organism selection */}
        <div className="space-y-4">
          <OrganismSelector />
          <GeneLookup />
          <ProteinLookup />
        </div>

        {/* Center panel: construct builder */}
        <div className="col-span-2 space-y-4">
          <ConstructBuilder />
          <SequenceViewer />
          <CodonOptimizer />
        </div>
      </div>
    </div>
  );
}
