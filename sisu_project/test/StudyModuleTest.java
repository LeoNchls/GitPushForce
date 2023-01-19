
import java.util.ArrayList;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 *
 * @author Leo
 */
public class StudyModuleTest {
    
    public StudyModuleTest() {
    }
    
    @BeforeAll
    public static void setUpClass() {
    }
    
    @AfterAll
    public static void tearDownClass() {
    }
    
    @BeforeEach
    public void setUp() {
    }
    
    @AfterEach
    public void tearDown() {
    }

    @Test
    public void testGetters() {
        int maxCredits = 4;
        String name = "test course name";
        String id = "test course id";
        String groupId = "test course groupId";
        ArrayList<String> organizers = new ArrayList<>();
        organizers.add("org");
        organizers.add("ani");
        organizers.add("zer");
        
        StudyModule testModule = new StudyModule(maxCredits, name, id, groupId, organizers);
        
        assertTrue(testModule.getMaxCredits() == 4);
        assertTrue(testModule.getName().equals(name));
        assertTrue(testModule.getGroupId().equals(groupId));
        assertTrue(testModule.getOrganizers().equals(organizers));
    }
    
    @Test
    public void testCompletionStatus() {
        int maxCredits = 4;
        String name = "test course name";
        String id = "test course id";
        String groupId = "test course groupId";
        ArrayList<String> organizers = new ArrayList<>();
        organizers.add("org");
        organizers.add("ani");
        organizers.add("zer");
        
        StudyModule testModule = new StudyModule(maxCredits, name, id, groupId, organizers);
        
        assertTrue(!testModule.isComplete());
        
        testModule.completeModule();
        
        assertTrue(testModule.isComplete());
        
        testModule.cancelModuleCompletion();
        
        assertTrue(!testModule.isComplete());
    }
}
