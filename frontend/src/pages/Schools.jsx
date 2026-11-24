
import { useEffect, useState } from 'react'
import { Search, Filter } from 'lucide-react'

import './Schools.css'
import { demoSchools } from '../data/demoSchools'
import { normalizeSchool } from '../utils/normalizeSchool'
import { apiGet } from '../services/api'



const PRIORITY_LEVELS = [
  { value: '0', label: 'No Priority', className: 'priority-low' },
  { value: '1', label: 'Low Priority', className: 'priority-low' },
  { value: '2', label: 'Medium Priority', className: 'priority-medium' },
  { value: '3', label: 'High Priority', className: 'priority-high' },
]

function getPriorityDetails(score) {
  if (score === null || score === undefined) {
    return {
      label: 'Not Assessed',
      className: 'priority-not-assessed',
    }
  }

  return (
    PRIORITY_LEVELS.find(
      (level) => level.value === String(score)
    ) ?? {
      label: `Score ${score}`,
      className: 'priority-not-assessed',
    }
  )
}


function getLatestScore(school) {
  const snapshots = Array.isArray(school.prioritySnapshots)
    ? school.prioritySnapshots
    : []

  const latest = [...snapshots].sort((a, b) => {
    const dateDifference =
      new Date(b.snapshotDate ?? 0) -
      new Date(a.snapshotDate ?? 0)

    return dateDifference || (b.id ?? 0) - (a.id ?? 0)
  })[0]

  return latest?.priorityScore ?? null
}

