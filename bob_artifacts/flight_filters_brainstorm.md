# Flight Filters Brainstorming - Galaxium Travels

## Current State Analysis

### Existing Filtering Capabilities

**Frontend ([`Flights.tsx`](booking_system_frontend/src/pages/Flights.tsx:36-41))**
- **Text Search**: Filters flights by origin or destination (case-insensitive substring match)
- **Implementation**: Client-side filtering using JavaScript `.filter()` method
- **UI**: Single search input with Search icon, shows count of filtered results

**Backend ([`flight.py`](booking_system_backend/services/flight.py:6-27))**
- **No filtering**: `list_flights()` returns all flights without any filter parameters
- **Data returned**: All flight fields including seat availability and computed prices for all classes

**Data Model ([`models.py`](booking_system_backend/models.py:19-29))**
Available fields in Flight model:
- `origin`, `destination` (String)
- `departure_time`, `arrival_time` (String - ISO format)
- `base_price` (Integer)
- `economy_seats_available`, `business_seats_available`, `galaxium_seats_available` (Integer)

### Current Limitations
- Only basic text search on origin/destination
- No date/time filtering
- No price range filtering
- No seat class availability filtering
- No sorting options
- All filtering happens client-side (inefficient for large datasets)

---

## Brainstorming: Additional Filter Options

### 1. **Date Range Filter** 🗓️
**Description**: Filter flights by departure date range (e.g., "Next 7 days", "This month", custom range)

**User Value**: ⭐⭐⭐⭐⭐ (Essential for travel planning)

**Implementation Complexity**: 🟢 Low-Medium
- Frontend: Date picker component or preset buttons
- Backend: Parse ISO datetime strings, filter by date range
- No schema changes needed

**Technical Notes**:
- Departure times are stored as ISO strings in [`models.py`](booking_system_backend/models.py:24)
- Add query parameters: `?departure_from=2026-03-01&departure_to=2026-03-31`
- Consider timezone handling for interplanetary travel

---

### 2. **Price Range Filter** 💰
**Description**: Filter by minimum/maximum price across all seat classes

**User Value**: ⭐⭐⭐⭐⭐ (Critical for budget-conscious travelers)

**Implementation Complexity**: 🟢 Low
- Frontend: Dual-range slider or min/max inputs
- Backend: Filter where any seat class price falls within range
- No schema changes needed

**Technical Notes**:
- Prices computed in [`flight.py`](booking_system_backend/services/flight.py:22-24): economy (1x), business (2.5x), galaxium (5x)
- Filter logic: `(economy_price >= min AND economy_price <= max) OR (business_price >= min AND business_price <= max) OR (galaxium_price >= min AND galaxium_price <= max)`
- Consider showing price distribution histogram

---

### 3. **Seat Class Availability Filter** 💺
**Description**: Show only flights with available seats in specific class(es)

**User Value**: ⭐⭐⭐⭐ (Prevents disappointment from sold-out classes)

**Implementation Complexity**: 🟢 Low
- Frontend: Checkbox group for Economy/Business/Galaxium
- Backend: Filter where selected class(es) have `seats_available > 0`
- No schema changes needed

**Technical Notes**:
- Seat availability already in model: [`economy_seats_available`](booking_system_backend/models.py:27), [`business_seats_available`](booking_system_backend/models.py:28), [`galaxium_seats_available`](booking_system_backend/models.py:29)
- Multiple selections = OR logic (show if ANY selected class available)
- Could add "minimum seats" threshold (e.g., "at least 2 seats")

---

### 4. **Flight Duration Filter** ⏱️
**Description**: Filter by travel time (e.g., "Under 5 hours", "5-10 hours", "10+ hours")

**User Value**: ⭐⭐⭐⭐ (Important for comfort preferences)

**Implementation Complexity**: 🟡 Medium
- Frontend: Preset duration ranges or custom slider
- Backend: Calculate duration from departure/arrival times, filter by range
- No schema changes needed

**Technical Notes**:
- Duration calculated from [`departure_time`](booking_system_backend/models.py:24) and [`arrival_time`](booking_system_backend/models.py:25)
- Already computed in frontend: [`calculateDuration()`](booking_system_frontend/src/utils/formatters.ts) utility
- Backend needs similar calculation for filtering
- Consider interplanetary time dilation effects (thematic!)

---

### 5. **Departure Time of Day Filter** 🌅
**Description**: Filter by departure time slots (Morning, Afternoon, Evening, Night)

**User Value**: ⭐⭐⭐⭐ (Preference-based, affects travel experience)

**Implementation Complexity**: 🟢 Low
- Frontend: Button group or checkboxes for time slots
- Backend: Extract hour from ISO datetime, categorize into slots
- No schema changes needed

**Technical Notes**:
- Time slots: Morning (6-12), Afternoon (12-18), Evening (18-24), Night (0-6)
- Parse hour from [`departure_time`](booking_system_backend/models.py:24) ISO string
- Multiple selections = OR logic
- Consider planetary time zones (Earth time vs Mars time?)

---

### 6. **Popular Routes / Destination Categories** 🌍
**Description**: Quick filters for popular destinations or route types (Inner Planets, Outer Planets, Moon Bases)

**User Value**: ⭐⭐⭐ (Nice-to-have for discovery)

**Implementation Complexity**: 🟡 Medium
- Frontend: Preset filter chips/buttons
- Backend: Categorize destinations, add category field or use mapping
- May need schema enhancement for scalability

