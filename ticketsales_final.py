# Imports
import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Venue:
    name: str
    capacity: int
    rental_cost: float
    city: str

@dataclass
class Event:
    date: datetime.date
    venue_name: str
    artist_name: str
    expected_attendance: int
    ticket_price: float
    artist_cost: float
    operations_cost: float
    rental_cost: float
    fees_percent: float = 0.10
    merch_spend_per_head: float = 0.0
    
    # Creates floating point values for accurate and concise data and information
    
    def ticket_gross(self) -> float:
        return self.expected_attendance * self.ticket_price

    def fees_total(self) -> float:
        return self.ticket_gross() * self.fees_percent

    def merch_gross(self) -> float:
        return self.expected_attendance * self.merch_spend_per_head

    def total_revenue(self) -> float:
        return self.ticket_gross() + self.merch_gross()

    def total_costs(self) -> float:
        return self.artist_cost + self.operations_cost + self.rental_cost + self.fees_total()

    def profit(self) -> float:
        return self.total_revenue() - self.total_costs()


# Venues Directory
VENUES: Dict[str, Venue] = {
    "Jammin Java": Venue("Jammin Java", 200, 2500, "Vienna, VA"),
    "Pearl Street Warehouse": Venue("Pearl Street Warehouse", 300, 3000, "Washington, DC"),
    "Rams Head On Stage": Venue("Rams Head On Stage", 300, 3500, "Annapolis, MD"),
    "The Atlantis": Venue("The Atlantis", 450, 5000, "Washington, DC"),
    "Union Stage": Venue("Union Stage", 450, 4500, "Washington, DC"),
    "The Birchmere": Venue("The Birchmere", 500, 5500, "Alexandria, VA"),
    "Baltimore Soundstage": Venue("Baltimore Soundstage", 1000, 8000, "Baltimore, MD"),
    "9:30 Club": Venue("9:30 Club", 1200, 12000, "Washington, DC"),
    "Lincoln Theatre": Venue("Lincoln Theatre", 1225, 12000, "Washington, DC"),
    "Rams Head Live / Nevermore Hall": Venue("Rams Head Live / Nevermore Hall", 1500, 14000, "Baltimore, MD"),
    "Warner Theatre": Venue("Warner Theatre", 1900, 18000, "Washington, DC"),
    "The Fillmore Silver Spring": Venue("The Fillmore Silver Spring", 2000, 20000, "Silver Spring, MD"),
    "Hippodrome Theatre": Venue("Hippodrome Theatre", 2300, 22000, "Baltimore, MD"),
    "Echostage": Venue("Echostage", 3000, 24000, "Washington, DC"),
    "MGM National Harbor Theater": Venue("MGM National Harbor Theater", 3500, 30000, "Oxon Hill, MD"),
    "Pier Six Pavilion": Venue("Pier Six Pavilion", 4400, 28000, "Baltimore, MD"),
    "The Anthem": Venue("The Anthem", 6000, 35000, "Washington, DC"),
    "EagleBank Arena": Venue("EagleBank Arena", 10000, 100000, "Fairfax, VA"),
    "Merriweather Post Pavilion": Venue("Merriweather Post Pavilion", 19319, 75000, "Columbia, MD"),
    "CFG Bank Arena": Venue("CFG Bank Arena", 20000, 120000, "Baltimore, MD"),
    "Capital One Arena": Venue("Capital One Arena", 20000, 150000, "Washington, DC"),
    "M&T Bank Stadium": Venue("M&T Bank Stadium", 70000, 350000, "Baltimore, MD"),
}


# Helper Functions to select venue
def choose_venue_by_tickets(tickets: int) -> Optional[Venue]:
    for v in sorted(VENUES.values(), key=lambda v: v.capacity):
        if tickets <= v.capacity:
            return v
    return None


