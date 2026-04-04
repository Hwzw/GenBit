import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getConstruct, createConstruct, updateConstruct } from "@/lib/api/constructs";
import type { ConstructCreate } from "@/types";

export function useConstruct(id: string | null) {
  return useQuery({
    queryKey: ["construct", id],
    queryFn: () => getConstruct(id!),
    enabled: !!id,
  });
}

export function useCreateConstruct() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: ConstructCreate) => createConstruct(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["constructs"] });
    },
  });
}

export function useUpdateConstruct(id: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<ConstructCreate>) => updateConstruct(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["construct", id] });
    },
  });
}
