
// ADDED USING GPT
import { useState } from 'react'
import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup,
} from 'react-leaflet'

import 'leaflet/dist/leaflet.css'
import './Map.css'

const demoSchools = [
  {
    id: 1,
    name: 'Demo Government School A',
    district: 'Jaipur',
    position: [26.9124, 75.7873],
    priority: 'High',
  },
  {
    id: 2,
    name: 'Demo Government School B',
    district: 'Ajmer',
    position: [26.4499, 74.6399],
    priority: 'Medium',
  },
  {
    id: 3,
    name: 'Demo Government School C',
    district: 'Udaipur',
    position: [24.5854, 73.7125],
    priority: 'Low',
  },
  {
    id: 4,
    name: 'Demo Government School D',
    district: 'Jodhpur',
    position: [26.2389, 73.0243],
    priority: 'Not Assessed',
  },
]

const priorityColors = {
  High: '#dc2626',
  Medium: '#f59e0b',
  Low: '#16a34a',
  'Not Assessed': '#64748b',
}

function Map() {
  const [priorityFilter, setPriorityFilter] = useState('All')

  const filteredSchools = demoSchools.filter((school) => {
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
            Demo Locations
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
