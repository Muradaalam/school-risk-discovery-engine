
const menuItems = [
  { name: 'Dashboard', icon: '▦' },
  { name: 'Schools', icon: '▤' },
  { name: 'Map', icon: '⌖' },
  { name: 'Analytics', icon: '▥' },
]

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <span className="brand-icon">🏫</span>
        <span>School Risk<br />Discovery Engine</span>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item, index) => (
          <div
            key={item.name}
            className={`sidebar-link ${index === 0 ? 'active' : ''}`}
          >
            <span className="menu-icon">{item.icon}</span>
            <span>{item.name}</span>
          </div>
        ))}
      </nav>

      <div className="sidebar-footer">
        School Risk Discovery Engine
      </div>
    </aside>
  )
}

export default Sidebar
