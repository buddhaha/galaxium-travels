# Implementation Plan: Query Parameters for Flights Endpoint

## Overview
Add filtering, searching, and sorting capabilities to the `/flights` endpoint to enable efficient flight searches from the frontend.

## GitHub Issue Reference
- **Issue**: #2 - Add query parameters to /flights endpoint for filtering and search
- **Repository**: Maximilian-Jesch/galaxium-travels-booking-system

## Design Decisions
1. **Date filtering**: Date ranges (from/to) using ISO format strings
2. **Text matching**: Case-insensitive partial matching for origin/destination
3. **Seat availability**: Filter for flights with at least 1 seat available in specified class
4. **Default behavior**: Return all flights when no filters provided (no pagination)
5. **Sorting**: Support sorting by price, departure_time, or duration with asc/desc order

## Implementation Steps

### 1. Backend Schema Changes (`schemas.py`)

**Create `FlightQueryParams` class:**
```python
from typing import Optional, Literal

class FlightQueryParams(BaseModel):
    # Location filters (case-insensitive partial match)
    origin: Optional[str] = None
    destination: Optional[str] = None
    
    # Date range filters (ISO format: YYYY-MM-DD)
    departure_date_from: Optional[str] = None
    departure_date_to: Optional[str] = None
    
    # Price range filters
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    
    # Seat availability filters (at least 1 seat available)
    has_economy: Optional[bool] = None
    has_business: Optional[bool] = None
    has_galaxium: Optional[bool] = None
    
    # Sorting
    sort: Optional[Literal['price', 'departure_time', 'duration']] = None
    order: Optional[Literal['asc', 'desc']] = 'asc'
```

**Key Points:**
- All parameters are optional (None by default)
- Use Pydantic for automatic validation
- Literal types ensure only valid sort/order values
- Date format: ISO 8601 (YYYY-MM-DD) for consistency

### 2. Service Layer Changes (`services/flight.py`)

**Update `list_flights` function signature:**
```python
def list_flights(
    db: Session,
    origin: Optional[str] = None,
    destination: Optional[str] = None,
    departure_date_from: Optional[str] = None,
    departure_date_to: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    has_economy: Optional[bool] = None,
    has_business: Optional[bool] = None,
    has_galaxium: Optional[bool] = None,
    sort: Optional[str] = None,
    order: Optional[str] = 'asc'
) -> list[FlightOut]:
```

**Implementation approach:**
1. Start with base query: `db.query(Flight)`
2. Apply filters conditionally using SQLAlchemy's filter methods
3. Use `.ilike()` for case-insensitive partial matching on text fields
4. Extract date from `departure_time` string for date comparisons
5. Filter by seat availability (> 0 for specified classes)
6. Apply sorting based on sort parameter
7. Return results as `FlightOut` objects with computed prices

**Filter Logic:**
- **Origin/Destination**: `Flight.origin.ilike(f'%{origin}%')`
- **Date range**: Extract date portion from `departure_time` string
- **Price range**: Compare against `base_price` (economy price)
- **Seat availability**: Check if `{class}_seats_available > 0`
- **Sorting**: 
  - `price`: Sort by `base_price`
  - `departure_time`: Sort by `departure_time` string
  - `duration`: Calculate from departure/arrival times

### 3. REST API Changes (`server.py`)

**Update `/flights` endpoint:**
```python
@app.get("/flights", response_model=list[FlightOut], tags=["Flights"])
def get_flights(
    origin: Optional[str] = None,
    destination: Optional[str] = None,
    departure_date_from: Optional[str] = None,
    departure_date_to: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    has_economy: Optional[bool] = None,
    has_business: Optional[bool] = None,
    has_galaxium: Optional[bool] = None,
    sort: Optional[str] = None,
    order: Optional[str] = 'asc',
    db: Session = Depends(get_db)
):
    """List flights with optional filtering and sorting.
    
    Query Parameters:
    - origin: Filter by origin (case-insensitive partial match)
    - destination: Filter by destination (case-insensitive partial match)
    - departure_date_from: Minimum departure date (YYYY-MM-DD)
    - departure_date_to: Maximum departure date (YYYY-MM-DD)
    - min_price: Minimum economy price
    - max_price: Maximum economy price
    - has_economy: Only flights with economy seats available
    - has_business: Only flights with business seats available
    - has_galaxium: Only flights with galaxium seats available
    - sort: Sort by 'price', 'departure_time', or 'duration'
    - order: Sort order 'asc' or 'desc' (default: asc)
    """
    return flight.list_flights(
        db=db,
        origin=origin,
        destination=destination,
        departure_date_from=departure_date_from,
        departure_date_to=departure_date_to,
        min_price=min_price,
        max_price=max_price,
        has_economy=has_economy,
        has_business=has_business,
        has_galaxium=has_galaxium,
        sort=sort,
        order=order
    )
```

**Alternative approach using Pydantic model:**
```python
def get_flights(
    params: FlightQueryParams = Depends(),
    db: Session = Depends(get_db)
):
    return flight.list_flights(db=db, **params.model_dump(exclude_none=True))
```

### 4. Testing Strategy (`tests/test_services.py` & `tests/test_rest.py`)

