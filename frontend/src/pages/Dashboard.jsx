
import {
  School,
  TriangleAlert,
  CircleAlert,
  CircleCheck,
} from 'lucide-react'

import './Dashboard.css'
import { demoSchools } from '../data/demoSchools'

const stats = [
  {
    title: 'Total Schools',
    value: demoSchools.length,
    description: 'Schools in the database',
    icon: School,
    color: 'blue',
  },
  {
    title: 'High Priority',
    value: demoSchools.filter((school) => school.priority === 'High').length,
    description: 'Priority for inspection',
    icon: TriangleAlert,
    color: 'red',
  },
  {
    title: 'Medium Priority',
    value: demoSchools.filter((school) => school.priority === 'Medium').length,
    description: 'Priority for inspection',
    icon: CircleAlert,
    color: 'orange',
  },
  {
    title: 'Low Priority',
    value: 	demoSchools.filter((school) => school.priority === 'Low').length,
    description: 'Priority for inspection',
    icon: CircleCheck,
    color: 'green',
  },
]

function Dashboard() {
  return (
    <div className="dashboard">
      <div className="dashboard-heading">
        <h1>Dashboard Overview</h1>
        <p>School Evidence & Inspection Priority System</p>
        <p className="dashboard-demo-note">
          Statistics are based on demonstration data.
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

              <h2 className="stat-value">{stat.value}</h2>

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
