import { useQuery } from "@tanstack/react-query";
import { searchProteins } from "@/lib/api/proteins";

export function useProteinSearch(query: string, organism?: string) {
  return useQuery({
    queryKey: ["proteins", "search", query, organism],
    queryFn: () => searchProteins(query, organism),
    enabled: query.length >= 2,
    staleTime: 5 * 60 * 1000,
  });
}
