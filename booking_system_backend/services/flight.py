from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func, cast, Integer
from models import Flight
from schemas import FlightOut, ErrorResponse
from datetime import datetime, timedelta
from typing import Optional


# Popular route categories (hardcoded for demo)
ROUTE_CATEGORIES = {
    'inner_planets': ['Earth', 'Mars', 'Venus', 'Mercury'],
    'outer_planets': ['Jupiter', 'Saturn', 'Uranus', 'Neptune'],
    'moons': ['Titan', 'Europa', 'Ganymede', 'Callisto', 'Io', 'Enceladus']
}


def list_flights(
    db: Session,
    # Phase 1: Core Filters
    sort_by: str = "departure_time",
    sort_order: str = "asc",
    departure_date_from: Optional[str] = None,
    departure_date_to: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    seat_class: Optional[str] = None,
    # Phase 2: Additional Filters
    departure_time_period: Optional[str] = None,  # morning, afternoon, evening, night
    min_duration: Optional[int] = None,  # in hours
    max_duration: Optional[int] = None,  # in hours
    min_seats_available: Optional[int] = None,
    # Phase 3: Popular Routes
    route_category: Optional[str] = None  # inner_planets, outer_planets, moons
) -> list[FlightOut] | ErrorResponse:
    """List flights with optional filtering and sorting.
    
    All parameters are optional for backward compatibility.
    
    Phase 1 Filters:
    - sort_by: Field to sort by (departure_time, base_price, duration, seats_available)
    - sort_order: Sort direction (asc, desc)
    - departure_date_from: Filter flights departing on or after this date (ISO format)
    - departure_date_to: Filter flights departing on or before this date (ISO format)
    - min_price: Minimum price (checks economy price)
    - max_price: Maximum price (checks economy price)
    - seat_class: Filter by seat class availability (economy, business, galaxium)
    
    Phase 2 Filters:
    - departure_time_period: Time of day (morning, afternoon, evening, night)
    - min_duration: Minimum flight duration in hours
    - max_duration: Maximum flight duration in hours
    - min_seats_available: Minimum total seats available
    
    Phase 3 Filters:
    - route_category: Route category (inner_planets, outer_planets, moons)
    """
    query = db.query(Flight)
    
    # Phase 1: Date range filter
    if departure_date_from:
        try:
            date_from = datetime.fromisoformat(departure_date_from.replace('Z', '+00:00'))
            query = query.filter(Flight.departure_time >= date_from.isoformat())
        except ValueError:
            return ErrorResponse(
                error="Invalid departure_date_from format",
                error_code="INVALID_DATE_FORMAT",
                details=f"The date '{departure_date_from}' is not in valid ISO format. Expected format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS"
            )
    
    if departure_date_to:
        try:
            date_to = datetime.fromisoformat(departure_date_to.replace('Z', '+00:00'))
            # Add one day to include the entire end date
            date_to = date_to + timedelta(days=1)
            query = query.filter(Flight.departure_time < date_to.isoformat())
        except ValueError:
            return ErrorResponse(
                error="Invalid departure_date_to format",
                error_code="INVALID_DATE_FORMAT",
                details=f"The date '{departure_date_to}' is not in valid ISO format. Expected format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS"
            )
    
    # Phase 1: Price range filter (based on economy price = base_price)
    if min_price is not None:
        query = query.filter(Flight.base_price >= min_price)
    
    if max_price is not None:
        query = query.filter(Flight.base_price <= max_price)
    
    # Phase 1: Seat class availability filter
    if seat_class:
        if seat_class == 'economy':
            query = query.filter(Flight.economy_seats_available > 0)
        elif seat_class == 'business':
            query = query.filter(Flight.business_seats_available > 0)
        elif seat_class == 'galaxium':
            query = query.filter(Flight.galaxium_seats_available > 0)
    
    # Phase 2: Departure time period filter
    if departure_time_period:
        # Extract hour from departure_time string (format: "YYYY-MM-DDTHH:MM:SS")
        # Morning: 6-11, Afternoon: 12-17, Evening: 18-21, Night: 22-5
        if departure_time_period == 'morning':
            query = query.filter(
                and_(
                    func.cast(func.substr(Flight.departure_time, 12, 2), Integer) >= 6,
                    func.cast(func.substr(Flight.departure_time, 12, 2), Integer) < 12
                )
            )
        elif departure_time_period == 'afternoon':
            query = query.filter(
                and_(
                    func.cast(func.substr(Flight.departure_time, 12, 2), Integer) >= 12,
                    func.cast(func.substr(Flight.departure_time, 12, 2), Integer) < 18
                )
            )
        elif departure_time_period == 'evening':
            query = query.filter(
                and_(
                    func.cast(func.substr(Flight.departure_time, 12, 2), Integer) >= 18,
                    func.cast(func.substr(Flight.departure_time, 12, 2), Integer) < 22
                )
            )
        elif departure_time_period == 'night':
            query = query.filter(
                or_(
                    func.cast(func.substr(Flight.departure_time, 12, 2), Integer) >= 22,
                    func.cast(func.substr(Flight.departure_time, 12, 2), Integer) < 6
                )
            )
    
    # Phase 2: Minimum seats available filter
    if min_seats_available is not None:
        total_seats = (
            Flight.economy_seats_available +
            Flight.business_seats_available +
            Flight.galaxium_seats_available
        )
        query = query.filter(total_seats >= min_seats_available)
    
    # Phase 3: Route category filter
    if route_category and route_category in ROUTE_CATEGORIES:
        destinations = ROUTE_CATEGORIES[route_category]
        query = query.filter(
            or_(
                Flight.origin.in_(destinations),
                Flight.destination.in_(destinations)
            )
        )
    
    # Get all flights before sorting (needed for duration calculation)
    flights = query.all()
    
    # Convert to result list with computed prices and duration
    result = []
    for f in flights:
        # Calculate duration in hours
        try:
            dep = datetime.fromisoformat(f.departure_time.replace('Z', '+00:00'))
            arr = datetime.fromisoformat(f.arrival_time.replace('Z', '+00:00'))
            duration_hours = (arr - dep).total_seconds() / 3600
        except (ValueError, AttributeError):
            duration_hours = 0
        
        # Phase 2: Duration filter
        if min_duration is not None and duration_hours < min_duration:
            continue
        if max_duration is not None and duration_hours > max_duration:
            continue
        
        # Compute prices for all seat classes
        flight_dict = {
            'flight_id': f.flight_id,
            'origin': f.origin,
            'destination': f.destination,
            'departure_time': f.departure_time,
            'arrival_time': f.arrival_time,
            'base_price': f.base_price,
            'economy_seats_available': f.economy_seats_available,
            'business_seats_available': f.business_seats_available,
            'galaxium_seats_available': f.galaxium_seats_available,
            'economy_price': f.base_price,  # 1x
            'business_price': int(f.base_price * 2.5),  # 2.5x
            'galaxium_price': f.base_price * 5  # 5x
        }
        result.append((FlightOut(**flight_dict), duration_hours, f))
    
    # Phase 1: Sorting
    valid_sort_fields = ['departure_time', 'base_price', 'duration', 'seats_available']
    if sort_by not in valid_sort_fields:
        sort_by = 'departure_time'
    
    reverse = (sort_order == 'desc')
    
    if sort_by == 'departure_time':
        result.sort(key=lambda x: x[0].departure_time, reverse=reverse)
    elif sort_by == 'base_price':
        result.sort(key=lambda x: x[0].base_price, reverse=reverse)
    elif sort_by == 'duration':
        result.sort(key=lambda x: x[1], reverse=reverse)
    elif sort_by == 'seats_available':
        result.sort(
            key=lambda x: (
                x[2].economy_seats_available +
                x[2].business_seats_available +
                x[2].galaxium_seats_available
            ),
            reverse=reverse
        )
    
    # Return only FlightOut objects
    return [flight_out for flight_out, _, _ in result]
