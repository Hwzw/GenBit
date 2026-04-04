import { Badge } from "@/components/common";

interface Props {
  accession: string;
  name: string;
  organism: string;
  source: string;
  onSelect?: () => void;
}

export function LookupResultCard({ accession, name, organism, source, onSelect }: Props) {
  return (
    <div
      onClick={onSelect}
      className="p-3 border border-gray-200 rounded-lg hover:border-genbit-400 cursor-pointer transition"
    >
      <div className="flex justify-between items-start">
        <div>
          <p className="font-medium text-sm">{name}</p>
          <p className="text-xs text-gray-500">{accession}</p>
        </div>
        <Badge label={source} />
      </div>
      <p className="text-xs text-gray-400 mt-1 italic">{organism}</p>
    </div>
  );
}
