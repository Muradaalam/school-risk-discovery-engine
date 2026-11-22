
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from 'recharts'

import './Analytics.css'
import { demoSchools, priorityColors } from '../data/demoSchools'

const chartColors = [
  '#2563eb',
  '#10b981',
  '#f59e0b',
  '#8b5cf6',
  '#ef4444',
  '#64748b',
]

function getLatestSnapshot(school) {
  const snapshots = Array.isArray(school.prioritySnapshots)
    ? school.prioritySnapshots
    : []

  return [...snapshots].sort(
    (a, b) =>
      new Date(b.snapshotDate ?? 0) -
      new Date(a.snapshotDate ?? 0)
  )[0] ?? null
}

function Analytics({ schools = demoSchools }) {
  const isBackendData = schools !== demoSchools

  const totalSchools = schools.length

  if (isBackendData) {
    const assessedSchools = schools.filter(
      (school) => getLatestSnapshot(school) !== null
    ).length

    const missingAssessments = totalSchools - assessedSchools

    const scoreCounts = new Map()
    const statusCounts = new Map()

    let activeIssues = 0

    schools.forEach((school) => {
      const snapshot = getLatestSnapshot(school)

      if (
        snapshot &&
        snapshot.priorityScore !== null &&
        snapshot.priorityScore !== undefined
      ) {
        const score = String(snapshot.priorityScore)

        scoreCounts.set(
          score,
          (scoreCounts.get(score) ?? 0) + 1
        )
      }

      const issues = Array.isArray(school.issues)
        ? school.issues
        : []

      issues.forEach((issue) => {
        const status = issue.status || 'UNKNOWN'

        statusCounts.set(
          status,
          (statusCounts.get(status) ?? 0) + 1
        )

        if (status === 'ACTIVE') {
          activeIssues += 1
        }
      })
    })

    const scoreData = [...scoreCounts.entries()]
      .sort((a, b) => Number(a[0]) - Number(b[0]))
      .map(([score, count], index) => ({
        name: `Score ${score}`,
        count,
        color: chartColors[index % chartColors.length],
      }))

    const assessmentData = [
      {
        name: 'Assessed',
        count: assessedSchools,
        color: '#10b981',
      },
      {
        name: 'Not Assessed',
        count: missingAssessments,
        color: '#f59e0b',
      },
    ]

    const issueStatusData = [...statusCounts.entries()]
      .sort((a, b) => a[0].localeCompare(b[0]))
      .map(([status, count], index) => ({
        name: status.replaceAll('_', ' '),
        count,
        color: chartColors[index % chartColors.length],
      }))

    const summaryItems = [
      { name: 'Total Schools', value: totalSchools },
      { name: 'Assessed Schools', value: assessedSchools },
      { name: 'Missing Assessments', value: missingAssessments },
      { name: 'Active Issues', value: activeIssues },
    ]

    return (
      <div className="analytics-page">
        <div className="analytics-header">
          <h1>School Analytics</h1>
          <p>
            Live analytics from {totalSchools} school records
            fetched from the backend. Priority scores are
            displayed as recorded, without assuming a
            High/Medium/Low mapping.
          </p>
        </div>

        <div className="analytics-summary">
          {summaryItems.map((item) => (
            <div
              className="analytics-stat-card"
              key={item.name}
            >
              <p>{item.name}</p>
              <h2>{item.value}</h2>
            </div>
          ))}
        </div>

        <div className="analytics-charts">
          <div className="analytics-chart-card">
            <h2>Priority Score Distribution</h2>

            <div className="analytics-chart">
              {scoreData.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={scoreData}>
                    <CartesianGrid
                      strokeDasharray="3 3"
                      vertical={false}
                    />
                    <XAxis dataKey="name" />
                    <YAxis allowDecimals={false} />
                    <Tooltip />
                    <Bar
                      dataKey="count"
                      name="Schools"
                      radius={[6, 6, 0, 0]}
                    >
                      {scoreData.map((item) => (
                        <Cell
                          key={item.name}
                          fill={item.color}
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <p>No priority scores available.</p>
              )}
            </div>
          </div>

          <div className="analytics-chart-card">
            <h2>Assessment Coverage</h2>

            <div className="analytics-chart">
              {totalSchools > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={assessmentData}
                      dataKey="count"
                      nameKey="name"
                      cx="50%"
                      cy="45%"
                      outerRadius={100}
                    >
                      {assessmentData.map((item) => (
                        <Cell
                          key={item.name}
                          fill={item.color}
                        />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <p>No schools loaded.</p>
              )}
            </div>
          </div>

          <div className="analytics-chart-card">
            <h2>Issue Status Distribution</h2>

            <div className="analytics-chart">
              {issueStatusData.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={issueStatusData}>
                    <CartesianGrid
                      strokeDasharray="3 3"
                      vertical={false}
                    />
                    <XAxis dataKey="name" />
                    <YAxis allowDecimals={false} />
                    <Tooltip />
                    <Bar
                      dataKey="count"
                      name="Issues"
                      radius={[6, 6, 0, 0]}
                    >
                      {issueStatusData.map((item) => (
                        <Cell
                          key={item.name}
                          fill={item.color}
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <p>No issue records returned by the backend.</p>
              )}
            </div>
          </div>
        </div>

        <p>
          Data coverage: these statistics include only schools
          currently loaded from the backend. They are not
          statewide totals.
        </p>
      </div>
    )
  }

  // Preserve the original demo analytics.
  const priorityData = [
    'High',
    'Medium',
    'Low',
    'Not Assessed',
  ].map((priority) => ({
    name: priority,
    count: schools.filter(
      (school) =>
        (school.priority ?? 'Not Assessed') === priority
    ).length,
    color: priorityColors[priority] ?? '#64748b',
  }))

  return (
    <div className="analytics-page">
      <div className="analytics-header">
        <h1>School Analytics</h1>
        <p>
          Overview of school inspection priorities.
          All values shown are demo data.
        </p>
      </div>

      <div className="analytics-summary">
        <div className="analytics-stat-card">
          <p>Total Schools</p>
          <h2>{totalSchools}</h2>
        </div>

        {priorityData.map((item) => (
          <div
            className="analytics-stat-card"
            key={item.name}
          >
            <p>{item.name}</p>
            <h2 style={{ color: item.color }}>
              {item.count}
            </h2>
          </div>
        ))}
      </div>

      <div className="analytics-charts">
        <div className="analytics-chart-card">
          <h2>Inspection Priority Distribution</h2>

          <div className="analytics-chart">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={priorityData}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                />
                <XAxis dataKey="name" />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar
                  dataKey="count"
                  name="Schools"
                  radius={[6, 6, 0, 0]}
                >
                  {priorityData.map((item) => (
                    <Cell
                      key={item.name}
                      fill={item.color}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="analytics-chart-card">
          <h2>Priority Breakdown</h2>

          <div className="analytics-chart">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={priorityData}
                  dataKey="count"
                  nameKey="name"
                  cx="50%"
                  cy="45%"
                  outerRadius={100}
                >
                  {priorityData.map((item) => (
                    <Cell
                      key={item.name}
                      fill={item.color}
                    />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Analytics
