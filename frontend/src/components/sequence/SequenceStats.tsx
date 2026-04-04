import { Card } from "@/components/common";

interface SequenceStatsProps {
  sequence: string;
  type: "dna" | "protein";
}

export function SequenceStats({ sequence, type }: SequenceStatsProps) {
  const length = sequence.length;
  const gcContent =
    type === "dna"
      ? ((sequence.match(/[GC]/gi)?.length || 0) / length) * 100
      : null;

  return (
    <Card title="Sequence Statistics">
      <div className="grid grid-cols-3 gap-4 text-sm">
        <div>
          <p className="text-gray-500">Length</p>
          <p className="font-semibold">{length} {type === "dna" ? "bp" : "aa"}</p>
        </div>
        {gcContent !== null && (
          <div>
            <p className="text-gray-500">GC Content</p>
            <p className="font-semibold">{gcContent.toFixed(1)}%</p>
          </div>
        )}
        {type === "dna" && (
          <div>
            <p className="text-gray-500">Codons</p>
            <p className="font-semibold">{Math.floor(length / 3)}</p>
          </div>
        )}
      </div>
    </Card>
  );
}
