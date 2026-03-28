## Problem

Currently, users can only book individual seats one at a time. Families and groups traveling together need a streamlined way to book multiple seats on the same flight in a single transaction, ensuring they can coordinate their travel plans efficiently.

## Proposed Solution

Implement a family/group booking flow that allows users to:

1. Select a flight and specify the number of passengers (2–10 travelers)
2. Enter passenger details for each traveler in the group
3. Book all seats together in a single transaction
4. Ensure seat availability for the entire group before confirming
5. Have one primary booker who manages the group reservation

## Technical Approach (initial proposal)

**Backend:**
- Extend the booking model with a `group_id` field to link related bookings
- Add `group_size`, `is_primary_booking`, and `passenger_name` fields
- Modify `book_flight()` to handle multiple passenger bookings atomically
- Validate sufficient seats are available for the entire group before inserting

**Database schema (proposed):**
```sql
-- Add to bookings table
group_id          UUID     (nullable, links related bookings)
group_size        INTEGER  (total passengers in group)
is_primary_booking BOOLEAN (identifies the main booking)
passenger_name    VARCHAR  (name of this specific passenger)
```

## Acceptance Criteria

- [ ] Users can select 2–10 passengers when booking a flight
- [ ] System validates sufficient seats are available for the entire group
- [ ] Group bookings are created atomically (all succeed or all fail)
- [ ] Cancelling a group booking cancels all associated bookings
- [ ] Backend API endpoint supports group booking creation
- [ ] Tests cover group booking scenarios (success, insufficient availability, validation)

## Out of Scope (Phase 1)

- Frontend changes
- Payment splitting among group members
- Add/remove passengers after initial booking
- Email notifications to group members
- Seat selection to ensure group sits together

## Priority

Medium — enhances user experience for a common travel scenario
