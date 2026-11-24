
import { useEffect, useState } from 'react'

import Sidebar from './components/Sidebar'
import Navbar from './components/Navbar'

import Dashboard from './pages/Dashboard'
import Schools from './pages/Schools'
import SchoolDetails from './pages/SchoolDetails'
import Map from './pages/Map'
import Analytics from './pages/Analytics'

import { getTop50Schools } from './services/api'

import './App.css'

function App() {
  const [activePage, setActivePage] = useState('Dashboard')
  const [selectedSchool, setSelectedSchool] = useState(null)

  const [realSchools, setRealSchools] = useState([])
  const [schoolsLoading, setSchoolsLoading] = useState(true)
  const [schoolsError, setSchoolsError] = useState('')

  useEffect(() => {
    let cancelled = false

    async function loadSchools() {
      setSchoolsLoading(true)
      setSchoolsError('')

      try {
        const schools = await getTop50Schools()

        if (!cancelled) {
          setRealSchools(schools)
        }
      } catch (error) {
        if (!cancelled) {
          setSchoolsError(error.message)
        }
      } finally {
        if (!cancelled) {
          setSchoolsLoading(false)
        }
      }
    }

    loadSchools()

    return () => {
      cancelled = true
    }
  }, [])

  function handlePageChange(page) {
    setActivePage(page)
    setSelectedSchool(null)
  }

  function handleSchoolSelect(school) {
    setSelectedSchool(school)
    setActivePage('SchoolDetails')
  }

  function handleBackToSchools() {
    setSelectedSchool(null)
    setActivePage('Schools')
  }

  function renderPage() {
    switch (activePage) {
      case 'Schools':
        return (
          <Schools
            schools={realSchools}
            onSchoolSelect={handleSchoolSelect}
          />
        )

      case 'SchoolDetails':
        return (
          <SchoolDetails
            school={selectedSchool}
            onBack={handleBackToSchools}
          />
        )

      case 'Map':
        return <Map schools={realSchools} />

      case 'Analytics':
        return <Analytics schools={realSchools} />

      case 'Dashboard':
      default:
        return (
  <Dashboard
    schools={realSchools}
    onSchoolSelect={handleSchoolSelect}
  />
)
    }
  }

  return (
    <div className="app-layout">
      <Sidebar
        activePage={
          activePage === 'SchoolDetails'
            ? 'Schools'
            : activePage
        }
        onPageChange={handlePageChange}
      />

      <div className="main-area">
        <Navbar />

        <main className="main-content">
          {schoolsLoading ? (
            <div
              role="status"
              style={{
                padding: '24px',
                textAlign: 'center',
              }}
            >
              <h2>Loading school data...</h2>
              <p>
                Fetching the latest priority-ranked
                schools from the backend.
              </p>
            </div>
          ) : schoolsError ? (
            <div
              role="alert"
              style={{
                padding: '24px',
                borderRadius: '12px',
                backgroundColor: '#fef2f2',
                color: '#991b1b',
              }}
            >
              <h2>Unable to load school data</h2>

              <p>{schoolsError}</p>

              <p>
                Please check that the Spring Boot backend
                is running on port 8080, then refresh
                the page.
              </p>
            </div>
          ) : (
            renderPage()
          )}
        </main>
      </div>
    </div>
  )
}

export default App
