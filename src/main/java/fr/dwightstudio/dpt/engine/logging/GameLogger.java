package fr.dwightstudio.dpt.engine.logging;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.util.logging.Level;
import java.util.logging.LogManager;
import java.util.logging.Logger;

public class GameLogger {

    private static final LogManager logManager = LogManager.getLogManager();
    private static final Logger logger = Logger.getLogger("");

    public static boolean init() {
        try {
            logManager.readConfiguration(new FileInputStream("logger.properties"));
            System.setErr(createLoggingProxy(System.err));
            logger.setLevel(Level.FINER);
            logger.log(Level.INFO, "Logger Initialized");
            return true;
        } catch (IOException exception) {
            logger.log(Level.SEVERE, "Cannot read logger configuration file", exception);
            return false;
        }
    }

    public static PrintStream createLoggingProxy(final PrintStream printStream) {
        return new PrintStream(printStream) {
            public void print(final String string) {
                printStream.print(string);
                logger.log(Level.SEVERE, string);
            }
        };
    }

    public static void log(Level level, String string) {
        logger.log(level, string);
    }

    public static void log(Level level, String string, Object[] params) {
        logger.log(level, string, params);
    }

    public static void log(Level level, String string, Object param) {
        logger.log(level, string, param);
    }

    public static void log(Level level, String string, Throwable thrown) {
        logger.log(level, string, thrown);
    }
}
