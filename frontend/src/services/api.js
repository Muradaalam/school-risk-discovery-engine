
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

export async function apiGet(endpoint, token) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: token
      ? { Authorization: `Bearer ${token}` }
      : {},
  })

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`)
  }

  return response.json()
}

export async function getSchoolById(id, token) {
  return apiGet(
    `/school-service/school/getSchool/id?id=${encodeURIComponent(id)}`,
    token
  )
}

// Fetch up to 50 schools ranked by their latest priority score.
// Schools without priority assessments are excluded by the backend.
export async function getTop50Schools(token) {
  const schools = await apiGet(
    '/school-service/school/getTop50Schools',
    token
  )

  if (!Array.isArray(schools)) {
    throw new Error('Unexpected response: expected a school list')
  }

  return schools
}

// Keep the existing export temporarily so App.jsx continues to work.
// It now uses the dynamic API instead of hardcoded school IDs.
export async function getKnownSchools(token) {
  return getTop50Schools(token)
}
