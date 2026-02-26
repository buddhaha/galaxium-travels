# Flight Filters Implementation Plan (Local Demo)

**Related Issue**: [#10 - Add Flight Filtering and Sorting Features](https://github.ibm.com/Maximilian-Jesch/galaxium-travels-booking-system/issues/10)
**Brainstorming Document**: [`flight_filters_brainstorm.md`](flight_filters_brainstorm.md)
**Current Branch**: `feature/flight-filters`

---

## Overview

Add 8 filtering and sorting features to help users find flights. Currently only basic client-side search exists. This moves filtering to the backend and adds sorting, date/price ranges, and availability filters.

**Current State**:
- Backend: [`list_flights()`](../booking_system_backend/services/flight.py:6) returns all flights
- Frontend: [`Flights.tsx`](../booking_system_frontend/src/pages/Flights.tsx:36-41) filters client-side
- No sorting or advanced filters

**Goal**: Let users filter and sort flights by their preferences.

---

## Architecture Changes

### Backend
- Extend [`list_flights()`](../booking_system_backend/services/flight.py:6) with optional filter parameters
- Add SQLAlchemy query filters and ORDER BY clauses
- Create Pydantic models in [`schemas.py`](../booking_system_backend/schemas.py) for validation
- Update [`GET /flights`](../booking_system_backend/server.py) endpoint to accept query parameters

### Frontend
- Replace `searchTerm` state with `filters` object in [`Flights.tsx`](../booking_system_frontend/src/pages/Flights.tsx)
- Create filter components: `FlightFilters.tsx`, `SortDropdown.tsx`, `DateRangePicker.tsx`, `PriceRangeSlider.tsx`
- Update [`api.ts`](../booking_system_frontend/src/services/api.ts) to pass filter parameters

---

## Phase 1: Core Filters (High Priority)

### 1.1 Sort Options

**User Value**: Essential for decision-making, allows users to prioritize by price, time, or duration

**Backend Changes**:
- **File**: [`flight.py`](../booking_system_backend/services/flight.py:6)
- **Function**: `list_flights()`
- **New Parameters**:
  - `sort_by: str = "departure_time"` - Field to sort by
  - `sort_order: str = "asc"` - Sort direction
- **Logic**: Add SQLAlchemy `.order_by()` clause based on parameters
- **Sort Fields**: `departure_time`, `base_price`, calculated duration, total seats available
- **Validation**: Enum for valid sort fields, default to departure_time ascending

**Frontend Changes**:
- **Component**: New `SortDropdown.tsx` in `components/flights/`
- **Options**: 
  - Price: Low to High / High to Low
  - Departure: Earliest / Latest
  - Duration: Shortest / Longest
- **State**: Add `sortBy` and `sortOrder` to filters state
- **UI**: Dropdown in filter bar, show active sort with icon

**API Contract**:
- Query params: `?sort_by=base_price&sort_order=asc`
- No response schema changes

**Backend**: Add `sort_by` and `sort_order` parameters to [`list_flights()`](../booking_system_backend/services/flight.py:6), add SQLAlchemy ORDER BY clause

**Frontend**: Create `SortDropdown.tsx` with options for price, departure time, and duration

**Testing**: Basic unit tests for sort logic

---

### 1.2 Date Range Filter

**Backend**: Add `departure_from` and `departure_to` parameters, filter by date range using SQLAlchemy

**Frontend**: Create `DateRangePicker.tsx` with preset buttons ("Next 7 days", "This month") and custom range

**Testing**: Test date parsing and filtering

---

### 1.3 Price Range Filter

**Backend**: Add `price_min` and `price_max` parameters, filter where any seat class price falls in range

**Frontend**: Create `PriceRangeSlider.tsx` with dual-range slider

**Testing**: Test price filtering across seat classes

---

### 1.4 Seat Class Availability Filter

**Backend**: Add `seat_classes` parameter, filter where selected classes have seats available

**Frontend**: Add checkbox group in `FlightFilters.tsx` for Economy/Business/Galaxium

**Testing**: Test multi-select filtering

---

## Phase 2: Time & Availability Filters

### 2.1 Departure Time of Day Filter

**Backend**: Add `time_of_day` parameter, categorize into Morning/Afternoon/Evening/Night slots

**Frontend**: Add toggle buttons in `FlightFilters.tsx`

**Testing**: Test hour extraction and slot filtering

---

### 2.2 Flight Duration Filter

**Backend**: Add `min_duration` and `max_duration` parameters, calculate from departure/arrival times

**Frontend**: Add preset buttons ("Under 5 hours", "5-10 hours", "10+ hours")

**Testing**: Test duration calculation

---

### 2.3 Seat Availability Threshold

**Backend**: Add `min_seats` parameter, filter by total available seats

**Frontend**: Add number input or preset buttons ("2+", "4+", "6+")

**Testing**: Test seat threshold filtering

---

## Phase 3: Discovery Features

### 3.1 Destination Categories

**Backend**: Add `category` parameter with hardcoded mappings ("Inner Planets", "Outer Planets")

**Frontend**: Add category chips in `FlightFilters.tsx`

**Testing**: Test category filtering

---

## Technical Considerations

### Database Queries
- Use SQLAlchemy query chaining for filtering
- Add basic indexes on `departure_time` and `base_price` if needed

### Pagination (Optional)
- Add if result sets exceed 100 flights
- Simple `page` and `per_page` parameters with `.limit()` and `.offset()`

### Error Handling
- Validate filter parameters with Pydantic
- Return 400 for invalid parameters
- Show "No flights match your filters" for empty results
- Basic error messages in frontend

---

## Testing Strategy

### Unit Tests ([`test_services.py`](../booking_system_backend/tests/test_services.py))
- Test each filter parameter
- Test filter combinations
- Test sort logic
- Test edge cases (empty results, invalid params)

### Integration Tests ([`test_rest.py`](../booking_system_backend/tests/test_rest.py))
- Test `GET /flights` with filter combinations
- Test parameter validation
- Test response format

---

## Implementation Notes

- All filter parameters optional (backward compatible)
- AND logic between filter types (date AND price)
- OR logic within same type (economy OR business)
- Keep UI simple and functional for demo

---

**Document Version**: 2.0 (Simplified for Local Demo)
**Last Updated**: 2026-02-26
**Author**: Bob (Plan Mode)