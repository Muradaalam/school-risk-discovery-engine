
import { useState, useEffect } from 'react'
import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup,
  useMap,
} from 'react-leaflet'

import {
  demoSchools,
  priorityColors,
} from '../data/demoSchools'

import 'leaflet/dist/leaflet.css'
import './Map.css'

const scoreColors = [
  '#2563eb',
  '#10b981',
  '#f59e0b',
  '#8b5cf6',
  '#ef4444',
  '#64748b',
]

function getLatestSnapshot(school) {
  const snapshots = Array.isArray(school.prioritySnapshots)
    ? school.prioritySnapshots
    : []

  return [...snapshots].sort((a, b) => {
    const dateDifference =
      new Date(b.snapshotDate ?? 0) -
      new Date(a.snapshotDate ?? 0)

    return dateDifference || (b.id ?? 0) - (a.id ?? 0)
  })[0] ?? null
}

function getValidPosition(school, isBackendData) {
  // Demo schools may have pre-defined map positions.
  if (
    !isBackendData &&
    Array.isArray(school.position) &&
    school.position.length === 2
  ) {
    const lat = Number(school.position[0])
    const lng = Number(school.position[1])

    if (
      Number.isFinite(lat) &&
      Number.isFinite(lng) &&
      lat >= -90 &&
      lat <= 90 &&
      lng >= -180 &&
      lng <= 180
    ) {
      return [lat, lng]
    }
  }

  // Do not turn missing coordinates into [0, 0].
  if (
    school.latitude === null ||
    school.latitude === undefined ||
    school.latitude === '' ||
    school.longitude === null ||
    school.longitude === undefined ||
    school.longitude === ''
  ) {
    return null
  }

  const lat = Number(school.latitude)
  const lng = Number(school.longitude)

  if (
    !Number.isFinite(lat) ||
    !Number.isFinite(lng) ||
    lat < -90 ||
    lat > 90 ||
    lng < -180 ||
    lng > 180
  ) {
    return null
  }

  return [lat, lng]
}

function MapBoundsUpdater({ positions }) {
  const map = useMap()

  useEffect(() => {
    if (positions.length === 1) {
      map.setView(positions[0], 11)
    } else if (positions.length > 1) {
      map.fitBounds(positions, {
        padding: [35, 35],
        maxZoom: 11,
      })
    } else {
      map.setView([26.2, 74.5], 7)
    }
  }, [map, positions])

  return null
}

