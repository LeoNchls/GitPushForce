
/**
 * Interface for mapping groupIds to Module and CourseUnit JSON data
 *
 * @author Leo
 */
public interface JsonStringFetcher {
    /**
     * Get a JSON string with the same format as Modules in SISU
     * @param groupId groupId of the module
     * @return JSON string of Module
     */
    public String getModule(String groupId);
    /**
     * Get a JSON string with the same format as CourseUnits in SISU
     * @param groupId groupId of the CourseUnit
     * @return JSON string of CourseUnit
     */
    public String getCourseUnit(String groupId);
}
