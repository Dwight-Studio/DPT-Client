package fr.dwightstudio.dpt.engine.logging;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.PrintStream;

public class GameLogger {

    public static final Logger logger = LogManager.getLogger("GameLogger");

    public static void init() {
        System.setErr(createLoggingProxy(System.err));
        logger.info("Logger initialized");
    }

    public static PrintStream createLoggingProxy(final PrintStream printStream) {
        return new PrintStream(printStream) {
            public void print(final String string) {
                printStream.print(string);
                logger.fatal(string);
            }
        };
    }

    public static Logger getLogger(String name) {
        return LogManager.getLogger(name);
    }
}
