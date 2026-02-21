import { useState, useEffect } from 'react'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import Modal from '../components/ui/Modal'
import Toast from '../components/ui/Toast'
import Spinner from '../components/ui/Spinner'
import PageLoader from '../components/ui/PageLoader'
import EmptyState from '../components/ui/EmptyState'
import ErrorState from '../components/ui/ErrorState'
import EmployeeForm from '../components/employee/EmployeeForm'
import EmployeeTable from '../components/employee/EmployeeTable'
import { getEmployees, createEmployee, updateEmployee, deleteEmployee } from '../services/api'
import { useToast } from '../hooks/useToast'

export default function Employees() {
  const [employees, setEmployees] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showAddModal, setShowAddModal] = useState(false)
  const [showEditModal, setShowEditModal] = useState(false)
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [selectedEmployee, setSelectedEmployee] = useState(null)
  const [isDeleting, setIsDeleting] = useState(false)
  const { toast, showSuccess, showError, hideToast } = useToast()

  const fetchEmployees = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await getEmployees()
      setEmployees(response.data)
    } catch (err) {
      setError(err.message || 'Failed to load employees')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchEmployees()
  }, [])

  const handleAddEmployee = async (formData) => {
    try {
      await createEmployee(formData)
      showSuccess('Employee added successfully!')
      setShowAddModal(false)
      fetchEmployees()
    } catch (err) {
      showError(err.response?.data?.message || 'Failed to add employee')
      throw err // Re-throw to keep form in loading state
    }
  }

  const handleEditClick = (employee) => {
    setSelectedEmployee(employee)
    setShowEditModal(true)
  }

  const handleEditEmployee = async (formData) => {
    try {
      await updateEmployee(selectedEmployee.id, formData)
      showSuccess('Employee updated successfully!')
      setShowEditModal(false)
      setSelectedEmployee(null)
      fetchEmployees()
    } catch (err) {
      showError(err.response?.data?.message || 'Failed to update employee')
      throw err // Re-throw to keep form in loading state
    }
  }

  const handleDeleteClick = (employee) => {
    setSelectedEmployee(employee)
    setShowDeleteModal(true)
  }

  const handleDeleteConfirm = async () => {
    setIsDeleting(true)
    try {
      await deleteEmployee(selectedEmployee.id)
      showSuccess('Employee deleted successfully!')
      fetchEmployees()
    } catch (err) {
      showError(err.response?.data?.message || 'Failed to delete employee')
    } finally {
      setIsDeleting(false)
      setShowDeleteModal(false)
      setSelectedEmployee(null)
    }
  }

  return (
    <div className="space-y-6">
      {toast && <Toast message={toast.message} type={toast.type} onClose={hideToast} />}
      
      {loading ? (
        <PageLoader message="Loading employees..." />
      ) : (
        <>
          <div className="flex justify-between items-center">
            <h3 className="text-xl font-bold text-gray-800">Employee Management</h3>
            <Button onClick={() => setShowAddModal(true)}>
              <span className="flex items-center gap-2">
                <span>➕</span>
                Add Employee
              </span>
            </Button>
          </div>

          <Card>
            {error ? (
              <ErrorState message={error} onRetry={fetchEmployees} />
            ) : employees.length === 0 ? (
              <EmptyState
                icon="👥"
                message="No employees found. Add your first employee to get started."
                action={<Button onClick={() => setShowAddModal(true)}>Add Employee</Button>}
              />
            ) : (
              <EmployeeTable 
                employees={employees} 
                onEdit={handleEditClick}
                onDelete={handleDeleteClick} 
              />
            )}
          </Card>
        </>
      )}

      <Modal
        isOpen={showAddModal}
        onClose={() => setShowAddModal(false)}
        title="Add New Employee"
      >
        <EmployeeForm
          onSubmit={handleAddEmployee}
          onCancel={() => setShowAddModal(false)}
        />
      </Modal>

      <Modal
        isOpen={showEditModal}
        onClose={() => {
          setShowEditModal(false)
          setSelectedEmployee(null)
        }}
        title="Edit Employee"
      >
        <EmployeeForm
          employee={selectedEmployee}
          onSubmit={handleEditEmployee}
          onCancel={() => {
            setShowEditModal(false)
            setSelectedEmployee(null)
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
            Are you sure you want to delete <strong>{selectedEmployee?.full_name}</strong>?
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
