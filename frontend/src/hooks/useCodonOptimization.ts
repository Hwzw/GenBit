import { useMutation } from "@tanstack/react-query";
import { optimizeCodons } from "@/lib/api/optimization";
import type { OptimizationRequest } from "@/types";

export function useCodonOptimization() {
  return useMutation({
    mutationFn: (request: OptimizationRequest) => optimizeCodons(request),
  });
}
