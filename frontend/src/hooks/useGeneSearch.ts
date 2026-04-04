import { useQuery } from "@tanstack/react-query";
import { searchGenes } from "@/lib/api/genes";

export function useGeneSearch(query: string, organism?: string) {
  return useQuery({
    queryKey: ["genes", "search", query, organism],
    queryFn: () => searchGenes(query, organism),
    enabled: query.length >= 2,
    staleTime: 5 * 60 * 1000,
  });
}
