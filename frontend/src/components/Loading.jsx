
import { LoaderCircle } from 'lucide-react'
import './Loading.css'

function Loading({ message = 'Loading data...' }) {
  return (
    <div className="loading-container" role="status">
      <LoaderCircle
        size={32}
        className="loading-spinner"
        aria-hidden="true"
      />

      <p>{message}</p>
    </div>
  )
}

export default Loading
