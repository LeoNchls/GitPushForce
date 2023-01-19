
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

/**
 * JsonStringFetcher for the JSON files under the directory JSON.
 * 
 * @author Leo
 */
public class LocalJsonFetcher implements JsonStringFetcher {

    @Override
    public String getModule(String groupId) {
        try {
            return getFromLocation("../json/modules/" + groupId + ".json");
        } catch (FileNotFoundException e) {
            System.err.format("Module file not found: " + groupId + "\n");
            return getModule("module-not-found");
        } catch (IOException e) {
            System.err.format("error in Module file: " + groupId + "\n");
        }
        return null;
    }

    @Override
    public String getCourseUnit(String groupId) {
        try {
            return getFromLocation("../json/courseunits/" + groupId + ".json");
        } catch (FileNotFoundException e) {
            System.err.format("CourseUnit file not found: " + groupId + "\n");
            return getCourseUnit("course-unit-not-found");
        } catch (IOException e) {
            System.err.format("error in CourseUnit file: " + groupId + "\n");
        }
        return null;
    }
    
    private String getFromLocation(String fileLocation) throws FileNotFoundException, IOException {
        BufferedReader br;
        String jsonString = "";
        br = new BufferedReader(new FileReader(fileLocation));
        
        // Read lines into jsonString
        String line = br.readLine();
        while (line != null) {
            jsonString += line;
            line = br.readLine();
        }
        
        return jsonString;
    }
}
