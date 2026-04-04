import { Card, Badge } from "@/components/common";
import type { OptimizationResult } from "@/types";

interface Props {
  result: OptimizationResult;
}

export function OptimizationResults({ result }: Props) {
  return (
    <Card title="Optimization Results">
      <div className="space-y-3">
        <div className="flex items-center gap-2">
          <Badge label={result.status} variant={result.status === "completed" ? "success" : "warning"} />
        </div>
        {result.cai_before != null && result.cai_after != null && (
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p className="text-gray-500">CAI Before</p>
              <p className="font-semibold">{result.cai_before.toFixed(3)}</p>
            </div>
            <div>
              <p className="text-gray-500">CAI After</p>
              <p className="font-semibold text-genbit-600">{result.cai_after.toFixed(3)}</p>
            </div>
          </div>
        )}
        {result.gc_content != null && (
          <div className="text-sm">
            <p className="text-gray-500">GC Content</p>
            <p className="font-semibold">{(result.gc_content * 100).toFixed(1)}%</p>
          </div>
        )}
      </div>
    </Card>
  );
}
