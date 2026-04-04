"use client";

import type { ConstructElement as ConstructElementType } from "@/types";
import { Badge } from "@/components/common";

const TYPE_COLORS: Record<string, string> = {
  promoter: "bg-blue-100 border-blue-300",
  kozak: "bg-purple-100 border-purple-300",
  cds: "bg-green-100 border-green-300",
  terminator: "bg-red-100 border-red-300",
  tag: "bg-yellow-100 border-yellow-300",
  utr: "bg-orange-100 border-orange-300",
  custom: "bg-gray-100 border-gray-300",
};

interface Props {
  element: ConstructElementType;
  index: number;
}

export function ConstructElement({ element, index }: Props) {
  const colorClass = TYPE_COLORS[element.element_type] || TYPE_COLORS.custom;

  return (
    <div className={`border rounded-lg p-3 cursor-move ${colorClass}`}>
      <div className="flex items-center gap-2">
        <span className="text-xs text-gray-500">{index + 1}</span>
        <Badge label={element.element_type} />
      </div>
      <p className="text-sm font-medium mt-1">{element.label}</p>
      <p className="text-xs text-gray-500">{element.sequence.length} bp</p>
    </div>
  );
}
