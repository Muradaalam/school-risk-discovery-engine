
import './Schools.css'

import { useState } from 'react'
import { Search, Filter } from 'lucide-react'
import { demoSchools } from '../data/demoSchools'

// Temporary demonstration data.
// Replace with actual backend data later.



function Schools({ onSchoolSelect }) {
  const [searchTerm, setSearchTerm] = useState('')
  const [priorityFilter, setPriorityFilter] = useState('All')

  const filteredSchools = demoSchools.filter((school) => {
    const search = searchTerm.toLowerCase().trim()

    const matchesSearch =
      school.name.toLowerCase().includes(search) ||
      school.district.toLowerCase().includes(search) ||
      school.udise.toLowerCase().includes(search)

    const matchesPriority =
      priorityFilter === 'All' ||
      school.priority === priorityFilter

    return matchesSearch && matchesPriority
  })

  return (
    <div className="schools-page">
      <div className="schools-heading">
        <h1>Schools Directory</h1>
        <p>
          Explore school records, evidence, and inspection priorities.
        </p>
      </div>

      <div className="schools-table-card">
        <div className="schools-table-header">
          <h2>All Schools</h2>
          <span className="demo-label">Demo Data</span>
        </div>

        <div className="schools-controls">
          <div className="schools-search">
            <Search size={18} />
            <input
              type="text"
              placeholder="Search by school, district, or UDISE..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <div className="schools-filter">
            <Filter size={18} />
            <select
              value={priorityFilter}
              onChange={(e) => setPriorityFilter(e.target.value)}
              aria-label="Filter by inspection priority"
            >
              <option value="All">All Priorities</option>
              <option value="High">High Priority</option>
              <option value="Medium">Medium Priority</option>
              <option value="Low">Low Priority</option>
              <option value="Not Assessed">Not Assessed</option>
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
                <th>Inspection Priority</th>
              </tr>
            </thead>

            <tbody>
              {filteredSchools.map((school) => (
                <tr key={school.id}
                 className="clickable-school-row"
                 onClick={() => onSchoolSelect(school)}
                 tabIndex={0}
                 role="button"
                 onKeyDown={(event) => {
                  if (event.key === 'Enter' || event.key === ' ') {
                    event.preventDefault()
                    onSchoolSelect(school)
                  }
                }}>
                  <td className="school-name">{school.name}</td>
                  <td>{school.udise}</td>
                  <td>{school.district}</td>
                  <td>{school.evidenceCount}</td>
                  <td>
                    <span
                      className={`priority-badge priority-${school.priority
                        .toLowerCase()
                        .replace(/\s+/g, '-')}`}
                    >
                      {school.priority}
                    </span>
                  </td>
                </tr>
              ))}

              {filteredSchools.length === 0 && (
                <tr>
                  <td colSpan="5" className="schools-empty">
                    No schools match your search or filter.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        <p className="schools-result-count">
          Showing {filteredSchools.length} of {demoSchools.length} schools
        </p>
      </div>
    </div>
  )
}

export default Schools