**Service Layer Tests:**
- Test each filter independently
- Test filter combinations
- Test case-insensitive matching
- Test date range filtering
- Test price range filtering
- Test seat availability filtering
- Test sorting (all fields, both orders)
- Test empty results
- Test no filters (returns all)

**REST API Tests:**
- Test query parameter parsing
- Test invalid parameter values
- Test URL encoding
- Test combined filters
- Test response format
- Test error handling

**Example test cases:**
```python
def test_filter_by_origin(db_session):
    results = flight.list_flights(db_session, origin="earth")
    assert all("earth" in f.origin.lower() for f in results)

def test_filter_by_price_range(db_session):
    results = flight.list_flights(db_session, min_price=1000, max_price=5000)
    assert all(1000 <= f.base_price <= 5000 for f in results)

def test_sort_by_price_asc(db_session):
    results = flight.list_flights(db_session, sort="price", order="asc")
    prices = [f.base_price for f in results]
    assert prices == sorted(prices)
```

### 5. Frontend Integration (`booking_system_frontend/src/services/api.ts`)

**Update `getFlights` function:**
```typescript
export interface FlightFilters {
  origin?: string;
  destination?: string;
  departure_date_from?: string;
  departure_date_to?: string;
  min_price?: number;
  max_price?: number;
  has_economy?: boolean;
  has_business?: boolean;
  has_galaxium?: boolean;
  sort?: 'price' | 'departure_time' | 'duration';
  order?: 'asc' | 'desc';
}

export const getFlights = async (filters?: FlightFilters): Promise<Flight[]> => {
  const params = new URLSearchParams();
  
  if (filters) {
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.append(key, String(value));
      }
    });
  }
  
  const queryString = params.toString();
  const url = queryString ? `/api/flights?${queryString}` : '/api/flights';
  
  const response = await apiClient.get<Flight[]>(url);
  return response;
};
```

**Frontend UI Components:**
- Add search form with origin/destination inputs
- Add date range pickers
- Add price range sliders
- Add seat class checkboxes
- Add sort dropdown
- Update Flights page to use new filters

### 6. Documentation Updates

**Update API documentation:**
- Add query parameter descriptions to OpenAPI/Swagger
- Update README.md with example queries
- Add inline code comments

**Example API calls:**
```bash
# Filter by route
GET /api/flights?origin=Earth&destination=Mars

# Filter by price range
GET /api/flights?min_price=1000&max_price=5000

# Filter by date range
GET /api/flights?departure_date_from=2026-03-01&departure_date_to=2026-03-31

# Filter by seat availability
GET /api/flights?has_economy=true&has_business=true

# Combined filters with sorting
GET /api/flights?origin=Earth&max_price=10000&sort=price&order=asc

# Complex query
GET /api/flights?origin=Earth&destination=Mars&departure_date_from=2026-03-01&max_price=1500000&has_galaxium=true&sort=price&order=asc
```

## Implementation Order

1. ✅ **Schema changes** - Add `FlightQueryParams` to `schemas.py`
2. ✅ **Service layer** - Update `list_flights()` in `services/flight.py`
3. ✅ **REST endpoint** - Modify `/flights` in `server.py`
4. ✅ **Backend tests** - Add comprehensive test coverage
5. ✅ **Frontend API** - Update `api.ts` with filter support
6. ✅ **Frontend UI** - Add search/filter components (optional for MVP)
7. ✅ **Documentation** - Update README and API docs

## Technical Considerations

### Database Performance
- Current implementation uses SQLAlchemy ORM queries
- For small datasets (< 10k flights), in-memory filtering is acceptable
- For larger datasets, consider:
  - Adding database indexes on `origin`, `destination`, `departure_time`
  - Using database-level date functions for date filtering
  - Implementing pagination

### Date Handling
- `departure_time` is stored as string in format "YYYY-MM-DD HH:MM"
- Extract date portion using string slicing: `departure_time[:10]`
- Compare as strings (works for ISO format)
- Consider migrating to DateTime column type in future

### Price Filtering
- Filter on `base_price` (economy price)
- Frontend should clarify this is economy pricing
- Business/Galaxium prices are computed (2.5x and 5x multipliers)

### Backward Compatibility
- All parameters are optional
- No parameters = return all flights (current behavior)
- Existing API consumers continue to work unchanged

## Testing Checklist

- [ ] Unit tests for service layer filters
- [ ] Unit tests for sorting logic
- [ ] Integration tests for REST endpoint
- [ ] Test invalid parameter values
- [ ] Test edge cases (empty results, no filters)
- [ ] Test case-insensitive matching
- [ ] Test date range boundaries
- [ ] Test combined filters
- [ ] Frontend integration testing
- [ ] Manual testing with Swagger UI

## Success Criteria

1. ✅ All query parameters work as specified
2. ✅ Case-insensitive partial matching for text fields
3. ✅ Date range filtering works correctly
4. ✅ Price filtering uses economy price
5. ✅ Seat availability filtering works for all classes
6. ✅ Sorting works for all fields in both directions
7. ✅ All tests pass
8. ✅ Backward compatible (no breaking changes)
9. ✅ API documentation updated
10. ✅ Frontend can use new filters

## Future Enhancements

- Add pagination (limit/offset or cursor-based)
- Add full-text search
- Add more sort options (duration, popularity)
- Add filter by airline/aircraft type
- Add distance-based filtering
- Cache frequently used queries
- Add query performance monitoring