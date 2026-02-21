import { useState, useEffect } from 'react'
import Card from '../components/ui/Card'
import PageLoader from '../components/ui/PageLoader'
import ErrorState from '../components/ui/ErrorState'
import Pagination from '../components/ui/Pagination'
import { getDashboardStats, getAttendanceSummary } from '../services/api'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [summary, setSummary] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 10

  const fetchStats = async () => {
    setLoading(true)
    setError(null)
    try {
      const [statsRes, summaryRes] = await Promise.all([
        getDashboardStats(),
        getAttendanceSummary()
      ])
      setStats(statsRes.data)
      setSummary(summaryRes.data)
    } catch (err) {
      setError(err.message || 'Failed to load dashboard stats')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchStats()
  }, [])

  if (loading) return <PageLoader message="Loading dashboard..." />
  if (error) return <ErrorState message={error} onRetry={fetchStats} />

  const statCards = [
    { 
      label: 'Total Employees', 
      value: stats?.total_employees || 0, 
      icon: '👥',
      gradient: 'from-blue-500 to-indigo-600',
      bgGradient: 'from-blue-50 to-indigo-50'
    },
    { 
      label: 'Present Today', 
      value: stats?.present_today || 0, 
      icon: '✅',
      gradient: 'from-green-500 to-emerald-600',
      bgGradient: 'from-green-50 to-emerald-50'
    },
    { 
      label: 'Absent Today', 
      value: stats?.absent_today || 0, 
      icon: '❌',
      gradient: 'from-red-500 to-rose-600',
      bgGradient: 'from-red-50 to-rose-50'
    },
  ]

  const attendanceRate = stats?.total_employees > 0 
    ? ((stats?.present_today / stats?.total_employees) * 100).toFixed(1)
    : 0

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {statCards.map((stat, index) => (
          <Card key={index} hover>
            <div className={`bg-gradient-to-br ${stat.bgGradient} rounded-lg p-6 -m-6 mb-0`}>
              <div className="flex items-center justify-between mb-4">
                <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${stat.gradient} flex items-center justify-center text-2xl shadow-lg`}>
                  {stat.icon}
                </div>
              </div>
              <p className="text-sm font-medium text-gray-600 mb-1">{stat.label}</p>
              <p className={`text-4xl font-bold bg-gradient-to-r ${stat.gradient} bg-clip-text text-transparent`}>
                {stat.value}
              </p>
            </div>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Attendance Rate</h3>
          <div className="flex items-center justify-center py-8">
            <div className="relative w-48 h-48">
              <svg className="transform -rotate-90 w-48 h-48">
                <circle
                  cx="96"
                  cy="96"
                  r="80"
                  stroke="#e5e7eb"
                  strokeWidth="16"
                  fill="none"
                />
                <circle
                  cx="96"
                  cy="96"
                  r="80"
                  stroke="url(#gradient)"
                  strokeWidth="16"
                  fill="none"
                  strokeDasharray={`${(attendanceRate / 100) * 502.4} 502.4`}
                  strokeLinecap="round"
                />
                <defs>
                  <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#667eea" />
                    <stop offset="100%" stopColor="#764ba2" />
                  </linearGradient>
                </defs>
              </svg>
              <div className="absolute inset-0 flex items-center justify-center flex-col">
                <span className="text-4xl font-bold text-gray-800">{attendanceRate}%</span>
                <span className="text-sm text-gray-500 mt-1">Present</span>
              </div>
            </div>
          </div>
        </Card>

        <Card>
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Quick Stats</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center text-white font-bold">
                  %
                </div>
                <div>
                  <p className="text-sm text-gray-600">Attendance Rate</p>
                  <p className="text-xl font-bold text-gray-800">{attendanceRate}%</p>
                </div>
              </div>
            </div>
            
            <div className="flex items-center justify-between p-4 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-600 flex items-center justify-center text-white font-bold">
                  #
                </div>
                <div>
                  <p className="text-sm text-gray-600">Total Workforce</p>
                  <p className="text-xl font-bold text-gray-800">{stats?.total_employees || 0}</p>
                </div>
              </div>
            </div>
          </div>
        </Card>
      </div>

      {/* Employee Attendance Summary */}
      {summary.length > 0 && (
        <Card>
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white text-xl">
              📊
            </div>
            <h3 className="text-lg font-bold text-gray-800">Employee Attendance Summary</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Employee ID</th>
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Name</th>
                  <th className="text-center py-3 px-4 text-sm font-semibold text-gray-700">Total Present</th>
                  <th className="text-center py-3 px-4 text-sm font-semibold text-gray-700">Total Absent</th>
                  <th className="text-center py-3 px-4 text-sm font-semibold text-gray-700">Total Days</th>
                  <th className="text-center py-3 px-4 text-sm font-semibold text-gray-700">Attendance %</th>
                </tr>
              </thead>
              <tbody>
                {summary.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage).map((emp) => {
                  const attendancePercent = emp.total_days > 0 
                    ? ((emp.total_present_days / emp.total_days) * 100).toFixed(1)
                    : 0
                  return (
                    <tr key={emp.employee_id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-3 px-4 text-sm text-gray-800 font-medium">{emp.employee_id}</td>
                      <td className="py-3 px-4 text-sm text-gray-800">{emp.employee_name}</td>
                      <td className="py-3 px-4 text-center">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          {emp.total_present_days}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-center">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                          {emp.total_absent_days}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-center text-sm text-gray-800 font-medium">
                        {emp.total_days}
                      </td>
                      <td className="py-3 px-4 text-center">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          attendancePercent >= 80 ? 'bg-green-100 text-green-800' :
                          attendancePercent >= 60 ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          {attendancePercent}%
                        </span>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
          <Pagination
            currentPage={currentPage}
            totalPages={Math.ceil(summary.length / itemsPerPage)}
            onPageChange={setCurrentPage}
            totalItems={summary.length}
            itemsPerPage={itemsPerPage}
          />
        </Card>
      )}
    </div>
  )
}
