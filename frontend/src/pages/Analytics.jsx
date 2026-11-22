
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

  return [...snapshots].sort((a, b) => {
    const dateDifference =
      new Date(b.snapshotDate ?? 0) -
      new Date(a.snapshotDate ?? 0)

    return dateDifference || (b.id ?? 0) - (a.id ?? 0)
  })[0] ?? null
}

function countBy(items, getKey) {
  const counts = new Map()

  items.forEach((item) => {
    const key = getKey(item) || 'UNKNOWN'

    counts.set(key, (counts.get(key) ?? 0) + 1)
  })

  return [...counts.entries()]
    .sort((a, b) => a[0].localeCompare(b[0]))
    .map(([name, count], index) => ({
      name: name.replaceAll('_', ' '),
      count,
      color: chartColors[index % chartColors.length],
    }))
}

function Analytics({ schools = demoSchools }) {
  const isBackendData = schools !== demoSchools
  const totalSchools = schools.length

  if (isBackendData) {
    const snapshots = schools.map(getLatestSnapshot)

    const assessedSchools = snapshots.filter(
      (snapshot) =>
        snapshot?.priorityScore !== null &&
        snapshot?.priorityScore !== undefined
    ).length

    const issues = schools.flatMap((school) =>
      Array.isArray(school.issues) ? school.issues : []
    )

    const activeIssues = issues.filter(
      (issue) => issue.status === 'ACTIVE'
    ).length

    const totalIssues = issues.length

    const scoreCounts = new Map()

    snapshots.forEach((snapshot) => {
      if (
        snapshot?.priorityScore !== null &&
        snapshot?.priorityScore !== undefined
      ) {
        const score = String(snapshot.priorityScore)

        scoreCounts.set(
          score,
          (scoreCounts.get(score) ?? 0) + 1
        )
      }
    })

    const scoreData = [...scoreCounts.entries()]
      .sort((a, b) => Number(b[0]) - Number(a[0]))
      .map(([score, count], index) => ({
        name: `Score ${score}`,
        count,
        color: chartColors[index % chartColors.length],
      }))

    const issueTypeData = countBy(
      issues,
      (issue) => issue.issueType
    )

    const issueStatusData = countBy(
      issues,
      (issue) => issue.status
    )

    const summaryItems = [
      {
        name: 'Top Schools Loaded',
        value: totalSchools,
      },
      {
        name: 'Assessed Schools',
        value: assessedSchools,
      },
      {
        name: 'Active Issues',
        value: activeIssues,
      },
      {
        name: 'Total Reported Issues',
        value: totalIssues,
      },
    ]

    return (
      <div className="analytics-page">
        <div className="analytics-header">
          <h1>Top Priority School Analytics</h1>

          <p>
            Live analytics from {totalSchools} school records
            returned by the Top 50 priority-ranked schools API.
            Only schools with priority assessments are eligible.
            Numeric scores are shown as recorded, without an
            assumed High/Medium/Low mapping.
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
                <ResponsiveContainer
                  width="100%"
                  height="100%"
                >
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
            <h2>Issue Type Breakdown</h2>

            <div className="analytics-chart">
              {issueTypeData.length > 0 ? (
                <ResponsiveContainer
                  width="100%"
                  height="100%"
                >
                  <PieChart>
                    <Pie
                      data={issueTypeData}
                      dataKey="count"
                      nameKey="name"
                      cx="50%"
                      cy="45%"
                      outerRadius={100}
                    >
                      {issueTypeData.map((item) => (
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
                <p>No issue records available.</p>
              )}
            </div>
          </div>

          <div className="analytics-chart-card">
            <h2>Issue Status Distribution</h2>

            <div className="analytics-chart">
              {issueStatusData.length > 0 ? (
                <ResponsiveContainer
                  width="100%"
                  height="100%"
                >
                  <BarChart data={issueStatusData}>
                    <CartesianGrid
                      strokeDasharray="3 3"
                      vertical={false}
                    />

                    <XAxis
                      dataKey="name"
                      interval={0}
                    />

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
                <p>No issue status data available.</p>
              )}
            </div>
          </div>
        </div>

        <p>
          Data coverage: statistics describe only the
          priority-ranked schools returned by the backend.
          Schools without assessments are excluded, and
          these figures are not statewide totals.
        </p>
      </div>
    )
  }

  // Original demo analytics remains unchanged.
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
            <ResponsiveContainer
              width="100%"
              height="100%"
            >
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
            <ResponsiveContainer
              width="100%"
              height="100%"
            >
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
