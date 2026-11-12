
// Using GPT to make this page
import './SchoolDetails.css'


const demoEvidence = {
  'DEMO-001': [
    {
      id: 1,
      date: '2025-08-12',
      type: 'Inspection Finding',
      title: 'Classroom roof requires maintenance',
      description: 'Demo inspection record describing roof damage.',
      source: 'Demo inspection report',
    },
    {
      id: 2,
      date: '2025-04-20',
      type: 'Repair Record',
      title: 'Roof repair request recorded',
      description: 'Demo maintenance request for classroom repairs.',
      source: 'Demo repair record',
    },
  ],
  'DEMO-002': [
    {
      id: 3,
      date: '2025-06-15',
      type: 'Infrastructure Finding',
      title: 'Drinking water facility requires review',
      description: 'Demo record indicating a possible water facility issue.',
      source: 'Demo infrastructure report',
    },
  ],
  'DEMO-003': [
    {
      id: 4,
      date: '2025-02-10',
      type: 'Inspection Finding',
      title: 'Minor classroom maintenance noted',
      description: 'Demo record describing routine maintenance.',
      source: 'Demo inspection report',
    },
  ],
}


function SchoolDetails({ school, onBack }) {

    const evidence = school
  ? demoEvidence[school.udise] || []
  : []
  if (!school) {
    return <p>No school selected.</p>
  }

  return (
    <div className="school-details-page">
      <button
        className="back-button"
        onClick={onBack}
      >
        ← Back to Schools
      </button>

      <div className="school-details-header">
        <div>
          <h1>{school.name}</h1>
          <p>School Information — Demo Data</p>
        </div>

        <span
          className={`priority-badge ${school.priority
            .toLowerCase()
            .replace(/\s+/g, '-')}`}
        >
          {school.priority}
        </span>
      </div>

      <div className="school-info-grid">
        <div className="school-info-card">
          <p>UDISE Code</p>
          <h3>{school.udise}</h3>
        </div>

        <div className="school-info-card">
          <p>District</p>
          <h3>{school.district}</h3>
        </div>

        <div className="school-info-card">
          <p>Evidence Records</p>
          <h3>{school.evidenceCount}</h3>
        </div>
      </div>

      
<div className="school-evidence-section">
  <div className="evidence-heading">
    <h2>Evidence Timeline</h2>
    <span className="demo-label">Demo Data</span>
  </div>

  {evidence.length > 0 ? (
    <div className="evidence-timeline">
      {evidence.map((item) => (
        <div className="evidence-item" key={item.id}>
          <div className="evidence-dot"></div>

          <div className="evidence-content">
            <span className="evidence-date">
              {item.date}
            </span>

            <h3>{item.title}</h3>

            <span className="evidence-type">
              {item.type}
            </span>

            <p>{item.description}</p>

            <div className="evidence-source">
              Source: {item.source}
            </div>
          </div>
        </div>
      ))}
    </div>
  ) : (
    <p>
      No demonstration evidence records are available
      for this school. Its inspection priority should
      not be inferred from missing evidence.
    </p>
  )}
</div>

    </div>
  )
}

export default SchoolDetails
