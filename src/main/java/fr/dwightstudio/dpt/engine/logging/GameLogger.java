package fr.dwightstudio.dpt.engine.logging;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.LogManager;
import java.util.logging.Logger;

public class GameLogger {

    private static final LogManager logManager = LogManager.getLogManager();
    public static final Logger logger = Logger.getLogger("");

    public static boolean init() {
        try {
            logManager.readConfiguration(new FileInputStream("logger.properties"));
            logger.setLevel(Level.FINER);
            logger.log(Level.INFO, "Logger Initialized");
            return true;
        } catch (IOException exception) {
            logger.log(Level.SEVERE, "Cannot read logger configuration file", exception);
            return false;
        }
    }
}
