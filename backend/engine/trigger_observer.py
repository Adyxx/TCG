

class TriggerObserver:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_name, callback):
        self.listeners.setdefault(event_name, []).append(callback)

    def emit(self, event_name, **kwargs):
        for callback in self.listeners.get(event_name, []):
            callback(**kwargs)

    def unsubscribe(self, event_name, callback):
        if event_name in self.listeners:
            self.listeners[event_name].remove(callback)

    def clear(self):
        self.listeners.clear()

    def print_trigger_listeners(event_name):
        listeners = trigger_observer.listeners.get(event_name, [])
        print(f"\n🔔 {len(listeners)} listeners for '{event_name}':")
        for i, callback in enumerate(listeners, 1):
            print(f"  {i}. {callback.__name__} (from {callback.__module__})")

trigger_observer = TriggerObserver()