**Technical Notes**:
- Current destinations in seed data: Earth, Mars, Moon, Venus, Jupiter, Saturn, etc.
- Could hardcode categories initially: `{"Inner": ["Earth", "Mars", "Venus", "Moon"], "Outer": ["Jupiter", "Saturn"]}`
- Better approach: Add `destination_category` field to Flight model
- Enables "Explore Mars routes" or "Weekend Moon trips" marketing

---

### 7. **Seat Availability Threshold** 🎫
**Description**: Filter by minimum available seats (e.g., "Group travel: 4+ seats available")

**User Value**: ⭐⭐⭐ (Essential for group bookings)

**Implementation Complexity**: 🟢 Low
- Frontend: Number input or preset buttons (2+, 4+, 6+)
- Backend: Filter where total available seats >= threshold
- No schema changes needed

**Technical Notes**:
- Sum across all classes: [`economy_seats_available + business_seats_available + galaxium_seats_available`](booking_system_frontend/src/components/flights/FlightCard.tsx:13)
- Or filter by specific class availability
- Useful for families, corporate travel, tour groups

---

### 8. **Sort Options** 🔄
**Description**: Sort flights by price (low/high), departure time (earliest/latest), duration (shortest/longest), availability

**User Value**: ⭐⭐⭐⭐⭐ (Critical for decision-making)

**Implementation Complexity**: 🟢 Low
- Frontend: Dropdown or button group for sort options
- Backend: Add `ORDER BY` clause to query
- No schema changes needed

**Technical Notes**:
- Sort fields: `base_price`, `departure_time`, calculated duration, total seats
- Default: Departure time ascending (soonest first)
- Can be client-side initially, move to backend for performance
- Consider "Best Value" sort (price/duration ratio)

---

## Prioritization Matrix

### High Priority (Implement First)
1. **Sort Options** - Essential UX, low complexity, high impact
2. **Date Range Filter** - Core travel planning feature
3. **Price Range Filter** - Budget-critical, simple implementation
4. **Seat Class Availability Filter** - Prevents user frustration

### Medium Priority (Phase 2)
5. **Departure Time of Day Filter** - Preference-based, good UX
6. **Flight Duration Filter** - Comfort consideration
7. **Seat Availability Threshold** - Group travel support

### Lower Priority (Nice-to-Have)
8. **Popular Routes / Destination Categories** - Discovery feature, requires more planning

---

## Technical Implementation Considerations

### Backend Changes Required

**Modify [`flight.py`](booking_system_backend/services/flight.py:6)**:
```python
def list_flights(
    db: Session,
    departure_from: str | None = None,
    departure_to: str | None = None,
    price_min: int | None = None,
    price_max: int | None = None,
    seat_classes: list[str] | None = None,
    time_of_day: list[str] | None = None,
    min_duration: int | None = None,
    max_duration: int | None = None,
    min_seats: int | None = None,
    sort_by: str = "departure_time",
    sort_order: str = "asc"
) -> list[FlightOut]:
```

**API Endpoint Updates**:
- Add query parameters to `GET /flights` endpoint
- Validate filter parameters
- Apply filters in SQL query for performance

### Frontend Changes Required

**New Components Needed**:
- `FlightFilters.tsx` - Comprehensive filter panel
- `DateRangePicker.tsx` - Date selection component
- `PriceRangeSlider.tsx` - Dual-range slider
- `SortDropdown.tsx` - Sort options selector

**State Management**:
- Expand filter state beyond just `searchTerm`
- Consider URL query params for shareable filtered views
- Debounce filter changes to reduce API calls

### Performance Considerations

- **Pagination**: Add pagination for large result sets
- **Caching**: Cache filter results on backend
- **Indexing**: Add database indexes on `departure_time`, `base_price`
- **Client vs Server**: Move filtering to backend for datasets > 100 flights

### UX Enhancements

- **Active Filter Indicators**: Show applied filters as removable chips
- **Filter Presets**: "Weekend Getaways", "Budget Flights", "Luxury Travel"
- **Save Filters**: Allow users to save favorite filter combinations
- **Clear All**: One-click to reset all filters
- **Results Count**: Always show "X flights match your filters"

---

## Recommended Implementation Order

### Phase 1: Core Filters (Week 1)
1. Add sort options (price, time, duration)
2. Implement date range filter
3. Add price range filter
4. Backend API parameter support

### Phase 2: Availability Filters (Week 2)
5. Seat class availability checkboxes
6. Minimum seats threshold
7. Departure time of day filter

### Phase 3: Advanced Features (Week 3)
8. Flight duration filter
9. Popular routes/categories
10. Filter presets and saved searches

### Phase 4: Polish (Week 4)
11. Performance optimization (pagination, caching)
12. Mobile-responsive filter UI
13. Analytics on filter usage
14. A/B testing filter layouts

---

## Space Travel Theme Opportunities

Consider these thematic enhancements:
- **"Warp Speed" Filter**: Fastest routes only
- **"Scenic Route"**: Longer flights with better views
- **"Launch Window"**: Optimal departure times based on planetary alignment
- **"Gravity Assist"**: Flights with layovers that reduce total cost
- **"Radiation Level"**: Safety-conscious filter for solar activity
- **"Zero-G Duration"**: Time spent in zero gravity during flight

---

## Conclusion

The current implementation has a solid foundation with basic search, but lacks essential filtering capabilities that users expect from modern booking systems. The recommended filters balance user value with implementation complexity, prioritizing features that directly impact booking decisions (price, date, availability) before adding convenience features (time of day, duration) and discovery features (categories).

**Key Takeaway**: Implement sorting and the top 4 filters first to achieve 80% of user value with 20% of the effort.