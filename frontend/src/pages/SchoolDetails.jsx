
// Using GPT to make this page
import './SchoolDetails.css'
import { demoEvidence } from '../data/demoEvidence'


function SchoolDetails({ school, onBack }) {

  const isBackendSchool = Boolean(school?.schoolName)
  const backendIssues = isBackendSchool && Array.isArray(school.issues)
  ? school.issues
  : []

const backendInspections = isBackendSchool && Array.isArray(school.inspections)
  ? school.inspections
  : []

const backendEvents = isBackendSchool && Array.isArray(school.events)
  ? school.events
  : []

const evidence =
  school && !isBackendSchool
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
          <h1>{isBackendSchool ? school.schoolName : school.name}</h1>
          <p>
            {isBackendSchool
              ? 'School Information — Backend Data'
              : 'School Information — Demo Data'}
          </p>
        </div>

        <span
          className={`priority-badge ${
            isBackendSchool
              ? 'priority-not-assessed'
              : school.priority.toLowerCase().replace(/\s+/g, '-')
          }`}
        >
          {isBackendSchool
            ? `Priority Score: ${
                school.prioritySnapshots?.[0]?.priorityScore ?? 'Not available'
              }`
            : school.priority}
        </span>
      </div>

      <div className="school-info-grid">
        <div className="school-info-card">
          <p>UDISE Code</p>
          <h3>{isBackendSchool ? school.udiseCode : school.udise}</h3>
        </div>

        <div className="school-info-card">
          <p>District</p>
          <h3>{school.district}</h3>
        </div>

        <div className="school-info-card">
          <p>Evidence Records</p>
          <h3>
  {isBackendSchool ? 'Not available' : school.evidenceCount}
</h3>
        </div>
      </div>

{isBackendSchool && (
  <div className="school-evidence-section">
    <div className="evidence-heading">
      <h2>Reported School Issues</h2>
      <span className="demo-label">Backend Data</span>
    </div>

    {backendIssues.length > 0 ? (
      <div className="evidence-timeline">
        {backendIssues.map((issue) => (
          <div className="evidence-item" key={issue.id}>
            <div className="evidence-dot"></div>

            <div className="evidence-content">
              <span className="evidence-date">
                {issue.firstDetected ?? 'Date unavailable'}
              </span>

              <h3>{issue.issueType ?? 'School Issue'}</h3>

              <p>
                {issue.issueTypeDescription ??
                  'No description available'}
              </p>

              <div className="evidence-source">
                Status: {issue.status ?? 'Unknown'}
              </div>
            </div>
          </div>
        ))}
      </div>
    ) : (
      <p>No issue records returned for this school.</p>
    )}
  </div>
)}

{isBackendSchool && (
  <div className="school-evidence-section">
    <div className="evidence-heading">
      <h2>Inspection History</h2>
      <span className="demo-label">Backend Data</span>
    </div>

    {backendInspections.length > 0 ? (
      <div className="evidence-timeline">
        {backendInspections.map((inspection) => (
          <div className="evidence-item" key={inspection.id}>
            <div className="evidence-dot"></div>

            <div className="evidence-content">
              <span className="evidence-date">
                {inspection.inspectionDate ?? 'Date unavailable'}
              </span>

              <h3>
                {inspection.inspectionType ?? 'School Inspection'}
              </h3>

              <p>
                {inspection.remarks ?? 'No remarks available'}
              </p>

              <div className="evidence-source">
                Inspector: {inspection.inspectorName ?? 'Not available'}
              </div>
            </div>
          </div>
        ))}
      </div>
    ) : (
      <p>No inspection records returned for this school.</p>
    )}
  </div>
)}
<div className="school-evidence-section">
  <div className="evidence-heading">
    <h2>Evidence Timeline</h2>
    <span className="demo-label">
  {isBackendSchool ? 'Backend Data' : 'Demo Data'}
</span>
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
      {isBackendSchool
        ? 'Evidence documents are not yet connected for this school. No conclusion about its inspection priority should be drawn from this.'
        : 'No demonstration evidence records are available for this school. Its inspection priority should not be inferred from missing evidence.'}
    </p>
  )}
</div>

    </div>
  )
}

export default SchoolDetails
