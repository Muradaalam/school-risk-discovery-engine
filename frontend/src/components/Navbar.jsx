
function Navbar() {
  return (
    <header className="top-navbar">
      <div className="navbar-search">
        <span>⌕</span>
        <input
          type="text"
          placeholder="Search schools, districts, or UDISE code..."
          aria-label="Search schools"
          disabled
        />
      </div>

      <div className="navbar-actions">
        <span className="user-avatar">S</span>
        <span className="user-name">Shahjad</span>
      </div>
    </header>
  )
}

export default Navbar
