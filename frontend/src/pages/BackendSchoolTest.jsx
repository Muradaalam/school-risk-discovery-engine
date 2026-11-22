
import { useState } from 'react'
import { getSchoolById } from '../services/api'
import Loading from '../components/Loading'
import ErrorMessage from '../components/ErrorMessage'
import SchoolDetails from './SchoolDetails'

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
    if (school) {
    return (
      <SchoolDetails
        school={school}
        onBack={() => setSchool(null)}
      />
    )
  }

  return (
    <div className="school-details-page">
      <h1>Live School Data</h1>
<p>
  View a real school record retrieved from the Spring Boot backend
  and MySQL database.
</p>
<p>
  Demo school ID: 1000001 — authentication token required.
</p>

      <form
          onSubmit={fetchSchool}
          style={{
            display: 'flex',
            gap: '12px',
            alignItems: 'center',
            flexWrap: 'wrap',
            marginTop: '24px',
          }}
        >
        <input
          type="password"
          style={{
            padding: '12px 16px',
            borderRadius: '8px',
            border: '1px solid #cbd5e1',
            fontSize: '14px',
            width: '320px',
            maxWidth: '100%',
          }}
          placeholder="Paste a fresh JWT token"
          value={token}
          onChange={(event) => setToken(event.target.value)}
          required
          autoComplete="off"
          aria-label="JWT token"
        />

        <button
  type="submit"
  disabled={loading}
  style={{
    padding: '12px 20px',
    backgroundColor: '#2563eb',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: loading ? 'not-allowed' : 'pointer',
  }}
>
  {loading ? 'Fetching...' : 'Fetch School'}
</button>
      </form>

      {loading && <Loading message="Fetching school..." />}

      {error && <ErrorMessage message={error} />}


    </div>
  )
}

export default BackendSchoolTest
