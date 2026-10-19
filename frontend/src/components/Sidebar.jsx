import './Sidebar.css'

const menuItems = [
  { name: 'Dashboard', icon: '/dashboard.png' },
  { name: 'Schools', icon: '/schoo.png' },
  { name: 'Map', icon: '/map.png' },
  { name: 'Analytics', icon: '/analytics.png' },
]

function Sidebar({ activePage, onPageChange }) {
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
          <button
               type="button"
               key={item.name}
               className={`sidebar-link ${activePage === item.name ? 'active' : ''}`}
               onClick={() => onPageChange(item.name)}
               disabled={!['Dashboard', 'Schools'].includes(item.name)}
          >
            {item.icon.startsWith('/') ? (
      <img src={item.icon} alt="" className="menu-icon-img" />
      ) : (
        <span className="menu-icon">{item.icon}</span>
      )}
        <span>{item.name}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        School Risk Discovery Engine
      </div>
    </aside>
  )
}

export default Sidebar
