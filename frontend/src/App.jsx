
import Sidebar from './components/Sidebar'
import Navbar from './components/Navbar'
import './App.css'

function App() {
  return (
    <div className="app-layout">
      <Sidebar />

      <div className="main-area">
        <Navbar />

        <main className="main-content">
          <h1>Dashboard</h1>
          <p>School Evidence & Inspection Priority System</p>
        </main>
      </div>
    </div>
  )
}

export default App
