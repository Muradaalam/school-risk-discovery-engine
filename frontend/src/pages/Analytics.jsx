
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


const priorityData = [
  'High',
  'Medium',
  'Low',
  'Not Assessed',
].map((priority) => ({
  name: priority,
  count: demoSchools.filter(
    (school) => school.priority === priority
  ).length,
  color: priorityColors[priority],
}))

function Analytics() {
  const totalSchools = priorityData.reduce(
    (total, item) => total + item.count,
    0
  )

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
