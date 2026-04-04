"use client";

import Link from "next/link";

export default function ProjectsPage() {
  return (
    <div className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Projects</h1>
          <Link
            href="/designer"
            className="px-4 py-2 bg-genbit-600 text-white rounded-lg hover:bg-genbit-700 transition"
          >
            New Project
          </Link>
        </div>

        {/* Project list placeholder */}
        <div className="bg-white rounded-lg shadow p-8 text-center text-gray-500">
          No projects yet. Start designing to create your first construct.
        </div>
      </div>
    </div>
  );
}
