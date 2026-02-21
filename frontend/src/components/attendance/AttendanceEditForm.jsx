import { useState, useEffect } from 'react'
import Button from '../ui/Button'
import Spinner from '../ui/Spinner'
import { ATTENDANCE_STATUS } from '../../utils/constants'

export default function AttendanceEditForm({ attendance, onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    status: ATTENDANCE_STATUS.PRESENT,
    date: new Date().toISOString().split('T')[0],
  })
  const [isSubmitting, setIsSubmitting] = useState(false)

  useEffect(() => {
    if (attendance) {
      setFormData({
        status: attendance.status || ATTENDANCE_STATUS.PRESENT,
        date: attendance.date || new Date().toISOString().split('T')[0],
      })
    }
  }, [attendance])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)
    try {
      await onSubmit(formData)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
        <p className="text-sm text-blue-700">
          <strong>Employee:</strong> {attendance?.employee_code} - {attendance?.employee_name}
        </p>
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

      <div className="flex gap-3 pt-4">
        <Button type="submit" className="flex-1" disabled={isSubmitting}>
          {isSubmitting ? (
            <span className="flex items-center justify-center gap-2">
              <Spinner size="sm" />
              Updating...
            </span>
          ) : (
            'Update Attendance'
          )}
        </Button>
        <Button type="button" variant="secondary" onClick={onCancel} className="flex-1" disabled={isSubmitting}>
          Cancel
        </Button>
      </div>
    </form>
  )
}
