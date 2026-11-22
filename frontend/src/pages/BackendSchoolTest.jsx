
import { useState } from 'react'
import { getSchoolById } from '../services/api'
import Loading from '../components/Loading'
import ErrorMessage from '../components/ErrorMessage'

function BackendSchoolTest() {
  const [token, setToken] = useState('')
  const [school, setSchool] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function fetchSchool(event) {
    event.preventDefault()
    setLoading(true)
    setError('')
    setSchool(null)

    try {
      const data = await getSchoolById(1000001, token.trim())
      setSchool(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="school-details-page">
      <h1>Backend Connection Test</h1>
      <p>Development testing only — school ID 1000001</p>

      <form onSubmit={fetchSchool}>
        <input
          type="password"
          placeholder="Paste a fresh JWT token"
          value={token}
          onChange={(event) => setToken(event.target.value)}
          required
          autoComplete="off"
          aria-label="JWT token"
        />

        <button type="submit">Fetch School</button>
      </form>

      {loading && <Loading message="Fetching school..." />}

      {error && <ErrorMessage message={error} />}

      {school && (
        <div>
          <h2>{school.schoolName}</h2>
          <p>UDISE: {school.udiseCode}</p>
          <p>District: {school.district}</p>
          <p>State: {school.state}</p>
          <p>
            Priority Score:{' '}
            {school.prioritySnapshots?.[0]?.priorityScore ?? 'Not available'}
          </p>
        </div>
      )}
    </div>
  )
}

export default BackendSchoolTest
