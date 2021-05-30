package fr.dwightstudio.dpt.engine.scripting;

import fr.dwightstudio.dpt.engine.graphics.render.Transform;
import fr.dwightstudio.dpt.engine.logging.GameLogger;

import java.text.MessageFormat;
import java.util.ArrayList;
import java.util.List;
public class GameObject {

    private final String name;
    private final List<Component> components;
    public Transform transform;
    private int zIndex;

    public GameObject(String name) {
        this.name = name;
        this.components = new ArrayList<>();
        this.transform = new Transform();
        this.zIndex = 0;
        GameLogger.getLogger("GameObject").debug(MessageFormat.format("Created GameObject : \"{0}\"", name));
    }

    public GameObject(String name, Transform transform) {
        this.name = name;
        this.components = new ArrayList<>();
        this.transform = transform;
        this.zIndex = 0;
        GameLogger.getLogger("GameObject").debug(MessageFormat.format("Create GameObject : \"{0}\"", name));
    }

    public GameObject(String name, int zIndex) {
        this.name = name;
        this.components = new ArrayList<>();
        this.transform = new Transform();
        this.zIndex = zIndex;
        GameLogger.getLogger("GameObject").debug(MessageFormat.format("Create GameObject : \"{0}\" with zIndex : {1}", name, zIndex));
    }

    public GameObject(String name, Transform transform, int zIndex) {
        this.name = name;
        this.components = new ArrayList<>();
        this.transform = transform;
        this.zIndex = zIndex;
        GameLogger.getLogger("GameObject").debug(MessageFormat.format("Create GameObject : \"{0}\" with zIndex : {1}", name, zIndex));
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

    public <T extends Component> List<T> getComponents(Class<T> componentClass) {
        List<T> componentList = new ArrayList<>();
        for (Component component : components) {
            if (componentClass.isAssignableFrom(component.getClass())) {
                try {
                    componentList.add(componentClass.cast(component));
                } catch (ClassCastException e) {
                    e.printStackTrace();
                }
            }
        }
        return componentList;
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

    public void init() {
        for (Component component : components) {
            component.init();
        }
    }

    public String getName() {
        return name;
    }

    public int getzIndex() {
        return zIndex;
    }
}
