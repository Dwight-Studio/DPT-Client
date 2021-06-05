package fr.dwightstudio.dpt.engine.scripting;

public abstract class Component {

    public GameObject gameObject = null;

    public void update(float dt) {}
    public void remove() {}

    public void init() {}
}
