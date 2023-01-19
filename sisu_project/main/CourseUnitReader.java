
import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.stream.JsonReader;
import java.io.StringReader;
import java.util.TreeMap;

/**
 * Read data from JSON source into CourseUnit object
 * 
 * @author Leo
 */
public class CourseUnitReader {
    // JsonStringFetcher as a source for JSON data
    private JsonStringFetcher jsonSource;
    
    /**
     * Constructor for CourseUnitReader
     * @param jsonSource Source to get JSON data from
     */
    public CourseUnitReader(JsonStringFetcher jsonSource) {
        this.jsonSource = jsonSource;
    }
    
    /**
     * Giving no JSON source leads to the reader using URL SISU
     */
    public CourseUnitReader() {
        this.jsonSource = new UrlJsonFetcher();
    }
    
    /**
     * Get CourseUnit of groupId from SISU
     * @param groupId groupId of CourseUnit to get
     * @return CourseUnit object of groupId
     */
    public CourseUnit buildCourseUnit(String groupId) {
        JsonObject rootElement = getJsonFromSource(groupId);
        
        // names
        String enName = getAttributePrefEn(rootElement, "name");
        
        // code
        String code = "code unavailable";
        JsonElement codeElement = rootElement.get("code");
        if ( !codeElement.isJsonNull() ) {
            code = codeElement.getAsString();
        }
        
        // credits
        int minCredits = getMinMaxCredits(rootElement).get("min");
        int maxCredits = getMinMaxCredits(rootElement).get("max");
        
        // course id
        JsonElement idElement = rootElement.get("id");
        String id = idElement.getAsString();
        
        // initialize result
        CourseUnit result = new CourseUnit(id,groupId,enName,code,minCredits,maxCredits);

        // addtl info
        result.setContent(getAttributePrefEn(rootElement, "content"));
        result.setPrerequisite(getAttributePrefEn(rootElement, "prerequisites"));
        result.setOutcome(getAttributePrefEn(rootElement, "outcomes"));
        result.setMaterial(getAttributePrefEn(rootElement, "learningMaterial"));
        
        return result;
    }
    
    /**
     * Get an English attribute from JsonObject.
     * If English attribute is unavailable, return Finnish attribute.
     * If no attribute is available, return null.
     * @param rootElement Object to get element from
     * @param attName Attribute name
     * @return Attribute value if it exists, else null
     */
    private String getAttributePrefEn(JsonObject rootElement, String attName) {
        String result = null;
        
        if ( rootElement.has(attName) ) {
            if (!rootElement.get(attName).isJsonNull()) {
                JsonObject contentLangObj = rootElement.get(attName).getAsJsonObject();
                if ( contentLangObj.has("en") ) {
                    result = contentLangObj.get("en").getAsString();
                } else {
                    result = contentLangObj.get("fi").getAsString();
                }
            }
        }
        
        return result;
    }
    
    private TreeMap<String, Integer> getMinMaxCredits(JsonObject rootElement) {
        JsonObject creditsObject = rootElement.get("credits").getAsJsonObject();
        JsonElement creditElement = null;
        int maxCredits = 0;
        int minCredits = 0;
        if (creditsObject.has("max")) {
            creditElement = creditsObject.getAsJsonObject().get("max");
            if ( !creditElement.isJsonNull() ) {
                maxCredits = creditElement.getAsInt();
            }
        }   
        if (creditsObject.has("min")) {
            creditElement = creditsObject.getAsJsonObject().get("min");
            if ( !creditElement.isJsonNull() ) {
                minCredits = creditElement.getAsInt();
            }
        } else {
            // if a minimum credits limit hasn't been defined, use max
            minCredits = maxCredits;
        }
        // if min credits was defined and max wasn't, use min as max
        if ( minCredits > maxCredits) {
            maxCredits = minCredits;
        }
        
        TreeMap<String, Integer> result = new TreeMap<>();
        result.put("min", minCredits);
        result.put("max", maxCredits);
        
        return result;
    }
    
    private JsonObject getJsonFromSource(String groupId) {
        Gson gson = new Gson();
        String jsonString = jsonSource.getCourseUnit(groupId);
        JsonReader jreader = new JsonReader(new StringReader(jsonString));
        jreader.setLenient(true);
        return gson.fromJson(jreader, JsonObject.class);
    }
}
