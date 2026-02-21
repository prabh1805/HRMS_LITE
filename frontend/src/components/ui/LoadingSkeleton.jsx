export default function LoadingSkeleton({ rows = 5 }) {
  return (
    <div className="space-y-4 animate-pulse">
      {[...Array(rows)].map((_, i) => (
        <div key={i} className="bg-gray-200 h-12 rounded-lg"></div>
      ))}
    </div>
  )
}
