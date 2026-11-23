
import './Navbar.css'
import { Bell, ChevronDown } from 'lucide-react'

function Navbar() {
  return (
    <header className="top-navbar">
      <div className="navbar-actions">
        <span className="notification-icon">
          <Bell size={20} />
        </span>

        <div className="user-profile">
          <div className="user-avatar">U</div>
          <span className="user-name">User</span>
          <ChevronDown size={16} />
        </div>
      </div>
    </header>
  )
}

export default Navbar
