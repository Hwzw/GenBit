import { Card } from "@/components/common";
import type { OrganismDetail } from "@/types";

interface Props {
  organism: OrganismDetail;
}

export function OrganismInfo({ organism }: Props) {
  return (
    <Card title="Organism Details">
      <div className="space-y-2 text-sm">
        <div>
          <span className="text-gray-500">Scientific Name: </span>
          <span className="font-medium italic">{organism.scientific_name}</span>
        </div>
        {organism.common_name && (
          <div>
            <span className="text-gray-500">Common Name: </span>
            <span>{organism.common_name}</span>
          </div>
        )}
        <div>
          <span className="text-gray-500">Taxonomy ID: </span>
          <span>{organism.tax_id}</span>
        </div>
        {organism.gc_content != null && (
          <div>
            <span className="text-gray-500">GC Content: </span>
            <span>{(organism.gc_content * 100).toFixed(1)}%</span>
          </div>
        )}
      </div>
    </Card>
  );
}
