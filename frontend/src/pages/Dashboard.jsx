
import {
  School,
  TriangleAlert,
  CircleAlert,
  CircleCheck,
} from 'lucide-react'

import './Dashboard.css'
import { demoSchools } from '../data/demoSchools'

function Dashboard({ schools = demoSchools }) {
  const isBackendData = schools !== demoSchools

  const latestSnapshots = schools.map((school) => {
    const snapshots = school.prioritySnapshots

    if (!Array.isArray(snapshots) || snapshots.length === 0) {
      return null
    }

    return [...snapshots].sort(
      (a, b) =>
        new Date(b.snapshotDate ?? 0) -
        new Date(a.snapshotDate ?? 0)
    )[0]
  })

  const assessedSchools = latestSnapshots.filter(
    (snapshot) => snapshot?.priorityScore != null
  ).length

  const activeIssues = latestSnapshots.reduce(
    (total, snapshot) =>
      total + (Number(snapshot?.activeIssues) || 0),
    0
  )

  const missingAssessments =
    schools.length - assessedSchools

  const stats = isBackendData
    ? [
        {
          title: 'Total Schools',
          value: schools.length,
          description: 'Known schools loaded from backend',
          icon: School,
          color: 'blue',
        },
        {
          title: 'Assessed Schools',
          value: assessedSchools,
          description: 'Schools with a recorded priority score',
          icon: CircleCheck,
          color: 'green',
        },
        {
          title: 'Active Issues',
          value: activeIssues,
          description: 'Active issues in latest priority snapshots',
          icon: TriangleAlert,
          color: 'red',
        },
        {
          title: 'Missing Assessments',
          value: missingAssessments,
          description: 'Schools without a recorded priority score',
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
            ? `Showing ${schools.length} known school records fetched from Spring Boot and MySQL. Statistics use the latest available priority snapshots.`
            : 'Statistics are based on demonstration data.'}
        </p>
      </div>

      <div className="stats-grid">
        {stats.map((stat) => {
          const Icon = stat.icon

          return (
            <div className="stat-card" key={stat.title}>
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
