"use client";

import { Card } from "@/components/common";
import { useDesignerStore } from "@/store/designerStore";
import { ConstructElement as ConstructElementComponent } from "./ConstructElement";
import { ElementPalette } from "./ElementPalette";

export function ConstructBuilder() {
  const elements = useDesignerStore((state) => state.elements);

  return (
    <Card title="Construct Builder">
      <div className="flex gap-4">
        <ElementPalette />
        <div className="flex-1 min-h-[200px] border-2 border-dashed border-gray-300 rounded-lg p-4">
          {elements.length === 0 ? (
            <p className="text-gray-400 text-sm text-center mt-8">
              Drag elements from the palette or click to add them to your construct.
            </p>
          ) : (
            <div className="flex gap-2 flex-wrap">
              {elements.map((element, index) => (
                <ConstructElementComponent key={index} element={element} index={index} />
              ))}
            </div>
          )}
        </div>
      </div>
    </Card>
  );
}
