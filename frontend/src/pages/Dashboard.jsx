
import {
  School,
  TriangleAlert,
  CircleAlert,
  CircleCheck,
} from 'lucide-react'

import './Dashboard.css'
import { demoSchools } from '../data/demoSchools'

function getPriorityLabel(score) {
  const labels = {
    0: 'No Priority',
    1: 'Low Priority',
    2: 'Medium Priority',
    3: 'High Priority',
  }

  if (score === null || score === undefined) {
    return 'Not Assessed'
  }

  return labels[score] ?? `Score ${score}`
}

function getLatestSnapshot(school) {
  const snapshots = Array.isArray(school.prioritySnapshots)
    ? school.prioritySnapshots
    : []

  return [...snapshots].sort((a, b) => {
    const dateDifference =
      new Date(b.snapshotDate ?? 0) -
      new Date(a.snapshotDate ?? 0)

    return dateDifference || (b.id ?? 0) - (a.id ?? 0)
  })[0] ?? null
}

function Dashboard({
  schools = demoSchools,
  onSchoolSelect,
}) {
  const isBackendData = schools !== demoSchools

  const latestSnapshots = isBackendData
    ? schools.map(getLatestSnapshot)
    : []

  const assessedSchools = latestSnapshots.filter(
    (snapshot) => snapshot?.priorityScore != null
  ).length

  const activeIssues = isBackendData
    ? schools.reduce((total, school) => {
        const issues = Array.isArray(school.issues)
          ? school.issues
          : []

        return total + issues.filter(
          (issue) => issue.status === 'ACTIVE'
        ).length
      }, 0)
    : 0

  const totalIssues = isBackendData
    ? schools.reduce(
        (total, school) =>
          total + (
            Array.isArray(school.issues)
              ? school.issues.length
              : 0
          ),
        0
      )
    : 0

  const stats = isBackendData
    ? [
        {
          title: 'Top Schools Loaded',
          value: schools.length,
          description: 'Up to 50 schools ranked by latest priority score',
          icon: School,
          color: 'blue',
        },
        {
          title: 'Assessed Schools',
          value: assessedSchools,
          description: 'Loaded schools with a recorded priority score',
          icon: CircleCheck,
          color: 'green',
        },
        {
          title: 'Active Issues',
          value: activeIssues,
          description: 'Issues with ACTIVE status in loaded schools',
          icon: TriangleAlert,
          color: 'red',
        },
        {
          title: 'Total Reported Issues',
          value: totalIssues,
          description: 'All reported issues across loaded schools',
          icon: CircleAlert,
          color: 'orange',
        },
      ]
    : [
        {
          title: 'Total Schools',
          value: schools.length,
          description: 'Schools in the demo dataset',
          icon: School,
          color: 'blue',
        },
        {
          title: 'High Priority',
          value: schools.filter(
            (school) => school.priority === 'High'
          ).length,
          description: 'Priority for inspection',
          icon: TriangleAlert,
          color: 'red',
        },
        {
          title: 'Medium Priority',
          value: schools.filter(
            (school) => school.priority === 'Medium'
          ).length,
          description: 'Priority for inspection',
          icon: CircleAlert,
          color: 'orange',
        },
        {
          title: 'Low Priority',
          value: schools.filter(
            (school) => school.priority === 'Low'
          ).length,
          description: 'Priority for inspection',
          icon: CircleCheck,
          color: 'green',
        },
      ]

  const prioritySchools = isBackendData
    ? schools
        .map((school) => ({
          school,
          snapshot: getLatestSnapshot(school),
        }))
        .filter(
          ({ snapshot }) =>
            snapshot?.priorityScore != null
        )
        .sort(
          (a, b) =>
            Number(b.snapshot.priorityScore) -
            Number(a.snapshot.priorityScore)
        )
    : []

  return (
    <div className="dashboard">
      <div className="dashboard-heading">
        <h1>Dashboard Overview</h1>
      </div>

      <div className="stats-grid">
        {stats.map((stat) => {
          const Icon = stat.icon

          return (
            <div
              className="stat-card"
              key={stat.title}
            >
              <div className="stat-card-top">
                <span className="stat-title">
                  {stat.title}
                </span>

                <div className={`stat-icon ${stat.color}`}>
                  <Icon size={22} />
                </div>
              </div>

              <h2 className="stat-value">
                {stat.value}
              </h2>

              <p className="stat-description">
                {stat.description}
              </p>
            </div>
          )
        })}
      </div>

      {isBackendData && (
        <section className="dashboard-priority-section">
          <div className="dashboard-priority-header">
            <div>
              <h2>Top Priority Schools</h2>
              <p>
                Schools ranked by their latest recorded
                priority score
              </p>
            </div>

            <span className="dashboard-school-count">
              {prioritySchools.length} schools
            </span>
          </div>

          {prioritySchools.length === 0 ? (
            <p className="dashboard-empty">
              No priority-assessed schools available.
            </p>
          ) : (
            <div className="dashboard-table-wrapper">
              <table className="dashboard-school-table">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>School Name</th>
                    <th>District</th>
                    <th>School ID</th>
                    <th>Priority Level</th>
                  </tr>
                </thead>

                <tbody>
                  {prioritySchools.map(
                    ({ school, snapshot }, index) => {
                      const schoolKey =
                        school.id ??
                        school.schoolId ??
                        index

                      const schoolName =
                        school.schoolName ??
                        school.name ??
                        'Unnamed School'

                      const schoolId =
                        school.schoolId ??
                        school.id ??
                        'N/A'

                      return (
                        <tr key={schoolKey}>
                          <td>{index + 1}</td>

                          <td>
                            {typeof onSchoolSelect ===
                            'function' ? (
                              <button
                                type="button"
                                className="dashboard-school-link"
                                onClick={() =>
                                  onSchoolSelect(school)
                                }
                              >
                                {schoolName}
                              </button>
                            ) : (
                              <span className="dashboard-school-name">
                                {schoolName}
                              </span>
                            )}
                          </td>

                          <td>
                            {school.district ?? 'N/A'}
                          </td>

                          <td>{schoolId}</td>

                          <td>
                            <span className="dashboard-score">
                              {getPriorityLabel(
                                snapshot.priorityScore
                              )}
                              {' '}
                              (Score {snapshot.priorityScore})
                            </span>
                          </td>
                        </tr>
                      )
                    }
                  )}
                </tbody>
              </table>
            </div>
          )}
        </section>
      )}
    </div>
  )
}

export default Dashboard
