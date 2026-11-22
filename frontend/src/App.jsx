
import { useState } from 'react'
import Sidebar from './components/Sidebar'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Schools from './pages/Schools'
import SchoolDetails from './pages/SchoolDetails'
import './App.css'
import Map from './pages/Map'
import Analytics from './pages/Analytics'
// import Loading from './components/Loading'
// import ErrorMessage from './components/ErrorMessage'
import BackendSchoolTest from './pages/BackendSchoolTest'
import { getKnownSchools } from './services/api'

function App() {
  const [activePage, setActivePage] = useState('Dashboard')
  const [selectedSchool, setSelectedSchool] = useState(null)
  const [realSchools, setRealSchools] = useState(null)
  const [schoolsLoading, setSchoolsLoading] = useState(false)
  const [schoolsError, setSchoolsError] = useState('')
  const [schoolToken, setSchoolToken] = useState('')
  async function loadRealSchools(token) {
  setSchoolsLoading(true)
  setSchoolsError('')

  try {
    const schools = await getKnownSchools(token)
    setRealSchools(schools)
  } catch (error) {
    setSchoolsError(error.message)
  } finally {
    setSchoolsLoading(false)
  }
}

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
      case 'BackendSchoolTest':
  return <BackendSchoolTest />
      case 'Schools':
  return (
    <Schools
      schools={realSchools ?? undefined}
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
  return <Map schools={realSchools ?? undefined} />
      
case 'Analytics':
  return <Analytics schools={realSchools ?? undefined} />
      case 'Dashboard':
default:
  return <Dashboard schools={realSchools ?? undefined} />
      
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
  <form
    onSubmit={(event) => {
      event.preventDefault()
      loadRealSchools(schoolToken.trim())
    }}
    style={{
      display: 'flex',
      gap: '10px',
      alignItems: 'center',
      flexWrap: 'wrap',
      marginBottom: '20px',
    }}
  >
    <input
      type="password"
      placeholder="Enter fresh backend JWT"
      value={schoolToken}
      onChange={(event) => setSchoolToken(event.target.value)}
      autoComplete="off"
      required
      style={{ padding: '10px', minWidth: '250px' }}
    />

    <button type="submit" disabled={schoolsLoading}>
      {schoolsLoading ? 'Loading...' : 'Load Real Schools'}
    </button>

    {realSchools && <span>Loaded {realSchools.length} real schools</span>}
    {schoolsError && <p role="alert">{schoolsError}</p>}
  </form>

  {renderPage()}
</main>
      </div>
    </div>
  )
}

export default App
