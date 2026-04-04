"use client";

const DESIGN_STEPS = [
  { id: "organism", label: "1. Select Organism" },
  { id: "gene", label: "2. Gene/Protein Lookup" },
  { id: "construct", label: "3. Build Construct" },
  { id: "optimize", label: "4. Optimize Codons" },
  { id: "export", label: "5. Export" },
];

export function Sidebar() {
  return (
    <aside className="w-56 bg-white border-r border-gray-200 p-4">
      <h3 className="text-sm font-semibold text-gray-500 uppercase mb-4">Design Steps</h3>
      <nav className="space-y-2">
        {DESIGN_STEPS.map((step) => (
          <div
            key={step.id}
            className="px-3 py-2 text-sm text-gray-700 rounded hover:bg-genbit-50 cursor-pointer transition"
          >
            {step.label}
          </div>
        ))}
      </nav>
    </aside>
  );
}
