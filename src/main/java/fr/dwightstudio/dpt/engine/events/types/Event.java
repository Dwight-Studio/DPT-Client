package fr.dwightstudio.dpt.engine.events.types;

/**
 * Base Event class
 */
public class Event {

    private final Thread thread;

    public Event() {
        this.thread = Thread.currentThread();
    }

    /**
     * @return the Thread in which the event is fired
     */
    public Thread getThread() {
        return thread;
    }

}
