
import { AlertCircle, RefreshCw } from 'lucide-react'
import './ErrorMessage.css'

function ErrorMessage({
  message = 'Something went wrong. Please try again.',
  onRetry,
}) {
  return (
    <div className="error-container" role="alert">
      <AlertCircle
        size={36}
        className="error-icon"
        aria-hidden="true"
      />

      <h2>Unable to Load Data</h2>

      <p>{message}</p>

      {onRetry && (
        <button
          type="button"
          className="retry-button"
          onClick={onRetry}
        >
          <RefreshCw size={16} />
          Try Again
        </button>
      )}
    </div>
  )
}

export default ErrorMessage
