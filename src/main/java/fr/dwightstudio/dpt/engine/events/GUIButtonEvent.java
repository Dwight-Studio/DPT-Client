package fr.dwightstudio.dpt.engine.events;

public interface GUIButtonEvent {
    void onClick(long buttonID);
    void onHover(long buttonID);
}
