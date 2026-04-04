"use client";

import { Card, Input, Button } from "@/components/common";

export function PromoterSelector() {
  return (
    <Card title="Promoter Selection">
      <div className="space-y-3">
        <Input label="Search Promoters" placeholder="e.g. CMV, EF1a, GAL1..." />
        <div className="text-sm text-gray-500">
          Search EPD or select from common synthetic promoters.
        </div>
        <Button variant="secondary">Browse Catalog</Button>
      </div>
    </Card>
  );
}
