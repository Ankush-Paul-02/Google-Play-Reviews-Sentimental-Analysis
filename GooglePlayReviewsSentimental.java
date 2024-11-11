
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;

public class GooglePlayReviewsSentimental {

    public static void main(String[] args) {
        // Define the path to the Python script
        String pythonScriptPath = "google_play_reviews_sentimental.py"; // Adjust this path if needed
        String appId = "com.skillcat";

        // Create a list of command arguments
        List<String> command = new ArrayList<>();
        command.add("python"); // Use "python" if Python is in the PATH
        command.add(pythonScriptPath);
        command.add(appId);

        // Use ProcessBuilder to start the Python process
        ProcessBuilder processBuilder = new ProcessBuilder(command);

        // Timer setup
        Timer timer = new Timer();
        TimerTask task = new TimerTask() {
            int seconds = 0;

            @Override
            public void run() {
                seconds++;
                System.out.println("Timer: " + seconds + " seconds");
            }
        };

        // Start the timer
        timer.scheduleAtFixedRate(task, 0, 1000);

        try {
            Process process = processBuilder.start();

            // Capture the standard output
            BufferedReader stdOutput = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            System.out.println("Output from Python script:");
            while ((line = stdOutput.readLine()) != null) {
                System.out.println(line);
            }

            // Capture any errors
            BufferedReader stdError = new BufferedReader(new InputStreamReader(process.getErrorStream()));
            System.out.println("Error (if any):");
            while ((line = stdError.readLine()) != null) {
                System.err.println(line);
            }

            // Wait for the process to complete
            int exitCode = process.waitFor();
            System.out.println("Python script exited with code: " + exitCode);

            // Stop the timer after the process is done
            timer.cancel();

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

    }

}
