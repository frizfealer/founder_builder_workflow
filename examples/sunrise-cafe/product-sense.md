Status: Confirmed

# Product Sense — Sunrise Café AI Reservation Agent

## 1. Product Framing

- **User:** a visitor to Sunrise Café, a café admin who enters the café's tables, and café staff who mark parties as seated.
- **Problem:** the visitor should not need to understand the café's booking rules or fill out a traditional reservation form.
- **Desired outcome:** through natural-language conversation, the visitor finds an available table and the agent makes a reservation for it in a real reservation system.
- **Why AI:** the product is an AI reservation agent that the visitor uses through natural-language conversation.
- **Initial boundary:** reservations are real, not simulated. The product includes the café's reservation system as well as the agent.

## 2. Product Scope

- **In scope now:**
  - Finding an available table through natural-language conversation.
  - The agent making a real reservation for that table.
  - The café's reservation system, including an admin entering the café's tables.
- **Out of scope:** no out-of-scope items are established by the authoritative inputs.
- **Committed future scope:** no committed future scope is established by the authoritative inputs.

## 3. Responsibilities & Authority

- The agent makes reservations in the café's reservation system.
- The agent gets the visitor's explicit confirmation before making a reservation.
- A café admin enters the café's tables.
- Café staff mark a party as seated.
- Groups larger than 8 are not booked by the agent; they call the café.

## 4. Capabilities & Behaviors

- The visitor can use natural-language conversation to find an available table.
- The visitor can do this without understanding the café's booking rules and without filling out a traditional reservation form.
- The agent makes a reservation for the table in the café's reservation system.
- A reservation records the guest's name, the guest's phone number, the booking time, and the table it holds. No other details a reservation records are established by the authoritative inputs.
- An admin enters a table with its number of seats and a table label.
- Staff and the admin know each table's label. The visitor and the agent do not need to know it.
- Staff can mark a party as seated.
- No other behavior of the café's reservation system is established by the authoritative inputs.

## 5. Business & Domain Rules

- The café is open Tuesday to Sunday, 7:00–15:00, and closed on Monday.
- A party has 1 to 8 people. Larger groups call the café.
- Bookings start on the half hour. The last seating is 14:00.
- Each booking holds a table for 90 minutes. A held table is not available to other bookings during that time.
- A booking is made up to 30 days ahead, and at least 1 hour before the booking time.
- A party gets the smallest table that is still free and seats them.
- A table is held 15 minutes past the booking time. If staff have not marked the party as seated by then, the table is released.
- A table the visitor finds through the product is available under these rules.

## 6. Failure & Recovery

- When no available table fits the visitor's request, the product tells the visitor and offers other available options, such as other times.
- No other failure behavior is established by the authoritative inputs.

## 7. Acceptable Quality

- No quality bar is established by the authoritative inputs.

## 8. Deferred Questions

None.
