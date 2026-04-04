"use client";

import { Card, Button } from "@/components/common";

export function KozakConfigurator() {
  return (
    <Card title="Kozak Sequence">
      <div className="space-y-3">
        <div className="text-sm">
          <p className="text-gray-500">
            The Kozak consensus sequence varies by organism. Select your target organism
            first, then generate the appropriate initiation context.
          </p>
        </div>
        <div className="p-3 bg-gray-50 rounded font-mono text-sm">
          <span className="text-gray-400">Consensus: </span>
          <span className="text-genbit-700 font-bold">GCCACCATGG</span>
          <span className="text-gray-400 text-xs ml-2">(vertebrate default)</span>
        </div>
        <Button variant="secondary">Generate Kozak</Button>
      </div>
    </Card>
  );
}
