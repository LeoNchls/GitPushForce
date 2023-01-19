
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Test for DegreeProgramme
 *
 * @author Leo
 */
public class DegreeProgrammeTest {
    
    public DegreeProgrammeTest() {
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
    public void testConstructor() {
        DegreeProgramme testProgramme = new DegreeProgramme(8, 
                "Test course name", 
                "Test course id", 
                "Test course groupId");
        
        assertTrue(testProgramme.getMaxCredits() == 8);
        assertTrue(testProgramme.getName().equals("Test course name"));
        assertTrue(testProgramme.getId().equals("Test course id"));
        assertTrue(testProgramme.getGroupId().equals("Test course groupId"));
    }
    
}
