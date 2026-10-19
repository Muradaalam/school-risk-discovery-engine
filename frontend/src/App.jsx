
import { useState } from 'react'
import Sidebar from './components/Sidebar'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Schools from './pages/Schools'
import './App.css'

function App() {
  const [activePage, setActivePage] = useState('Dashboard')

  function renderPage() {
    switch (activePage) {
      case 'Schools':
        return <Schools />
      case 'Dashboard':
      default:
        return <Dashboard />
    }
  }

  return (
    <div className="app-layout">
      <Sidebar
        activePage={activePage}
        onPageChange={setActivePage}
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
