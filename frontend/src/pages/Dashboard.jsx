
import {
  School,
  TriangleAlert,
  CircleAlert,
  CircleCheck,
} from 'lucide-react'

import './Dashboard.css'
import { demoSchools } from '../data/demoSchools'

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

function Dashboard({ schools = demoSchools }) {
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

  return (
    <div className="dashboard">
      <div className="dashboard-heading">
        <h1>Dashboard Overview</h1>

        <p>
          School Evidence & Inspection Priority System
        </p>

        <p className="dashboard-demo-note">
          {isBackendData
            ? `Showing ${schools.length} top-priority school records from Spring Boot and MySQL. The backend ranks up to 50 schools by their latest priority scores. Schools without priority assessments are excluded. These are not statewide totals.`
            : 'Statistics are based on demonstration data.'}
        </p>
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
    </div>
  )
}

export default Dashboard
