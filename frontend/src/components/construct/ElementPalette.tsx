"use client";

import { useDesignerStore } from "@/store/designerStore";
import { ElementType } from "@/types";

const PALETTE_ITEMS = [
  { type: ElementType.PROMOTER, label: "Promoter", color: "bg-blue-100 hover:bg-blue-200" },
  { type: ElementType.KOZAK, label: "Kozak", color: "bg-purple-100 hover:bg-purple-200" },
  { type: ElementType.CDS, label: "CDS", color: "bg-green-100 hover:bg-green-200" },
  { type: ElementType.TERMINATOR, label: "Terminator", color: "bg-red-100 hover:bg-red-200" },
  { type: ElementType.TAG, label: "Tag", color: "bg-yellow-100 hover:bg-yellow-200" },
  { type: ElementType.UTR, label: "UTR", color: "bg-orange-100 hover:bg-orange-200" },
];

export function ElementPalette() {
  const addElement = useDesignerStore((state) => state.addElement);

  return (
    <div className="w-32 space-y-2">
      <p className="text-xs font-semibold text-gray-500 uppercase">Elements</p>
      {PALETTE_ITEMS.map((item) => (
        <button
          key={item.type}
          onClick={() =>
            addElement({
              element_type: item.type,
              label: item.label,
              sequence: "",
              position: 0,
            })
          }
          className={`w-full text-left px-3 py-2 text-sm rounded transition ${item.color}`}
        >
          {item.label}
        </button>
      ))}
    </div>
  );
}
