import { motion } from 'framer-motion'

export default function Card({ children, className = '', hover = false }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      whileHover={hover ? { y: -4, boxShadow: '0 20px 40px -10px rgba(0, 0, 0, 0.15)' } : {}}
      className={`bg-white rounded-2xl shadow-md border border-gray-100 p-6 transition-all duration-200 ${className}`}
    >
      {children}
    </motion.div>
  )
}
