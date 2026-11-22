
import './Schools.css'

import { useState } from 'react'
import { Search, Filter } from 'lucide-react'
import { demoSchools } from '../data/demoSchools'
import { normalizeSchool } from '../utils/normalizeSchool'

function getLatestSnapshot(school) {
  const snapshots = Array.isArray(school.prioritySnapshots)
    ? school.prioritySnapshots
    : []

  return [...snapshots].sort(
    (a, b) => {
      const dateDifference =
        new Date(b.snapshotDate ?? 0) -
        new Date(a.snapshotDate ?? 0)

      return dateDifference || (b.id ?? 0) - (a.id ?? 0)
    }
  )[0] ?? null
}

function Schools({ onSchoolSelect, schools = demoSchools }) {
  const [searchTerm, setSearchTerm] = useState('')
  const [priorityFilter, setPriorityFilter] = useState('All')

  const isBackendData = schools !== demoSchools

  const normalizedSchools = schools.map((school) => {
    const normalized = normalizeSchool(school)

    if (!isBackendData) {
      return normalized
    }

    const snapshot = getLatestSnapshot(school)

    return {
      ...normalized,
      latestPriorityScore: snapshot?.priorityScore ?? null,
    }
  })

  const availableScores = [
    ...new Set(
      normalizedSchools
        .map((school) => school.latestPriorityScore)
        .filter((score) => score !== null && score !== undefined)
        .map(String)
    ),
  ].sort((a, b) => Number(a) - Number(b))

  const filteredSchools = normalizedSchools.filter((school) => {
    const search = searchTerm.toLowerCase().trim()

    const matchesSearch =
      String(school.name ?? '').toLowerCase().includes(search) ||
      String(school.district ?? '').toLowerCase().includes(search) ||
      String(school.udise ?? '').toLowerCase().includes(search)

    let matchesPriority = priorityFilter === 'All'

    if (!matchesPriority && isBackendData) {
      if (priorityFilter === 'Not Assessed') {
        matchesPriority =
          school.latestPriorityScore === null ||
          school.latestPriorityScore === undefined
      } else {
        matchesPriority =
          String(school.latestPriorityScore) === priorityFilter
      }
    }

    if (!matchesPriority && !isBackendData) {
      matchesPriority = school.priority === priorityFilter
    }

    return matchesSearch && matchesPriority
  })

  return (
    <div className="schools-page">
      <div className="schools-heading">
        <h1>
          {isBackendData
            ? 'Top Priority Schools'
            : 'Schools Directory'}
        </h1>

        <p>
          {isBackendData
            ? 'Schools ranked by their latest recorded priority score. The backend returns up to 50 assessed schools.'
            : 'Explore school records, evidence, and inspection priorities.'}
        </p>
      </div>

      <div className="schools-table-card">
        <div className="schools-table-header">
          <h2>
            {isBackendData
              ? 'Top 50 Assessed Schools'
              : 'All Schools'}
          </h2>

          <span className="demo-label">
            {isBackendData ? 'Backend Data' : 'Demo Data'}
          </span>
        </div>

        <div className="schools-controls">
          <div className="schools-search">
            <Search size={18} />

            <input
              type="text"
              placeholder="Search by school, district, or UDISE..."
              value={searchTerm}
              onChange={(event) =>
                setSearchTerm(event.target.value)
              }
            />
          </div>

          <div className="schools-filter">
            <Filter size={18} />

            <select
              value={priorityFilter}
              onChange={(event) =>
                setPriorityFilter(event.target.value)
              }
              aria-label={
                isBackendData
                  ? 'Filter by priority score'
                  : 'Filter by inspection priority'
              }
            >
              <option value="All">
                {isBackendData
                  ? 'All Scores'
                  : 'All Priorities'}
              </option>

              {isBackendData ? (
                <>
                  {availableScores.map((score) => (
                    <option key={score} value={score}>
                      Priority Score {score}
                    </option>
                  ))}

                  <option value="Not Assessed">
                    Not Assessed
                  </option>
                </>
              ) : (
                <>
                  <option value="High">High Priority</option>
                  <option value="Medium">Medium Priority</option>
                  <option value="Low">Low Priority</option>
                  <option value="Not Assessed">
                    Not Assessed
                  </option>
                </>
              )}
            </select>
          </div>
        </div>

        <div className="schools-table-wrapper">
          <table className="schools-table">
            <thead>
              <tr>
                <th>School Name</th>
                <th>UDISE Code</th>
                <th>District</th>
                <th>Evidence</th>
                <th>
                  {isBackendData
                    ? 'Priority Score'
                    : 'Inspection Priority'}
                </th>
              </tr>
            </thead>

            <tbody>
              {filteredSchools.map((school) => (
                <tr
                  key={school.id}
                  className="clickable-school-row"
                  onClick={() => onSchoolSelect(school)}
                  tabIndex={0}
                  role="button"
                  onKeyDown={(event) => {
                    if (
                      event.key === 'Enter' ||
                      event.key === ' '
                    ) {
                      event.preventDefault()
                      onSchoolSelect(school)
                    }
                  }}
                >
                  <td className="school-name">
                    {school.name}
                  </td>

                  <td>{school.udise}</td>

                  <td>{school.district}</td>

                  <td>{school.evidenceCount}</td>

                  <td>
                    {isBackendData ? (
                      <span className="priority-badge priority-not-assessed">
                        {school.latestPriorityScore !== null &&
                        school.latestPriorityScore !== undefined
                          ? `Score ${school.latestPriorityScore}`
                          : 'Not Assessed'}
                      </span>
                    ) : (
                      <span
                        className={`priority-badge priority-${school.priority
                          .toLowerCase()
                          .replace(/\s+/g, '-')}`}
                      >
                        {school.priority}
                      </span>
                    )}
                  </td>
                </tr>
              ))}

              {filteredSchools.length === 0 && (
                <tr>
                  <td
                    colSpan="5"
                    className="schools-empty"
                  >
                    No schools match your search or filter.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        <p className="schools-result-count">
          Showing {filteredSchools.length} of {schools.length}{' '}
          {isBackendData
            ? 'top-priority school records'
            : 'schools'}
        </p>

        {isBackendData && (
          <p className="schools-result-count">
            Schools without priority assessments are excluded
            by the backend. Numeric scores are displayed as
            recorded and have not been mapped to High,
            Medium, or Low categories.
          </p>
        )}
      </div>
    </div>
  )
}

export default Schools
