export function LoadingSpinner({ className = "" }: { className?: string }) {
  return (
    <div className={`flex justify-center items-center ${className}`}>
      <div className="w-6 h-6 border-2 border-genbit-600 border-t-transparent rounded-full animate-spin" />
    </div>
  );
}
