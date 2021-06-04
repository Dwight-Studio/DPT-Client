package fr.dwightstudio.dpt.engine.events;

import fr.dwightstudio.dpt.engine.logging.GameLogger;

public class EventHandler {

    private final EventSystemI event;

    public EventHandler(EventSystemI event) {
        this.event = event;
        EventSystem.eventHandlers.add(this);
        GameLogger.getLogger("EventHandler").debug("New EventHandler created");
    }

    public <T extends EventSystemI> T getEvent(Class<T> eventClass) {
        if (eventClass.isAssignableFrom(this.event.getClass())) {
            try {
                return eventClass.cast(event);
            } catch (ClassCastException e) {
                e.printStackTrace();
            }
        }
        return null;
    }

    public void update() {
        event.eventUpdate();
    }
}
