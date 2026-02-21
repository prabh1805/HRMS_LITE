import { NavLink } from 'react-router-dom'
import { motion } from 'framer-motion'

const navItems = [
  { path: '/', label: 'Dashboard', icon: '📊' },
  { path: '/employees', label: 'Employees', icon: '👥' },
  { path: '/attendance', label: 'Attendance', icon: '📅' },
]

export default function Sidebar() {
  return (
    <aside className="w-64 bg-gradient-to-b from-indigo-600 to-purple-700 h-screen fixed left-0 top-0 shadow-xl">
      <div className="p-6 border-b border-indigo-500/30">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <span className="text-3xl">🏢</span>
          HRMS Lite
        </h1>
        <p className="text-indigo-200 text-sm mt-1">Human Resource Management</p>
      </div>
      
      <nav className="p-4 space-y-2 mt-4">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                isActive
                  ? 'bg-white text-indigo-600 font-semibold shadow-lg'
                  : 'text-indigo-100 hover:bg-white/10 hover:text-white'
              }`
            }
          >
            {({ isActive }) => (
              <motion.div
                className="flex items-center gap-3 w-full"
                whileHover={{ x: 4 }}
                transition={{ duration: 0.2 }}
              >
                <span className="text-xl">{item.icon}</span>
                <span className="text-base">{item.label}</span>
              </motion.div>
            )}
          </NavLink>
        ))}
      </nav>
      
      <div className="absolute bottom-0 left-0 right-0 p-6 border-t border-indigo-500/30">
        <div className="text-indigo-200 text-xs text-center">
          © 2026 HRMS Lite
        </div>
      </div>
    </aside>
  )
}
