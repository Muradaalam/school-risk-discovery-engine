import './Navbar.css'

import { Search, Bell, ChevronDown } from 'lucide-react'

function Navbar() {
  return (
    <header className="top-navbar">

      {/* Left: Search bar */}
      <div className="navbar-search">
        <Search size={18} className="search-icon" />

        <input
          type="text"
          placeholder="Search schools, districts, or UDISE code..."
          aria-label="Search schools"
          disabled
        />
      </div>

      {/* Right: Notifications and profile */}
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
