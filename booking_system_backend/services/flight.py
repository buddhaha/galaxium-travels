from sqlalchemy.orm import Session
from models import Flight
from schemas import FlightOut
from typing import Optional
from datetime import datetime


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
    """List flights with optional filtering and sorting.
    
    Args:
        db: Database session
        origin: Filter by origin (case-insensitive partial match)
        destination: Filter by destination (case-insensitive partial match)
        departure_date_from: Minimum departure date (format: YYYY-MM-DD)
        departure_date_to: Maximum departure date (format: YYYY-MM-DD)
        min_price: Minimum economy price
        max_price: Maximum economy price
        has_economy: Only flights with economy seats available
        has_business: Only flights with business seats available
        has_galaxium: Only flights with galaxium seats available
        sort: Sort by 'price', 'departure_time', or 'duration'
        order: Sort order 'asc' or 'desc' (default: asc)
    
    Returns:
        List of FlightOut objects with computed prices for all seat classes
    """
    # Start with base query
    query = db.query(Flight)
    
    # Apply filters conditionally
    if origin:
        query = query.filter(Flight.origin.ilike(f'%{origin}%'))
    
    if destination:
        query = query.filter(Flight.destination.ilike(f'%{destination}%'))
    
    if departure_date_from:
        # Extract date portion from departure_time string (format: "YYYY-MM-DD HH:MM")
        query = query.filter(Flight.departure_time >= departure_date_from)
    
    if departure_date_to:
        # Add one day to include the entire end date
        query = query.filter(Flight.departure_time <= f'{departure_date_to} 23:59')
    
    if min_price is not None:
        query = query.filter(Flight.base_price >= min_price)
    
    if max_price is not None:
        query = query.filter(Flight.base_price <= max_price)
    
    if has_economy:
        query = query.filter(Flight.economy_seats_available > 0)
    
    if has_business:
        query = query.filter(Flight.business_seats_available > 0)
    
    if has_galaxium:
        query = query.filter(Flight.galaxium_seats_available > 0)
    
    # Execute query
    flights = query.all()
    
    # Convert to FlightOut objects with computed prices
    result = []
    for f in flights:
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
        result.append(FlightOut(**flight_dict))
    
    # Apply sorting if requested
    if sort:
        if sort == 'price':
            result.sort(key=lambda x: x.base_price, reverse=(order == 'desc'))
        elif sort == 'departure_time':
            result.sort(key=lambda x: x.departure_time, reverse=(order == 'desc'))
        elif sort == 'duration':
            # Calculate duration from departure and arrival times
            def get_duration(flight: FlightOut) -> int:
                try:
                    dep = datetime.strptime(flight.departure_time, "%Y-%m-%d %H:%M")
                    arr = datetime.strptime(flight.arrival_time, "%Y-%m-%d %H:%M")
                    return int((arr - dep).total_seconds())
                except:
                    return 0
            result.sort(key=get_duration, reverse=(order == 'desc'))
    
    return result
