import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.sql.Date;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.io.IOException;
import java.util.List;


public class LogClient {
    private LogClient() {}

    public static void main(String[] args) {
        if (args.length < 1) {
            System.err.println("Usage: java LogClient <config-file>");
            System.exit(1);
        }
        //Se le da el nombre del archivo .log como argumento
        String logFilePath = args[0];

        // Verificar si el archivo de log existe
        if (!Files.exists(Paths.get(logFilePath))) {
            System.err.println("Log file not found: " + logFilePath);
            System.exit(1);
        }

        try {
            List<String> lines = Files.readAllLines(Paths.get(logFilePath));

            // Conecta al registro RMI en localhost y puerto 1099
            Registry registry = LocateRegistry.getRegistry("localhost", 1099);
            CentralLogServerInterface server = (CentralLogServerInterface) registry.lookup("CentralLogServer");

            for (String log : lines) {
                // Ignorar líneas vacías y líneas de log de servidor Flask
                if (log.trim().isEmpty() || log.contains("WARNING:") || log.contains("Running on") || log.contains("Press CTRL+C")) {
                    continue;
                }

                String[] parts = log.split(", ");
                if (parts.length < 4) {
                    System.err.println("Invalid log entry: " + log);
                    continue;
                }
                String timestamp = parts[0];
                String eventType = parts[1];
                String juego = parts[2];
                String action = parts[3];
                String[] argsLog = new String[parts.length - 4];
                System.arraycopy(parts, 4, argsLog, 0, parts.length - 4);
                try {
                    String response = server.logEvent(timestamp,eventType, juego, action, argsLog);
                    System.out.println(response);
                } catch (Exception e) {
                    System.err.println("Error logging event: " + e.getMessage());
                }
            }
        } catch (IOException | java.rmi.NotBoundException e) {
            e.printStackTrace();
        }
    }
}
