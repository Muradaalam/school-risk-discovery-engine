
import './SchoolDetails.css'
import { demoEvidence } from '../data/demoEvidence'

function getPriorityDetails(score) {
  if (score === null || score === undefined || score === '') {
    return { label: 'Not Assessed', className: 'priority-not-assessed' }
  }

  const levels = {
    0: { label: 'No Priority', className: 'priority-low' },
    1: { label: 'Low Priority', className: 'priority-low' },
    2: { label: 'Medium Priority', className: 'priority-medium' },
    3: { label: 'High Priority', className: 'priority-high' },
  }

  return levels[String(score)] ?? {
    label: `Score ${score}`,
    className: 'priority-not-assessed',
  }
}

function formatPriority(score) {
  const level = getPriorityDetails(score)
  return score == null
    ? level.label
    : `${level.label} (Score ${score})`
}

function formatDate(value) {
  if (!value) return 'Not available'

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return String(value)

  return date.toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    timeZone: 'UTC',
  })
}

function safeUrl(value) {
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

function DocumentList({ documents, emptyMessage }) {
  if (!Array.isArray(documents) || documents.length === 0) {
    return <p>{emptyMessage}</p>
  }

  return (
    <div className="evidence-timeline">
      {documents.map((document, index) => {
        const sourceUrl = safeUrl(document.source?.sourceUrl)

        return (
          <div
            className="evidence-item"
            key={document.id ?? index}
          >
            <div className="evidence-dot"></div>

            <div className="evidence-content">
              <span className="evidence-date">
                {formatDate(document.source?.publicationDate)}
              </span>

              <h3>
                {document.documentName ?? 'Unnamed Document'}
              </h3>

              <p>
                {document.description ?? 'No description available'}
              </p>

              <p>
                Category: {document.objectCategory ?? 'Not available'}
              </p>

              <div className="evidence-source">
                Source: {document.source?.sourceName ?? 'Not available'}
              </div>

              {document.docPath && (
                <p>Stored document path: {document.docPath}</p>
              )}

              {sourceUrl && (
                <a
                  href={sourceUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  View Source Website
                </a>
              )}

              <p>
                Document download is not yet connected.
              </p>
            </div>
          </div>
        )
      })}
    </div>
  )
}


function buildSchoolTimeline(school) {
  const entries = []

  const snapshots = Array.isArray(school.prioritySnapshots)
    ? school.prioritySnapshots
    : []

  const inspections = Array.isArray(school.inspections)
    ? school.inspections
    : []

  const issues = Array.isArray(school.issues)
    ? school.issues
    : []

  const events = Array.isArray(school.events)
    ? school.events
    : []

  snapshots.forEach((snapshot, index) => {
    entries.push({
      id: `assessment-${snapshot.id ?? index}`,
      type: 'Priority Assessment',
      title: 'Priority Score Recorded',
      date: snapshot.snapshotDate,
      description: `Priority: ${formatPriority(snapshot.priorityScore)}`,
      details: `Active: ${
        snapshot.activeIssues ?? 'N/A'
      } | Under Resolution: ${
        snapshot.underResolutionIssues ?? 'N/A'
      } | Resolved: ${
        snapshot.resolvedIssues ?? 'N/A'
      }`,
    })
  })

  inspections.forEach((inspection, index) => {
    entries.push({
      id: `inspection-${inspection.id ?? index}`,
      type: 'Inspection',
      title: inspection.inspectionType ?? 'School Inspection',
      date: inspection.inspectionDate,
      description: inspection.remarks ?? 'No remarks available',
      details: `Inspector: ${
        inspection.inspectorName ?? 'Not available'
      }`,
    })
  })

  issues.forEach((issue, index) => {
    entries.push({
      id: `issue-${issue.id ?? index}`,
      type: 'Issue Reported',
      title: issue.issueType ?? 'School Issue',
      date: issue.firstDetected,
      description:
        issue.issueTypeDescription ??
        'No description available',
      details: `Current Status: ${issue.status ?? 'Unknown'}`,
    })
  })

  events.forEach((event, index) => {
    entries.push({
      id: `event-${event.id ?? index}`,
      type: 'School Event',
      title: event.eventType ?? 'School Event',
      date: event.eventDate,
      description:
        event.detailedDescription ??
        'No description available',
      details: `Location: ${event.location ?? 'Not available'}`,
    })
  })

  return entries.sort((a, b) => {
    const aTime = a.date
      ? new Date(a.date).getTime()
      : 0

    const bTime = b.date
      ? new Date(b.date).getTime()
      : 0

    const validA = Number.isFinite(aTime) ? aTime : 0
    const validB = Number.isFinite(bTime) ? bTime : 0

    return validB - validA
  })
}


function SchoolDetails({ school, onBack }) {
  if (!school) {
    return <p>No school selected.</p>
  }

  const isBackendSchool = Boolean(school.schoolName)

  const issues = isBackendSchool && Array.isArray(school.issues)
    ? school.issues
    : []

  const inspections =
    isBackendSchool && Array.isArray(school.inspections)
      ? school.inspections
      : []

  const sources = isBackendSchool && Array.isArray(school.sources)
    ? school.sources
    : []

  const events = isBackendSchool && Array.isArray(school.events)
    ? school.events
    : []

  const snapshots =
    isBackendSchool && Array.isArray(school.prioritySnapshots)
      ? school.prioritySnapshots
      : []

  const schoolDocuments =
    isBackendSchool && Array.isArray(school.schoolDocuments)
      ? school.schoolDocuments
      : []

  const evidence = !isBackendSchool
    ? demoEvidence[school.udise] || []
    : []

  const latestSnapshot = [...snapshots].sort(
    (a, b) =>
      new Date(b.snapshotDate ?? 0) -
      new Date(a.snapshotDate ?? 0)
  )[0]
  const activityTimeline = isBackendSchool
    ? buildSchoolTimeline(school)
    : []

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
            {isBackendSchool ? school.schoolName : school.name}
          </h1>

          <p>
            School Information — {isBackendSchool ? 'Backend Data' : 'Demo Data'}
          </p>
        </div>

        <span
          className={`priority-badge ${
            isBackendSchool
              ? getPriorityDetails(latestSnapshot?.priorityScore).className
              : `priority-${school.priority.toLowerCase().replace(/\s+/g, '-')}`
          }`}
        >
          {isBackendSchool
            ? formatPriority(latestSnapshot?.priorityScore)
            : school.priority}
        </span>
      </div>

      {isBackendSchool && (
        <div className="school-evidence-section">
          <div className="evidence-heading">
            <h2>Priority Assessment</h2>
            <span className="demo-label">Backend Data</span>
          </div>

          {snapshots.length > 0 ? (
            snapshots.map((snapshot, index) => (
              <div
                className="evidence-content"
                key={snapshot.id ?? index}
              >
                <p>
                  Assessment Date: {formatDate(snapshot.snapshotDate)}
                </p>
                <p>
                  Priority Level: {formatPriority(snapshot.priorityScore)}
                </p>
                <p>
                  Active Issues: {snapshot.activeIssues ?? 'Not available'}
                </p>
                <p>
                  Under Resolution: {snapshot.underResolutionIssues ?? 'Not available'}
                </p>
                <p>
                  Resolved Issues: {snapshot.resolvedIssues ?? 'Not available'}
                </p>
              </div>
            ))
          ) : (
            <p>No priority assessment records returned for this school.</p>
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
          <p>School Documents</p>
          <h3>
            {isBackendSchool
              ? schoolDocuments.length
              : 'Demo data'}
          </h3>
        </div>
      </div>

      {isBackendSchool && (
        <div className="school-evidence-section">
          <div className="evidence-heading">
            <h2>School Documents</h2>
            <span className="demo-label">Backend Data</span>
          </div>

          <DocumentList
            documents={schoolDocuments}
            emptyMessage="No school documents returned by the backend."
          />
        </div>
      )}

      {isBackendSchool && (
        <div className="school-evidence-section">
          <div className="evidence-heading">
            <h2>Reported School Issues</h2>
            <span className="demo-label">Backend Data</span>
          </div>

          {issues.length > 0 ? (
            <div className="evidence-timeline">
              {issues.map((issue, index) => (
                <div
                  className="evidence-item"
                  key={issue.id ?? index}
                >
                  <div className="evidence-dot"></div>

                  <div className="evidence-content">
                    <span className="evidence-date">
                      {formatDate(issue.firstDetected)}
                    </span>

                    <h3>{issue.issueType ?? 'School Issue'}</h3>

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

                    <h3>Issue Documents</h3>

                    <DocumentList
                      documents={issue.issueDocuments}
                      emptyMessage="No documents attached to this issue."
                    />
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

          {inspections.length > 0 ? (
            <div className="evidence-timeline">
              {inspections.map((inspection, index) => (
                <div
                  className="evidence-item"
                  key={inspection.id ?? index}
                >
                  <div className="evidence-dot"></div>

                  <div className="evidence-content">
                    <span className="evidence-date">
                      {formatDate(inspection.inspectionDate)}
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

      {isBackendSchool && (
        <div className="school-evidence-section">
          <div className="evidence-heading">
            <h2>Supporting Sources</h2>
            <span className="demo-label">Backend Data</span>
          </div>

          {sources.length > 0 ? (
            <div className="evidence-timeline">
              {sources.map((source, index) => {
                const url = safeUrl(source.sourceUrl)

                return (
                  <div
                    className="evidence-item"
                    key={source.id ?? index}
                  >
                    <div className="evidence-dot"></div>

                    <div className="evidence-content">
                      <span className="evidence-date">
                        {formatDate(source.publicationDate)}
                      </span>

                      <h3>
                        {source.sourceName ?? 'Unnamed Source'}
                      </h3>

                      {url ? (
                        <a
                          href={url}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          View Original Source
                        </a>
                      ) : (
                        <p>Source URL not available.</p>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>
          ) : (
            <p>No supporting sources returned for this school.</p>
          )}
        </div>
      )}

      {isBackendSchool && (
        <div className="school-evidence-section">
          <div className="evidence-heading">
            <h2>School Events</h2>
            <span className="demo-label">Backend Data</span>
          </div>

          {events.length > 0 ? (
            <div className="evidence-timeline">
              {events.map((event, index) => (
                <div
                  className="evidence-item"
                  key={event.id ?? index}
                >
                  <div className="evidence-dot"></div>

                  <div className="evidence-content">
                    <span className="evidence-date">
                      {formatDate(event.eventDate)}
                    </span>

                    <h3>{event.eventType ?? 'School Event'}</h3>

                    <p>
                      {event.detailedDescription ??
                        'No description available'}
                    </p>

                    <div className="evidence-source">
                      Location: {event.location ?? 'Not available'}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p>No event records returned for this school.</p>
          )}
        </div>
      )}

      
<div className="school-evidence-section">
  <div className="evidence-heading">
    <h2>School Activity Timeline</h2>

    <span className="demo-label">
      {isBackendSchool ? 'Backend Data' : 'Demo Data'}
    </span>
  </div>

  {isBackendSchool ? (
    activityTimeline.length > 0 ? (
      <div className="evidence-timeline">
        {activityTimeline.map((item) => (
          <div className="evidence-item" key={item.id}>
            <div className="evidence-dot"></div>

            <div className="evidence-content">
              <span className="evidence-date">
                {formatDate(item.date)}
              </span>

              <h3>{item.title}</h3>

              <span className="evidence-type">
                {item.type}
              </span>

              <p>{item.description}</p>

              <div className="evidence-source">
                {item.details}
              </div>
            </div>
          </div>
        ))}
      </div>
    ) : (
      <p>
        No dated activity or assessment records
        are available for this school.
      </p>
    )
  ) : evidence.length > 0 ? (
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
    <p>No demonstration evidence available.</p>
  )}
</div>

    </div>
  )
}

export default SchoolDetails
