
import { useState } from 'react'
import Sidebar from './components/Sidebar'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Schools from './pages/Schools'
import SchoolDetails from './pages/SchoolDetails'
import './App.css'
import Map from './pages/Map'

function App() {
  const [activePage, setActivePage] = useState('Dashboard')
  const [selectedSchool, setSelectedSchool] = useState(null)

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
        return <Schools onSchoolSelect={handleSchoolSelect} />

      case 'SchoolDetails':
        return (
          <SchoolDetails
            school={selectedSchool}
            onBack={handleBackToSchools}
          />
        )
      case 'Map':
        return <Map />
      case 'Dashboard':
      default:
        return <Dashboard />
      
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
          {renderPage()}
        </main>
      </div>
    </div>
  )
}

export default App
