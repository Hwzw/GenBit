"use client";

import { useParams } from "next/navigation";

export default function ProjectDetailPage() {
  const params = useParams();
  const projectId = params.id;

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Project Detail</h1>
        <p className="text-gray-500">Project ID: {projectId}</p>
        {/* TODO: Load project and display constructs */}
      </div>
    </div>
  );
}
