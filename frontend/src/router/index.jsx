import { Routes, Route } from 'react-router-dom'
import PageLayout from '../layout/PageLayout'
import Dashboard from '../pages/Dashboard'
import Employees from '../pages/Employees'
import Attendance from '../pages/Attendance'

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<PageLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="employees" element={<Employees />} />
        <Route path="attendance" element={<Attendance />} />
      </Route>
    </Routes>
  )
}
