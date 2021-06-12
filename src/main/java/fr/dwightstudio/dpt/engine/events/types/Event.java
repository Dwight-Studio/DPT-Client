/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

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
