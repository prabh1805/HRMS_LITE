import { useState } from 'react'
import Button from '../ui/Button'
import Spinner from '../ui/Spinner'
import { ATTENDANCE_STATUS } from '../../utils/constants'

export default function AttendanceForm({ employees, onSubmit }) {
  const [formData, setFormData] = useState({
    employee_id: '',
    status: ATTENDANCE_STATUS.PRESENT,
    date: new Date().toISOString().split('T')[0],
  })
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)
    try {
      await onSubmit(formData)
      // Reset form after successful submission
      setFormData({
        employee_id: '',
        status: ATTENDANCE_STATUS.PRESENT,
        date: new Date().toISOString().split('T')[0],
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Employee
        </label>
        <select
          value={formData.employee_id}
          onChange={(e) => setFormData({ ...formData, employee_id: e.target.value })}
          disabled={isSubmitting}
          required
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
        >
          <option value="">Select Employee</option>
          {employees.map((emp) => (
            <option key={emp.id} value={emp.employee_id}>
              {emp.employee_id} - {emp.full_name}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Date
        </label>
        <input
          type="date"
          value={formData.date}
          onChange={(e) => setFormData({ ...formData, date: e.target.value })}
          disabled={isSubmitting}
          required
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Status
        </label>
        <div className="flex gap-4">
          <label className="flex items-center cursor-pointer">
            <input
              type="radio"
              value={ATTENDANCE_STATUS.PRESENT}
              checked={formData.status === ATTENDANCE_STATUS.PRESENT}
              onChange={(e) => setFormData({ ...formData, status: e.target.value })}
              disabled={isSubmitting}
              className="mr-2"
            />
            <span className="text-green-700">✓ Present</span>
          </label>
          <label className="flex items-center cursor-pointer">
            <input
              type="radio"
              value={ATTENDANCE_STATUS.ABSENT}
              checked={formData.status === ATTENDANCE_STATUS.ABSENT}
              onChange={(e) => setFormData({ ...formData, status: e.target.value })}
              disabled={isSubmitting}
              className="mr-2"
            />
            <span className="text-red-700">✗ Absent</span>
          </label>
        </div>
      </div>

      <Button type="submit" className="w-full" disabled={isSubmitting}>
        {isSubmitting ? (
          <span className="flex items-center justify-center gap-2">
            <Spinner size="sm" />
            Marking...
          </span>
        ) : (
          'Mark Attendance'
        )}
      </Button>
    </form>
  )
}
