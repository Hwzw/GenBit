import { useQuery } from "@tanstack/react-query";
import { searchOrganisms } from "@/lib/api/organisms";

export function useOrganismSearch(query: string) {
  return useQuery({
    queryKey: ["organisms", "search", query],
    queryFn: () => searchOrganisms(query),
    enabled: query.length >= 2,
    staleTime: 10 * 60 * 1000,
  });
}
