import { useState } from 'react'
import Table from '../ui/Table'
import Button from '../ui/Button'
import Pagination from '../ui/Pagination'

export default function EmployeeTable({ employees, onDelete, onEdit }) {
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 10

  const columns = [
    { key: 'employee_id', label: 'Employee ID' },
    { key: 'full_name', label: 'Name' },
    { key: 'email', label: 'Email' },
    { key: 'department', label: 'Department' },
  ]

  const actions = (employee) => (
    <div className="flex gap-2">
      <Button
        variant="secondary"
        onClick={() => onEdit(employee)}
        className="text-sm px-3 py-1"
      >
        ✏️ Edit
      </Button>
      <Button
        variant="danger"
        onClick={() => onDelete(employee)}
        className="text-sm px-3 py-1"
      >
        🗑️ Delete
      </Button>
    </div>
  )

  // Pagination logic
  const totalPages = Math.ceil(employees.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  const paginatedEmployees = employees.slice(startIndex, endIndex)

  const handlePageChange = (page) => {
    setCurrentPage(page)
  }

  return (
    <div>
      <Table columns={columns} data={paginatedEmployees} actions={actions} />
      <Pagination
        currentPage={currentPage}
        totalPages={totalPages}
        onPageChange={handlePageChange}
        totalItems={employees.length}
        itemsPerPage={itemsPerPage}
      />
    </div>
  )
}
