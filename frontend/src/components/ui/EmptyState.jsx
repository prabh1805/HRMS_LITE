export default function EmptyState({ icon = '📭', message, action }) {
  return (
    <div className="text-center py-12">
      <div className="text-6xl mb-4">{icon}</div>
      <p className="text-gray-500 mb-6">{message}</p>
      {action && action}
    </div>
  )
}