function Map({ schools = demoSchools }) {
  const isBackendData = schools !== demoSchools
  const [priorityFilter, setPriorityFilter] = useState('All')

  const scores = isBackendData
    ? [
        ...new Set(
          schools
            .map((school) =>
              getLatestSnapshot(school)?.priorityScore
            )
            .filter(
              (score) =>
                score !== null &&
                score !== undefined
            )
            .map(String)
        ),
      ].sort((a, b) => Number(b) - Number(a))
    : []

  const scoreColorMap = Object.fromEntries(
    scores.map((score, index) => [
      score,
      scoreColors[index % scoreColors.length],
    ])
  )

  const validFilters = isBackendData
    ? ['All', ...scores, 'Not Assessed']
    : [
        'All',
        'High',
        'Medium',
        'Low',
        'Not Assessed',
      ]

  const currentFilter = validFilters.includes(priorityFilter)
    ? priorityFilter
    : 'All'

  const preparedSchools = schools.map((school) => {
    const snapshot = isBackendData
      ? getLatestSnapshot(school)
      : null

    const priorityScore = snapshot?.priorityScore ?? null

    const position = getValidPosition(
      school,
      isBackendData
    )

    return {
      ...school,
      displayName:
        school.schoolName ??
        school.name ??
        'Unnamed School',
      position,
      priorityScore,
      markerColor: isBackendData
        ? (
            priorityScore !== null
              ? scoreColorMap[String(priorityScore)]
              : '#64748b'
          )
        : (
            priorityColors[school.priority] ??
            '#64748b'
          ),
    }
  })

  const schoolsWithCoordinates = preparedSchools.filter(
    (school) => school.position !== null
  )

  const missingCoordinates =
    preparedSchools.length - schoolsWithCoordinates.length

  const filteredSchools = schoolsWithCoordinates.filter(
    (school) => {
      if (currentFilter === 'All') {
        return true
      }

      if (isBackendData) {
        if (currentFilter === 'Not Assessed') {
          return school.priorityScore === null
        }

        return (
          String(school.priorityScore) === currentFilter
        )
      }

      return school.priority === currentFilter
    }
  )

  const positions = filteredSchools.map(
    (school) => school.position
  )

  return (
    <div className="map-page">
      <div className="map-page-header">
        <h1>
          {isBackendData
            ? 'Top Priority Schools Map'
            : 'Schools Map'}
        </h1>

        <p>
          {isBackendData
            ? 'Geographic locations of priority-ranked schools with valid backend coordinates.'
            : 'Explore demonstration school inspection priorities by location.'}
        </p>
      </div>

      <div className="map-card">
        <div className="map-card-header">
          <div>
            <h2>School Locations</h2>

            <span className="map-demo-label">
              {isBackendData
                ? 'Backend Data'
                : 'Demo Locations'}
            </span>
          </div>

          <select
            className="map-priority-filter"
            value={currentFilter}
            onChange={(event) =>
              setPriorityFilter(event.target.value)
            }
            aria-label={
              isBackendData
                ? 'Filter by priority score'
                : 'Filter by inspection priority'
            }
          >
            <option value="All">
              {isBackendData
                ? 'All Scores'
                : 'All Priorities'}
            </option>

            {isBackendData ? (
              <>
                {scores.map((score) => (
                  <option
                    key={score}
                    value={score}
                  >
                    Priority Score {score}
                  </option>
                ))}

                <option value="Not Assessed">
                  Not Assessed
                </option>
              </>
            ) : (
              <>
                <option value="High">
                  High Priority
                </option>

                <option value="Medium">
                  Medium Priority
                </option>

                <option value="Low">
                  Low Priority
                </option>

                <option value="Not Assessed">
                  Not Assessed
                </option>
              </>
            )}
          </select>
        </div>

        {isBackendData && (
          <div
            style={{
              padding: '14px',
              marginBottom: '16px',
              backgroundColor: '#f1f5f9',
              color: '#475569',
              borderRadius: '8px',
            }}
          >
            <strong>
              {schoolsWithCoordinates.length} of{' '}
              {schools.length} loaded schools
              have valid map coordinates.
            </strong>

            <p style={{ margin: '8px 0 0' }}>
              {missingCoordinates} schools are missing
              valid latitude or longitude values.
            </p>

            {schoolsWithCoordinates.length === 0 && (
              <p style={{ margin: '8px 0 0' }}>
                No real school markers can be shown yet.
                Coordinates must be provided by the
                backend before these schools can be
                accurately placed on the map.
              </p>
            )}

            <p style={{ margin: '8px 0 0' }}>
              This map covers only the Top 50
              assessed-school dataset, not every school
              in the database.
            </p>
          </div>
        )}

        <MapContainer
          center={[26.2, 74.5]}
          zoom={7}
          scrollWheelZoom={true}
          className="schools-map"
        >
          <TileLayer
            attribution="&copy; OpenStreetMap contributors"
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          <MapBoundsUpdater positions={positions} />

          {filteredSchools.map((school) => (
            <CircleMarker
              key={school.id}
              center={school.position}
              radius={10}
              pathOptions={{
                color: '#ffffff',
                weight: 2,
                fillColor: school.markerColor,
                fillOpacity: 0.9,
              }}
            >
              <Popup>
                <strong>{school.displayName}</strong>

                <p>
                  District:{' '}
                  {school.district ?? 'Not available'}
                </p>

                {isBackendData ? (
                  <>
                    <p>
                      Priority Score:{' '}
                      {school.priorityScore ??
                        'Not Assessed'}
                    </p>

                    <p>
                      Latitude: {school.position[0]}
                    </p>

                    <p>
                      Longitude: {school.position[1]}
                    </p>

                    <small>
                      Location from backend school data.
                    </small>
                  </>
                ) : (
                  <>
                    <p>
                      Inspection Priority:{' '}
                      {school.priority}
                    </p>

                    <small>
                      Demonstration location only.
                    </small>
                  </>
                )}
              </Popup>
            </CircleMarker>
          ))}
        </MapContainer>

        <div className="map-legend">
          {isBackendData ? (
            <>
              {scores.map((score) => (
                <span key={score}>
                  <i
                    className="legend-dot"
                    style={{
                      backgroundColor:
                        scoreColorMap[score],
                    }}
                  />
                  {' '}Score {score}
                </span>
              ))}

              <span>
                <i
                  className="legend-dot"
                  style={{
                    backgroundColor: '#64748b',
                  }}
                />
                {' '}Not Assessed
              </span>
            </>
          ) : (
            <>
              <span>
                <i className="legend-dot high" />
                {' '}High
              </span>

              <span>
                <i className="legend-dot medium" />
                {' '}Medium
              </span>

              <span>
                <i className="legend-dot low" />
                {' '}Low
              </span>

              <span>
                <i className="legend-dot not-assessed" />
                {' '}Not Assessed
              </span>
            </>
          )}
        </div>

        {isBackendData && (
          <p
            style={{
              marginTop: '12px',
              color: '#64748b',
              fontSize: '13px',
            }}
          >
            Displaying {filteredSchools.length} mapped
            schools after filtering. Marker colors
            distinguish recorded numeric scores;
            they do not represent official
            High/Medium/Low categories.
          </p>
        )}
      </div>
    </div>
  )
}

export default Map
