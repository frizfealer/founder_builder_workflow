# Product Idea

Build an AI reservation agent for Sunrise Café.

A visitor should be able to use natural-language conversation
to find an available table.

The visitor should not need to understand the café's booking
rules or fill out a traditional reservation form.

## Clarifications

- 2026-10-23, on whether the agent may make a reservation, real or simulated: "make a reservation for real system; lets build the reservation system for the cafe as well"
- 2026-10-23, on what the product does when no available table fits the visitor's request: "Suggest alternatives" (selected option: "Tell the visitor and offer other available options (e.g. other times).")
- 2026-10-23, on the café's tables: "Table should be allow admin to enters and we don't need id, just how many seats"
- 2026-10-23, on opening hours (example shown: "Tue–Sun 7:00–15:00, closed Monday"): "Open hour correct"
- 2026-10-23, on the booking rules: "ok this rules are good"
  - Party size 1–8; larger groups call the café
  - Bookings start on the half hour, last seating 14:00
  - Each booking holds a table for 90 minutes
  - Book up to 30 days ahead, at least 1 hour before
  - A party gets the smallest table that seats them
  - 2 tables are kept for walk-ins and are never booked
  - A table is held 15 minutes past the booking time, then released
- 2026-10-23, on whether "A party gets the smallest table that seats them" means the smallest free table or only the smallest table size: "the smallest table that's still free this one"
- 2026-10-23, on whether the agent needs the visitor's explicit OK before it makes a reservation: "Yes"
- 2026-10-23, on which 2 tables are kept for walk-ins (rule "2 tables are kept for walk-ins and are never booked"): "Lets remove that rule"
- 2026-10-23, on whether a table is released 15 minutes past the booking time only if the party hasn't arrived, and how arrival is known: "Staff mark them as seated"
- 2026-10-23, on what a reservation records so staff can find the party's booking and the table it holds (options shown: a guest name, a phone number, or a table label the admin can set), and on the earlier "we don't need id": "yes, guest name and phone number, and a table label. What I mean is the guest or ai agent doesnot need to know the table label, but the staff and admin should know it and there is an ID internally"
