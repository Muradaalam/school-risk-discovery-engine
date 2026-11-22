export function normalizeSchool(school) {
  return {
    ...school,
    name: school.schoolName ?? school.name,
    udise: school.udiseCode ?? school.udise,
    district: school.district,
    priority: school.priority ?? 'Not Assessed',
    evidenceCount: school.evidenceCount ?? 'Not available',
  }
}