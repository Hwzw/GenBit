"use client";

import { Card } from "@/components/common";
import type { ConstructElement } from "@/types";

const TYPE_COLORS: Record<string, string> = {
  promoter: "bg-blue-400",
  kozak: "bg-purple-400",
  cds: "bg-green-400",
  terminator: "bg-red-400",
  tag: "bg-yellow-400",
  utr: "bg-orange-400",
  custom: "bg-gray-400",
};

interface Props {
  elements: ConstructElement[];
}

export function ConstructPreview({ elements }: Props) {
  const totalLength = elements.reduce((sum, e) => sum + e.sequence.length, 0);

  return (
    <Card title="Linear Map">
      {elements.length === 0 ? (
        <p className="text-gray-400 text-sm">No elements added yet.</p>
      ) : (
        <div>
          <div className="flex h-8 rounded overflow-hidden">
            {elements.map((el, i) => {
              const width = totalLength > 0 ? (el.sequence.length / totalLength) * 100 : 0;
              return (
                <div
                  key={i}
                  className={`${TYPE_COLORS[el.element_type] || TYPE_COLORS.custom} flex items-center justify-center text-xs text-white font-medium`}
                  style={{ width: `${width}%` }}
                  title={`${el.label} (${el.sequence.length} bp)`}
                >
                  {width > 10 ? el.label : ""}
                </div>
              );
            })}
          </div>
          <p className="text-xs text-gray-500 mt-2">Total: {totalLength} bp</p>
        </div>
      )}
    </Card>
  );
}
