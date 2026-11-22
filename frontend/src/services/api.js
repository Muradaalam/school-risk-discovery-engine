
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
export async function getKnownSchools(token) {
  const schoolIds = [1000000, 1000001, 1000002]

  return Promise.all(
    schoolIds.map((id) => getSchoolById(id, token))
  )
}

