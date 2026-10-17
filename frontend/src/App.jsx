
import Sidebar from './components/Sidebar'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import './App.css'

function App() {
  return (
    <div className="app-layout">
      <Sidebar />

      <div className="main-area">
        <Navbar />

        <main className="main-content">
          <Dashboard />
        </main>
      </div>
    </div>
  )
}

export default App
