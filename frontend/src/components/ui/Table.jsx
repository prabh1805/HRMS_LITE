import { motion } from 'framer-motion'

export default function Table({ columns, data, actions }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-gray-200">
            {columns.map((col) => (
              <th
                key={col.key}
                className="text-left py-3 px-4 text-sm font-medium text-gray-600"
              >
                {col.label}
              </th>
            ))}
            {actions && <th className="text-right py-3 px-4 text-sm font-medium text-gray-600">Actions</th>}
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <motion.tr
              key={row.id || index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05, duration: 0.2 }}
              className="border-b border-gray-100 hover:bg-gray-50 transition-colors duration-150"
            >
              {columns.map((col) => (
                <td key={col.key} className="py-3 px-4 text-sm text-gray-800">
                  {col.render ? col.render(row[col.key], row) : row[col.key]}
                </td>
              ))}
              {actions && (
                <td className="py-3 px-4 text-right">
                  {actions(row)}
                </td>
              )}
            </motion.tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
