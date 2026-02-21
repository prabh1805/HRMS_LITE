import Spinner from './Spinner'

export default function PageLoader({ message = 'Loading...' }) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[400px] space-y-4">
      <Spinner size="xl" className="text-indigo-600" />
      <p className="text-gray-600 font-medium">{message}</p>
    </div>
  )
}
