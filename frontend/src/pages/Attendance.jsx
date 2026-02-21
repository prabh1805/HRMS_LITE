import { useState, useEffect } from 'react'
import Card from '../components/ui/Card'
import Modal from '../components/ui/Modal'
import Button from '../components/ui/Button'
import Toast from '../components/ui/Toast'
import Spinner from '../components/ui/Spinner'
import PageLoader from '../components/ui/PageLoader'
import EmptyState from '../components/ui/EmptyState'
import ErrorState from '../components/ui/ErrorState'
import AttendanceForm from '../components/attendance/AttendanceForm'
import AttendanceEditForm from '../components/attendance/AttendanceEditForm'
import AttendanceTable from '../components/attendance/AttendanceTable'
import { getEmployees, getAttendance, markAttendance, updateAttendance, deleteAttendance } from '../services/api'
import { useToast } from '../hooks/useToast'

export default function Attendance() {
  const [employees, setEmployees] = useState([])
  const [attendance, setAttendance] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showEditModal, setShowEditModal] = useState(false)
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [selectedAttendance, setSelectedAttendance] = useState(null)
  const [isDeleting, setIsDeleting] = useState(false)
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const { toast, showSuccess, showError, hideToast } = useToast()

  const fetchData = async () => {
    setLoading(true)
    setError(null)
    try {
      const [employeesRes, attendanceRes] = await Promise.all([
        getEmployees(),
        getAttendance(startDate || null, endDate || null)
      ])
      setEmployees(employeesRes.data)
      setAttendance(attendanceRes.data)
    } catch (err) {
      setError(err.message || 'Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [startDate, endDate])

  const handleMarkAttendance = async (formData) => {
    try {
      await markAttendance(formData)
      showSuccess('Attendance marked successfully!')
      fetchData()
    } catch (err) {
      showError(err.response?.data?.message || 'Failed to mark attendance')
      throw err // Re-throw to keep form in loading state
    }
  }

  const handleEditClick = (record) => {
    setSelectedAttendance(record)
    setShowEditModal(true)
  }

  const handleEditAttendance = async (formData) => {
    try {
      await updateAttendance(selectedAttendance.id, formData)
      showSuccess('Attendance updated successfully!')
      setShowEditModal(false)
      setSelectedAttendance(null)
      fetchData()
    } catch (err) {
      showError(err.response?.data?.message || 'Failed to update attendance')
      throw err // Re-throw to keep form in loading state
    }
  }

  const handleDeleteClick = (record) => {
    setSelectedAttendance(record)
    setShowDeleteModal(true)
  }

  const handleDeleteConfirm = async () => {
    setIsDeleting(true)
    try {
      await deleteAttendance(selectedAttendance.id)
      showSuccess('Attendance record deleted successfully!')
      fetchData()
    } catch (err) {
      showError(err.response?.data?.message || 'Failed to delete attendance')
    } finally {
      setIsDeleting(false)
      setShowDeleteModal(false)
      setSelectedAttendance(null)
    }
  }

  if (loading) return <PageLoader message="Loading attendance data..." />
  if (error) return <ErrorState message={error} onRetry={fetchData} />

  const handleClearFilters = () => {
    setStartDate('')
    setEndDate('')
  }

  return (
    <div className="space-y-6">
      {toast && <Toast message={toast.message} type={toast.type} onClose={hideToast} />}
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-1">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center text-white text-xl">
              ✓
            </div>
            <h3 className="text-lg font-bold text-gray-800">Mark Attendance</h3>
          </div>
          {employees.length === 0 ? (
            <EmptyState
              icon="👥"
              message="No employees found. Add employees first."
            />
          ) : (
            <AttendanceForm employees={employees} onSubmit={handleMarkAttendance} />
          )}
        </Card>

        <Card className="lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white text-xl">
                📋
              </div>
              <h3 className="text-lg font-bold text-gray-800">Attendance History</h3>
            </div>
          </div>

          {/* Date Filters */}
          <div className="mb-4 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg">
            <div className="flex flex-wrap items-end gap-3">
              <div className="flex-1 min-w-[150px]">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Start Date
                </label>
                <input
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                />
              </div>
              <div className="flex-1 min-w-[150px]">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  End Date
                </label>
                <input
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                />
              </div>
              {(startDate || endDate) && (
                <Button variant="secondary" onClick={handleClearFilters}>
                  Clear Filters
                </Button>
              )}
            </div>
          </div>

          {attendance.length === 0 ? (
            <EmptyState
              icon="📅"
              message={startDate || endDate ? "No attendance records found for the selected date range." : "No attendance records found. Start marking attendance to see records here."}
            />
          ) : (
            <AttendanceTable 
              attendance={attendance} 
              onEdit={handleEditClick}
              onDelete={handleDeleteClick}
            />
          )}
        </Card>
      </div>

      <Modal
        isOpen={showEditModal}
        onClose={() => {
          setShowEditModal(false)
          setSelectedAttendance(null)
        }}
        title="Edit Attendance Record"
      >
        <AttendanceEditForm
          attendance={selectedAttendance}
          onSubmit={handleEditAttendance}
          onCancel={() => {
            setShowEditModal(false)
            setSelectedAttendance(null)
          }}
        />
      </Modal>

      <Modal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        title="Confirm Delete"
      >
        <div className="space-y-4">
          <p className="text-gray-600">
            Are you sure you want to delete the attendance record for{' '}
            <strong>{selectedAttendance?.employee_name}</strong> on{' '}
            <strong>{selectedAttendance?.date}</strong>?
            This action cannot be undone.
          </p>
          <div className="flex gap-3">
            <Button variant="danger" onClick={handleDeleteConfirm} className="flex-1" disabled={isDeleting}>
              {isDeleting ? (
                <span className="flex items-center justify-center gap-2">
                  <Spinner size="sm" />
                  Deleting...
                </span>
              ) : (
                'Delete'
              )}
            </Button>
            <Button variant="secondary" onClick={() => setShowDeleteModal(false)} className="flex-1" disabled={isDeleting}>
              Cancel
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}
