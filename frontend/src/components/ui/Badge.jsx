import { STATUS_COLORS } from '../../utils/constants'

export default function Badge({ status }) {
  const colorClass = STATUS_COLORS[status] || 'bg-gray-100 text-gray-800'
  
  const displayText = {
    'PRESENT': '✓ Present',
    'ABSENT': '✗ Absent'
  }
  
  return (
    <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold ${colorClass}`}>
      {displayText[status] || status}
    </span>
  )
}
