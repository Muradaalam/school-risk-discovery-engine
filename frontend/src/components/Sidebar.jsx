import './Sidebar.css'

const menuItems = [
  { name: 'Dashboard', icon: '/dashboard.png' },
  { name: 'Schools', icon: '/schoo.png' },
  { name: 'Map', icon: '/map.png' },
  { name: 'Analytics', icon: '/analytics.png' },
]

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <img
           src="/school.png"
           alt="School Risk Discovery Engine"
           className="brand-logo"
        />
        <span>School Risk<br />Discovery Engine</span>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item, index) => (
          <div
            key={item.name}
            className={`sidebar-link ${index === 0 ? 'active' : ''}`}
          >
            {item.icon.startsWith('/') ? (
      <img src={item.icon} alt="" className="menu-icon-img" />
      ) : (
        <span className="menu-icon">{item.icon}</span>
      )}
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
