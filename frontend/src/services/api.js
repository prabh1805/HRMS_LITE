import axios from 'axios'
import { API_BASE_URL } from '../utils/constants'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Employees
export const getEmployees = () => api.get('/v1/employees')
export const createEmployee = (data) => api.post('/v1/employees', data)
export const updateEmployee = (id, data) => api.put(`/v1/employees/${id}`, data)
export const deleteEmployee = (id) => api.delete(`/v1/employees/${id}`)

// Attendance
export const getAttendance = (startDate = null, endDate = null) => {
  const params = new URLSearchParams()
  if (startDate) params.append('start_date', startDate)
  if (endDate) params.append('end_date', endDate)
  const queryString = params.toString()
  return api.get(`/v1/attendance${queryString ? `?${queryString}` : ''}`)
}
export const markAttendance = (data) => api.post('/v1/attendance', data)
export const updateAttendance = (id, data) => api.put(`/v1/attendance/${id}`, data)
export const deleteAttendance = (id) => api.delete(`/v1/attendance/${id}`)
export const getAttendanceSummary = () => api.get('/v1/attendance/summary/by-employee')
export const getDashboardStats = () => api.get('/v1/dashboard/stats')

export default api
