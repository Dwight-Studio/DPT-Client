package fr.dwightstudio.dpt.engine.logging;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.PrintStream;

public class GameLogger {

    public static final Logger logger = LogManager.getLogger("GameLogger");

    /**
     * Initialize the GameLogger
     */
    public static void init() {
        System.setErr(createLoggingProxy(System.err));
        logger.info("Logger initialized");
    }

    /**
     * This will create a proxy for a print stream
     * Basically it will redirect the specified print stream to the logger
     *
     * @param printStream the print stream to redirect
     * @return a PrintStream
     */
    public static PrintStream createLoggingProxy(final PrintStream printStream) {
        return new PrintStream(printStream) {
            public void print(final String string) {
                printStream.print(string);
                logger.fatal(string);
            }
        };
    }

    /**
     * @param name the logger instance of the specified name
     * @return a Logger
     */
    public static Logger getLogger(String name) {
        return LogManager.getLogger(name);
    }
}
