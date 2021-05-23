package fr.dwightstudio.dpt.engine.scripting;

import fr.dwightstudio.dpt.engine.logging.GameLogger;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;

public class GameObject {

    private final String name;
    private final List<Component> components;

    public GameObject(String name) {
        this.name = name;
        this.components = new ArrayList<>();
        GameLogger.logger.log(Level.FINE, "Created GameObject : \"{0}\"", new Object[] {name});
    }

    public <T extends Component> T getComponent(Class<T> componentClass) {
        for (Component component : components) {
            if (componentClass.isAssignableFrom(component.getClass())) {
                try {
                    return componentClass.cast(component);
                } catch (ClassCastException e) {
                    e.printStackTrace();
                }
            }
        }

        return null;
    }

    public <T extends  Component> void removeComponent(Class<T> componentClass) {
        for (int i = 0; i < components.size(); i++) {
            if (componentClass.isAssignableFrom(components.get(i).getClass())) {
                components.remove(i);
                return;
            }
        }
    }

    public void addComponent(Component component) {
        this.components.add(component);
        component.gameObject = this;
    }

    public void update(float dt) {
        for (Component component : components) {
            component.update(dt);
        }
    }

    public void start() {
        for (Component component : components) {
            component.start();
        }
    }

    public String getName() {
        return name;
    }
}