function Schools({ onSchoolSelect, schools = demoSchools }) {
  const isBackendData = schools !== demoSchools

  const [searchTerm, setSearchTerm] = useState('')
  const [priorityFilter, setPriorityFilter] = useState('All')

  const [searchResults, setSearchResults] = useState(null)
  const [searchLoading, setSearchLoading] = useState(false)
  const [searchError, setSearchError] = useState('')

  const searchQuery = searchTerm.trim()
  const needsBackendSearch =
    isBackendData &&
    (searchQuery !== '' || priorityFilter !== 'All')

  useEffect(() => {
    let cancelled = false

    if (!needsBackendSearch) {
      return () => {
        cancelled = true
      }
    }

    const timer = setTimeout(async () => {
      if (cancelled) return

      setSearchLoading(true)
      setSearchError('')

      try {
        const params = new URLSearchParams()
        params.set('query', searchQuery)

        if (
          priorityFilter !== 'All' &&
          priorityFilter !== 'Not Assessed'
        ) {
          params.set('priorityScore', priorityFilter)
        }

        const results = await apiGet(
          `/school-service/school/search?${params.toString()}`
        )

        if (!Array.isArray(results)) {
          throw new Error('Invalid response from school search API')
        }

        if (!cancelled) {
          setSearchResults(results)
        }
      } catch (error) {
        if (!cancelled) {
          setSearchResults([])
          setSearchError(error.message)
        }
      } finally {
        if (!cancelled) {
          setSearchLoading(false)
        }
      }
    }, 400)

    return () => {
      cancelled = true
      clearTimeout(timer)
    }
  }, [
    searchQuery,
    priorityFilter,
    isBackendData,
    needsBackendSearch,
  ])



  const sourceSchools = isBackendData
    ? (
        needsBackendSearch
          ? (searchResults ?? [])
          : schools
      )
    : schools

  const preparedSchools = sourceSchools.map((school) => ({
    original: school,
    normalized: normalizeSchool(school),
    score: isBackendData ? getLatestScore(school) : null,
  }))

  const filteredSchools = preparedSchools.filter((item) => {
    const { original, normalized, score } = item

    if (isBackendData) {
      if (priorityFilter === 'Not Assessed') {
        return score == null
      }

      if (priorityFilter === 'All') {
        return true
      }

      return String(score) === priorityFilter
    }

    const query = searchQuery.toLowerCase()

    const matchesSearch =
      !query ||
      String(normalized.name ?? '')
        .toLowerCase()
        .includes(query) ||
      String(normalized.district ?? '')
        .toLowerCase()
        .includes(query) ||
      String(normalized.udise ?? '')
        .toLowerCase()
        .includes(query) ||
      String(original.id ?? '')
        .toLowerCase()
        .includes(query)

    const matchesPriority =
      priorityFilter === 'All' ||
      normalized.priority === priorityFilter

    return matchesSearch && matchesPriority
  })

  function selectSchool(item) {
    onSchoolSelect(
      isBackendData ? item.original : item.normalized
    )
  }

  return (
    <div className="schools-page">
      <div className="schools-heading">
        <h1>Schools Directory</h1>

        <p>
          {isBackendData
            ? 'Search school records directly from MySQL by name, ID, UDISE code, district, or priority score.'
            : 'Explore demonstration school records and inspection priorities.'}
        </p>
      </div>

      <div className="schools-table-card">
        <div className="schools-table-header">
          <h2>
            {isBackendData
              ? (
                  needsBackendSearch
                    ? 'Database Search Results'
                    : 'Top Priority Schools'
                )
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
              type="search"
              placeholder={
                isBackendData
                  ? 'Search name, ID, UDISE or district...'
                  : 'Search school, district or UDISE...'
              }
              value={searchTerm}
              onChange={(event) => {
                setSearchTerm(event.target.value)
                setSearchResults(null)
                setSearchError('')
              }}
              aria-label="Search schools"
            />
          </div>

          <div className="schools-filter">
            <Filter size={18} />

            <select
              value={priorityFilter}
              onChange={(event) => {
                setPriorityFilter(event.target.value)
                setSearchResults(null)
                setSearchError('')
              }}
              aria-label="Filter schools by priority"
            >
              <option value="All">
                {isBackendData
                  ? 'All Scores'
                  : 'All Priorities'}
              </option>

              {isBackendData ? (
  <>
    {PRIORITY_LEVELS.map((level) => (
      <option key={level.value} value={level.value}>
        {level.label}
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

        {isBackendData && (
          <p
            style={{
              margin: '12px 0',
              fontSize: '13px',
              color: '#64748b',
            }}
          >
            {needsBackendSearch
              ? 'Searching the full school database. Results update automatically as you type.'
              : 'Showing up to 50 assessed schools. Start typing to search the full database.'}
          </p>
        )}

        {searchLoading && (
          <p role="status" style={{ color: '#2563eb' }}>
            Searching database...
          </p>
        )}

        {searchError && (
          <p role="alert" style={{ color: '#b91c1c' }}>
            Search failed: {searchError}
          </p>
        )}

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
              {filteredSchools.map((item) => {
                const school = item.normalized

                return (
                  <tr
                    key={item.original.id}
                    className="clickable-school-row"
                    onClick={() => selectSchool(item)}
                    tabIndex={0}
                    role="button"
                    onKeyDown={(event) => {
                      if (
                        event.key === 'Enter' ||
                        event.key === ' '
                      ) {
                        event.preventDefault()
                        selectSchool(item)
                      }
                    }}
                  >
                    <td className="school-name">
                      {school.name}
                    </td>

                    <td>{school.udise}</td>
                    <td>{school.district}</td>
                    <td>{school.evidenceCount ?? 0}</td>

                    <td>
{isBackendData ? (
  <span
    className={`priority-badge ${
      getPriorityDetails(item.score).className
    }`}
  >
    {getPriorityDetails(item.score).label}
  </span>
) : (
                        <span
                          className={`priority-badge priority-${String(
                            school.priority
                          )
                            .toLowerCase()
                            .replace(/\s+/g, '-')}`}
                        >
                          {school.priority}
                        </span>
                      )}
                    </td>
                  </tr>
                )
              })}

              {filteredSchools.length === 0 && (
                <tr>
                  <td
                    colSpan="5"
                    className="schools-empty"
                  >
                    {searchLoading
                      ? 'Searching database...'
                      : 'No matching schools found.'}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        <p className="schools-result-count">
          Showing {filteredSchools.length} school records
          {isBackendData && needsBackendSearch
            ? ' from database search'
            : ''}
        </p>

        {isBackendData && (
          <p className="schools-result-count">
            Database search returns up to 100 matching
            records. Schools without priority scores can
            also be found.
          </p>
        )}
      </div>
    </div>
  )
}

export default Schools