def input_int(prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    while True:
        try:
            val = int(input(prompt))
            if min_val is not None and val < min_val:
                print(f"Value must be >= {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"Value must be <= {max_val}.")
                continue
            return val
        except ValueError:
            print("Invalid input! Please enter a whole integer.")


def input_float(prompt: str, min_val: Optional[float] = None) -> float:
    while True:
        try:
            val = float(input(prompt))
            if min_val is not None and val < min_val:
                print(f"Value must be >= {min_val}.")
                continue
            return val
        except ValueError:
            print("Invalid input! Please enter a real number.")

# Showcases avaliable venues
def pick_venue_by_menu() -> Venue:
    print("\nAvailable Venues:")
    sorted_venues = sorted(VENUES.values(), key=lambda v: v.capacity)
    for idx, v in enumerate(sorted_venues, start=1):
        print(f"{idx}. {v.name} — capacity {v.capacity} — rental ${v.rental_cost:,.0f} — {v.city}")
    choice = input_int("Select a venue by number: ", 1, len(sorted_venues))
    return sorted_venues[choice - 1]

# Plans out the events and chooses venue
def plan_event() -> Event:
    print("\n--- Plan a New Event ---")
    mode = input("Choose venue selection mode: [A]uto by tickets / [M]anual pick: ").strip().lower()
    if mode == "a":
        tickets = input_int("Estimated tickets the artist can sell: ", 1)
        venue = choose_venue_by_tickets(tickets)
        if not venue:
            print("No venue can accommodate this attendance! Try another estimate or choose a different market.")
            venue = pick_venue_by_menu()
        expected_attendance = min(tickets, venue.capacity)
    else:
        venue = pick_venue_by_menu()
        expected_attendance = input_int(f"Expected attendance (<= {venue.capacity}): ", 1, venue.capacity)
    
    # The information on what the user inputs for the data
    
    artist_name = input("Artist name: ").strip() or "Unknown Artist"
    date_str = input("Event date (YYYY-MM-DD): ").strip()
    date = datetime.date.fromisoformat(date_str)

    artist_cost = input_float("Artist Cost ($): ", 0.0)
    operations_cost = input_float("Operations Cost ($): ", 0.0)
    rental_cost = venue.rental_cost
    fees_percent = input_float("Fees percent (ex. 0.10 for 10%): ", 0.0)
    merch_per_head = input_float("Merch spend per attendee ($): ", 0.0)
    ticket_price = input_float("Ticket Price Average($): ", 0.0)

    event = Event(
        date=date,
        venue_name=venue.name,
        artist_name=artist_name,
        expected_attendance=expected_attendance,
        ticket_price=ticket_price,
        artist_cost=artist_cost,
        operations_cost=operations_cost,
        rental_cost=rental_cost,
        fees_percent=fees_percent,
        merch_spend_per_head=merch_per_head
    )
    # Entire summary of venue, attendance, cost, etc.
    
    print("\n--- Event Summary ---")
    print(f"Venue: {venue.name} (capacity {venue.capacity}, rental ${venue.rental_cost:,.0f})")
    print(f"Artist: {artist_name} on {event.date.isoformat()} — expected attendance: {event.expected_attendance}")
    print(f"Ticket price: ${event.ticket_price:.2f}")
    print(f"Ticket gross: ${event.ticket_gross():,.2f}")
    print(f"Fees ({fees_percent*100:.1f}%): ${event.fees_total():,.2f}")
    print(f"Merch gross: ${event.merch_gross():,.2f}")
    print(f"Costs (artist + operational costs + rental + fees): ${event.total_costs():,.2f}")
    print(f"Total revenue: ${event.total_revenue():,.2f}")
    print(f"Profit: ${event.profit():,.2f}")

    return event

# Scheduling of events

def list_events(events: List[Event]) -> None:
    if not events:
        print("\nNo events have been scheduled yet.")
        return
    print("\n--- Scheduled Events ---")
    for e in sorted(events, key=lambda ev: (ev.date, ev.venue_name)):
        print(f"{e.date.isoformat()} — {e.venue_name} — {e.artist_name} — "
              f"{e.expected_attendance}/{VENUES[e.venue_name].capacity} "
              f"— price ${e.ticket_price:.2f} — profit ${e.profit():,.2f}")

# Option 3: Removing Events

def remove_event(events: List[Event]) -> None:
    list_events(events)
    if not events:
        return

    date_str = input("Enter date (YYYY-MM-DD) of the event to remove: ").strip()
    try:
        date = datetime.date.fromisoformat(date_str)
    except ValueError:
        print("Invalid date format.")
        return

    
    for e in events:
        if e.date == date:
            events.remove(e)
            print(f"Removed event on {date.isoformat()} at {e.venue_name}.")
            return

    print("No event was found on that specific date.")
    
    # Main Programming Loop that gives the user the prompt (choosing options)
    
if __name__ == "__main__":
    events: List[Event] = []

    while True:
        print("\n--- Concert Event Planner ---")
        print("\nWelcome! Please select the four options below to book a show!")
        print("1. Plan a new event")
        print("2. List events")
        print("3. Remove an event")
        print("4. Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            event = plan_event()
            events.append(event)
        elif choice == "2":
            list_events(events)
        elif choice == "3":
            remove_event(events)
        elif choice == "4":
            print("Goodbye And Thank You For Using Our Platform!")
            break
        else:
            print("Invalid choice, please try again.")