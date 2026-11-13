
// Using GPT to make this page
import './SchoolDetails.css'
import { demoEvidence } from '../data/demoEvidence'


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
