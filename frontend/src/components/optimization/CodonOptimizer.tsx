"use client";

import { Card, Button, Select } from "@/components/common";
import { OptimizationStrategy } from "@/types";

export function CodonOptimizer() {
  return (
    <Card title="Codon Optimization">
      <div className="space-y-4">
        <Select
          label="Optimization Strategy"
          options={[
            { value: OptimizationStrategy.FREQUENCY, label: "Most Frequent Codons" },
            { value: OptimizationStrategy.HARMONIZED, label: "Harmonized (match rare codon positions)" },
            { value: OptimizationStrategy.BALANCED, label: "Balanced (frequency + constraints)" },
          ]}
        />
        <div className="flex gap-4">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-1">GC Min (%)</label>
            <input
              type="number"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
              placeholder="30"
              min={0}
              max={100}
            />
          </div>
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-1">GC Max (%)</label>
            <input
              type="number"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
              placeholder="70"
              min={0}
              max={100}
            />
          </div>
        </div>
        <Button>Optimize Codons</Button>
      </div>
    </Card>
  );
}
