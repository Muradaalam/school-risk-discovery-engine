
import './SchoolDetails.css'
import { demoEvidence } from '../data/demoEvidence'

function SchoolDetails({ school, onBack }) {
  if (!school) {
    return <p>No school selected.</p>
  }

  const isBackendSchool = Boolean(school.schoolName)

  const backendIssues =
    isBackendSchool && Array.isArray(school.issues)
      ? school.issues
      : []

  const backendInspections =
    isBackendSchool && Array.isArray(school.inspections)
      ? school.inspections
      : []

  const backendEvents =
    isBackendSchool && Array.isArray(school.events)
      ? school.events
      : []

  const backendSources =
    isBackendSchool && Array.isArray(school.sources)
      ? school.sources
      : []

  const backendSnapshots =
    isBackendSchool && Array.isArray(school.prioritySnapshots)
      ? school.prioritySnapshots
      : []

  const evidence = !isBackendSchool
    ? demoEvidence[school.udise] || []
    : []

  function formatDate(value) {
    if (!value) return 'Not available'

    const date = new Date(value)

    if (Number.isNaN(date.getTime())) {
      return String(value)
    }

    return date.toLocaleDateString('en-IN', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      timeZone: 'UTC',
    })
  }

  function safeSourceUrl(value) {
    if (typeof value !== 'string') return null

    try {
      const url = new URL(value)

      return ['http:', 'https:'].includes(url.protocol)
        ? url.href
        : null
    } catch {
      return null
    }
  }

  return (
    <div className="school-details-page">
      <button
        type="button"
        className="back-button"
        onClick={onBack}
      >
        ← Back to Schools
      </button>

      <div className="school-details-header">
        <div>
          <h1>
            {isBackendSchool
              ? school.schoolName
              : school.name}
          </h1>

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
              : `priority-${school.priority
                  .toLowerCase()
                  .replace(/\s+/g, '-')}`
          }`}
        >
          {isBackendSchool
            ? `Priority Score: ${
                backendSnapshots[0]?.priorityScore ??
                'Not available'
              }`
            : school.priority}
        </span>
      </div>

      {isBackendSchool && (
        <div className="school-evidence-section">
          <div className="evidence-heading">
            <h2>Priority Assessment</h2>
            <span className="demo-label">
              Backend Data
            </span>
          </div>

          {backendSnapshots.length > 0 ? (
            backendSnapshots.map((snapshot, index) => (
              <div
                className="evidence-content"
                key={snapshot.id ?? index}
              >
                <p>
                  Assessment Date:{' '}
                  {formatDate(snapshot.snapshotDate)}
                </p>

                <p>
                  Priority Score:{' '}
                  {snapshot.priorityScore ?? 'Not available'}
                </p>

                <p>
                  Active Issues:{' '}
                  {snapshot.activeIssues ?? 'Not available'}
                </p>

                <p>
                  Under Resolution:{' '}
                  {snapshot.underResolutionIssues ??
                    'Not available'}
                </p>

                <p>
                  Resolved Issues:{' '}
                  {snapshot.resolvedIssues ??
                    'Not available'}
                </p>
              </div>
            ))
          ) : (
            <p>
              No priority assessment records returned
              for this school.
            </p>
          )}
        </div>
      )}

      <div className="school-info-grid">
        <div className="school-info-card">
          <p>UDISE Code</p>
          <h3>
            {isBackendSchool
              ? school.udiseCode ?? 'Not available'
              : school.udise}
          </h3>
        </div>

        <div className="school-info-card">
          <p>District</p>
          <h3>{school.district ?? 'Not available'}</h3>
        </div>

        <div className="school-info-card">
          <p>Evidence Records</p>
          <h3>
            {isBackendSchool
              ? 'Not available'
              : school.evidenceCount}
          </h3>
        </div>
      </div>

      {isBackendSchool && (
        <div className="school-evidence-section">
          <div className="evidence-heading">
            <h2>Reported School Issues</h2>
            <span className="demo-label">
              Backend Data
            </span>
          </div>

          {backendIssues.length > 0 ? (
            <div className="evidence-timeline">
              {backendIssues.map((issue, index) => (
                <div
                  className="evidence-item"
                  key={issue.id ?? index}
                >
                  <div className="evidence-dot"></div>

                  <div className="evidence-content">
                    <span className="evidence-date">
                      {formatDate(issue.firstDetected)}
                    </span>

                    <h3>
                      {issue.issueType ?? 'School Issue'}
                    </h3>

                    <p>
                      {issue.issueTypeDescription ??
                        'No description available'}
                    </p>

                    <div className="evidence-source">
                      Status: {issue.status ?? 'Unknown'}
                    </div>

                    {issue.statusDescription && (
                      <p>{issue.statusDescription}</p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p>
              No issue records returned for this school.
            </p>
          )}
        </div>
      )}

      {isBackendSchool && (
        <div className="school-evidence-section">
          <div className="evidence-heading">
            <h2>Inspection History</h2>
            <span className="demo-label">
              Backend Data
            </span>
          </div>

          {backendInspections.length > 0 ? (
            <div className="evidence-timeline">
              {backendInspections.map(
                (inspection, index) => (
                  <div
                    className="evidence-item"
                    key={inspection.id ?? index}
                  >
                    <div className="evidence-dot"></div>

                    <div className="evidence-content">
                      <span className="evidence-date">
                        {formatDate(
                          inspection.inspectionDate
                        )}
                      </span>

                      <h3>
                        {inspection.inspectionType ??
                          'School Inspection'}
                      </h3>

                      <p>
                        {inspection.remarks ??
                          'No remarks available'}
                      </p>

                      <div className="evidence-source">
                        Inspector:{' '}
                        {inspection.inspectorName ??
                          'Not available'}
                      </div>
                    </div>
                  </div>
                )
              )}
            </div>
          ) : (
            <p>
              No inspection records returned for this school.
            </p>
          )}
        </div>
      )}

      {isBackendSchool && (
        <div className="school-evidence-section">
          <div className="evidence-heading">
            <h2>Supporting Sources</h2>
            <span className="demo-label">
              Backend Data
            </span>
          </div>

          {backendSources.length > 0 ? (
            <div className="evidence-timeline">
              {backendSources.map((source, index) => {
                const sourceUrl = safeSourceUrl(
                  source.sourceUrl
                )

                return (
                  <div
                    className="evidence-item"
                    key={source.id ?? index}
                  >
                    <div className="evidence-dot"></div>

                    <div className="evidence-content">
                      <span className="evidence-date">
                        {formatDate(
                          source.publicationDate
                        )}
                      </span>

                      <h3>
                        {source.sourceName ??
                          'Unnamed Source'}
                      </h3>

                      {sourceUrl ? (
                        <a
                          href={sourceUrl}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          View Original Source
                        </a>
                      ) : (
                        <p>
                          Source URL not available.
                        </p>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>
          ) : (
            <p>
              No supporting sources returned for this school.
            </p>
          )}
        </div>
      )}

      {isBackendSchool && (
        <div className="school-evidence-section">
          <div className="evidence-heading">
            <h2>School Events</h2>
            <span className="demo-label">
              Backend Data
            </span>
          </div>

          <p>
            {backendEvents.length > 0
              ? `${backendEvents.length} event record(s) returned by the backend.`
              : 'No event records returned for this school.'}
          </p>
        </div>
      )}

      <div className="school-evidence-section">
        <div className="evidence-heading">
          <h2>Evidence Timeline</h2>

          <span className="demo-label">
            {isBackendSchool
              ? 'Backend Data'
              : 'Demo Data'}
          </span>
        </div>

        {evidence.length > 0 ? (
          <div className="evidence-timeline">
            {evidence.map((item) => (
              <div
                className="evidence-item"
                key={item.id}
              >
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
              ? 'Evidence documents are not yet connected for this school. The reported issues, inspections, and sources above are backend records, not independently verified evidence documents.'
              : 'No demonstration evidence records are available for this school. Its inspection priority should not be inferred from missing evidence.'}
          </p>
        )}
      </div>
    </div>
  )
}

export default SchoolDetails
