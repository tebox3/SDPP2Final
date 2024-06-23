import java.rmi.Remote;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.io.FileWriter;
import java.io.IOException;
import java.time.Instant;
import java.util.Date;

interface CentralLogServerInterface extends Remote {
    String logEvent(String timestamp,String eventType, String juego, String action, String[] args) throws RemoteException;
}

public class CentralLogServer extends UnicastRemoteObject implements CentralLogServerInterface {
    private static final String LOG_FILE = "logCentralizado.log";

    protected CentralLogServer() throws RemoteException {
        super();
    }

    public String logEvent(String timestamp,String eventType, String juego, String action, String[] args) throws RemoteException {
        try (FileWriter writer = new FileWriter(LOG_FILE, true)) {
            //long timestamp = Instant.now().getEpochSecond();
            String logMessage = timestamp + ", " + eventType + ", " + juego + ", " + action;
            for (String arg : args) {
                logMessage += ", " + arg;
            }
            writer.write(logMessage + "\n");
            return "Logged Successfully";
        } catch (IOException e) {
            e.printStackTrace();
            return "Logging Failed";
        }
    }

    public static void main(String[] args) {
        try {
            CentralLogServer server = new CentralLogServer();
            Registry registry = LocateRegistry.createRegistry(1099); // el servidor esta corriendo en el puerto 1099
            registry.bind("CentralLogServer", server);
            System.out.println("Central Log Server is ready.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
