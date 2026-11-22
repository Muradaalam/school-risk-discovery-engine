
// ADDED USING GPT
import { useState } from 'react'
import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup,
} from 'react-leaflet'

import {
  demoSchools,
  priorityColors,
} from '../data/demoSchools'

import 'leaflet/dist/leaflet.css'
import './Map.css'


function Map({ schools = demoSchools }) {
  const isBackendData = schools !== demoSchools
  const [priorityFilter, setPriorityFilter] = useState('All')

const filteredSchools = schools
  .filter((school) => {
    if (school.position) return true

    return (
      school.latitude != null &&
      school.longitude != null &&
      Number.isFinite(Number(school.latitude)) &&
      Number.isFinite(Number(school.longitude))
    )
  })
  .map((school) => ({
    ...school,
    position: school.position ?? [
      Number(school.latitude),
      Number(school.longitude),
    ],
  }))
  .filter((school) => {
    return (
      priorityFilter === 'All' ||
      school.priority === priorityFilter
    )
  })

  return (
    <div className="map-page">
      <div className="map-page-header">
        <h1>Schools Map</h1>
        <p>
          Explore school inspection priorities by location.
        </p>
      </div>

      <div className="map-card">

        <div className="map-card-header">
          <div>
          <h2>School Locations</h2>
<span className="map-demo-label">
  {isBackendData ? 'Backend Data' : 'Demo Locations'}
</span>
         </div>

         <select
           className="map-priority-filter"
            value={priorityFilter}
            onChange={(event) =>
              setPriorityFilter(event.target.value)
            }
            aria-label="Filter schools by inspection priority"
          >
           <option value="All">All Priorities</option>
           <option value="High">High Priority</option>
           <option value="Medium">Medium Priority</option>
           <option value="Low">Low Priority</option>
           <option value="Not Assessed">Not Assessed</option>
         </select>
        </div>

{isBackendData && filteredSchools.length === 0 && (
  <p style={{
    padding: '14px',
    color: '#64748b',
    backgroundColor: '#f1f5f9',
    borderRadius: '8px',
    marginBottom: '16px',
  }}>
    No school locations available. The backend records do not
    currently contain latitude and longitude coordinates.
  </p>
)}
        <MapContainer
          center={[26.2, 74.5]}
          zoom={7}
          scrollWheelZoom={true}
          className="schools-map"
        >
          <TileLayer
            attribution='&copy; OpenStreetMap contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {filteredSchools.map((school) => (
            <CircleMarker
              key={school.id}
              center={school.position}
              radius={10}
              pathOptions={{
                color: '#ffffff',
                weight: 2,
                fillColor: priorityColors[school.priority],
                fillOpacity: 0.9,
              }}
            >
              <Popup>
                <strong>{school.name}</strong>
                <p>District: {school.district}</p>
                <p>
                  Inspection Priority: {school.priority}
                </p>
                <small>
                  Demonstration location only.
                </small>
              </Popup>
            </CircleMarker>
          ))}
        </MapContainer>

        <div className="map-legend">
          <span>
            <i className="legend-dot high"></i> High
          </span>
          <span>
            <i className="legend-dot medium"></i> Medium
          </span>
          <span>
            <i className="legend-dot low"></i> Low
          </span>
          <span>
            <i className="legend-dot not-assessed"></i>
            Not Assessed
          </span>
        </div>
      </div>
    </div>
  )
}

export default Map
