import datetime
import json
import os

FILE_NAME = 'events.json'
class Event:
    def __init__(self, date, description):
        self.date = date
        self.description = description

    def __str__(self):
        return f"{self.description} on {self.date}"
    
class EventCalendar:
    def __init__(self):
        self.events = self.load_events()

    def add_event(self, date, description):
        event = Event(date, description)
        if date in self.events:
            self.events[date].append(event)
        else:
            self.events[date] = [event]
        self.save_events()
        print(f"Event '{description}' added on {date} ")

    def remove_event(self, date, description):
        if date in self.events:
            original_length = len(self.events[date])
            self.events[date] = [event for event in self.events[date] if event.description]
            if len(self.events[date]) < original_length:
                print(f"Event '{description}' removed from {date}. ")
                if not self.events[date]:
                    del self.events[date]
                self.save_events()
            else:
                print(f"Event '{description}' not found on '{date}'. ")
        else:
            print(f"No events found on {date}.")

    def view_events(self, date):
        if date in self.events:
            print(f"Events on {date}:")
            for i, event in enumerate(self.events[date], 1):
                print(f"{i}. {event.description}")
        else:
            print(f"No events on {date}")

    def load_events(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, 'r') as file:
                events_data = json.load(file)
                events = {}
                for date, event_list in events_data.items():
                    events[date] = [Event(date, desc) for desc in event_list]
                return events
        return {}
    
    def save_events(self):
        #events_data = {date:[event.description for event in event_list] for date, event_list in self.events.items()}
        events_data = {date: [event.description for event in event_list] for date, event_list in self.events.items()}
       
        with open(FILE_NAME, 'w') as file:
            json.dump(events_data, file)
        
class EventManager:
    def __init__(self):
        self.calendar = EventCalendar()

    def run(self):
        while True:
            print(".\nEvent Calendar")
            print("1. Add Event")
            print("2. Remove Event")
            print("3. View Events")
            print("4. Exit")
            choice = input("Choose an option: ")
            if choice == '1':
                date_str = input("Enter date (YYYY-MM-DD)")
                description = input("Enter event description: ")
                try:
                    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date().isoformat()
                    self.calendar.add_event(date, description)
                except ValueError:
                    print("Invalid date format. Please try again.")
            
            elif choice == '2':
                date_str = input("Enter date (YYYY-MM-DD): ")
                description = input("Enter event description: ")
                try:
                    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date().isoformat()
                    self.calendar.remove_event(date, description)
                except ValueError:
                    print("Invalid date format. Please try again")
            elif choice == '3':
                date_str = input("Enter date (YYY-MM-DD): ")
                try:
                    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date().isoformat()
                    self.calendar.view_events(date)
                except ValueError:
                    print("Invalid date format. Please try again.")

            elif choice == '4':
                print("Exiting the program.")
                
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    manager = EventManager()
    manager.run()