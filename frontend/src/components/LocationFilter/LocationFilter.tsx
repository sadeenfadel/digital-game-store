import type { Location } from '../../models/product'

type FilterValue = Location | 'ALL'

interface LocationFilterProps {
  value: FilterValue
  onChange: (location: FilterValue) => void
}

export function LocationFilter({ value, onChange }: LocationFilterProps) {
  return (
    <div className="location-filter">
      <label className="filter-label">Location:</label>
      <div className="filter-buttons">
        <button
          className={`filter-btn ${value === 'ALL' ? 'active' : ''}`}
          onClick={() => onChange('ALL')}
        >
          All
        </button>
        <button
          className={`filter-btn ${value === 'JO' ? 'active' : ''}`}
          onClick={() => onChange('JO')}
        >
          JO
        </button>
        <button
          className={`filter-btn ${value === 'SA' ? 'active' : ''}`}
          onClick={() => onChange('SA')}
        >
          SA
        </button>
      </div>
    </div>
  )
}
