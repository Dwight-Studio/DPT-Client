/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.events;

import fr.dwightstudio.dpt.engine.events.types.Event;
import fr.dwightstudio.dpt.engine.inputs.KeyboardListener;
import fr.dwightstudio.dpt.engine.inputs.MouseListener;
import fr.dwightstudio.dpt.engine.logging.GameLogger;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.text.MessageFormat;
import java.util.HashSet;

import static org.lwjgl.glfw.GLFW.*;

public class EventSystem implements Runnable {
    private final long window;

    private static final HashSet<EventListener> eventListeners = new HashSet<>();

    public EventSystem(long window) {
        this.window = window;
    }

    @Override
    public void run() {
        GameLogger.getLogger("EventSystem").debug("Event System Thread started");
        glfwSetKeyCallback(window, KeyboardListener.keyCallback); // Setup a key callback
        glfwSetMouseButtonCallback(window, MouseListener.mouseButtonCallback); // Setup a mouse buttons callback
        glfwSetCursorPosCallback(window, MouseListener.cursorPosCallback); // Setup a mouse cursor callback
        glfwSetScrollCallback(window, MouseListener.mouseScrollCallback); // Setup a mouse scroll wheel callback
    }

    /**
     * Fire an event
     *
     * @param event the event to fire
     */
    public static void fire(Event event) {
        //"Je REFLECHIT, ta compris la REFLECTION !!!"
        Runnable runnable = () -> {
            for (EventListener eventListener : eventListeners) {
                for (Method method : eventListener.getClass().getDeclaredMethods()) {
                    if (method.isAnnotationPresent(EventHandler.class)) {
                        Class<?> type = event.getClass();
                        while (type != Object.class) {
                            if (method.getParameterTypes()[0] == type) {
                                try {
                                    method.invoke(eventListener, event);
                                    break;
                                } catch (IllegalAccessException | InvocationTargetException e) {
                                    e.printStackTrace();
                                }
                            }
                            type = type.getSuperclass();
                        }
                    }
                }
            }
        };
        Thread thread = new Thread(runnable);
        thread.setName("Event Handler Thread");
        thread.start();
    }

    /**
     * Register a new listener
     *
     * @param eventListener the event listener to register
     */
    public static void registerListener(EventListener eventListener) {
        for (Method method : eventListener.getClass().getDeclaredMethods()) {
            if (method.isAnnotationPresent(EventHandler.class)) {
                if (method.getParameterCount() == 1 && method.getReturnType() == Void.TYPE && Modifier.isPublic(method.getModifiers()) && Event.class.isAssignableFrom(method.getParameterTypes()[0])) {
                    eventListeners.add(eventListener);
                } else {
                    GameLogger.getLogger("EventSystem").error(MessageFormat.format("Invalid EventHandler detected ({0}@{1})", method.getName(), eventListener.getClass().getName()));
                }
            }
        }
    }

    /**
     * Unregister an event listener
     *
     * @param eventListener the event listener to unregister
     */
    public static void unregisterListener(EventListener eventListener){
        eventListeners.remove(eventListener);
    }

}
