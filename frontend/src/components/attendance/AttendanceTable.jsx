import { useState } from 'react'
import Table from '../ui/Table'
import Badge from '../ui/Badge'
import Button from '../ui/Button'
import Pagination from '../ui/Pagination'

export default function AttendanceTable({ attendance, onEdit, onDelete }) {
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 15

  const columns = [
    { key: 'employee_code', label: 'Employee ID' },
    { key: 'employee_name', label: 'Employee Name' },
    { key: 'date', label: 'Date' },
    { 
      key: 'status', 
      label: 'Status',
      render: (status) => <Badge status={status} />
    },
  ]

  const actions = (record) => (
    <div className="flex gap-2">
      <Button
        variant="secondary"
        onClick={() => onEdit(record)}
        className="text-sm px-3 py-1"
      >
        ✏️ Edit
      </Button>
      <Button
        variant="danger"
        onClick={() => onDelete(record)}
        className="text-sm px-3 py-1"
      >
        🗑️ Delete
      </Button>
    </div>
  )

  // Pagination logic
  const totalPages = Math.ceil(attendance.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  const paginatedAttendance = attendance.slice(startIndex, endIndex)

  const handlePageChange = (page) => {
    setCurrentPage(page)
  }

  return (
    <div>
      <Table columns={columns} data={paginatedAttendance} actions={actions} />
      <Pagination
        currentPage={currentPage}
        totalPages={totalPages}
        onPageChange={handlePageChange}
        totalItems={attendance.length}
        itemsPerPage={itemsPerPage}
      />
    </div>
  )
}
