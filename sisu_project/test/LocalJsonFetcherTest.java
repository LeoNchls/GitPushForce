
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
public class LocalJsonFetcherTest {
    
    public LocalJsonFetcherTest() {
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

    /**
     * Test of getModule method, of class LocalJsonFetcher.
     */
    @Test
    public void testGetModule() {
        String groupId = "otm-6b575bfa-e488-4ee0-a8d9-877608ce64e9";
        LocalJsonFetcher ljf = new LocalJsonFetcher();
        
        assertTrue(ljf.getModule(groupId).endsWith("\"curriculumPeriodIds\": []}"));
    }

    /**
     * Test of getCourseUnit method, of class LocalJsonFetcher.
     */
    @Test
    public void testGetCourseUnit() {
        String groupId = "tut-cu-g-35899";
        LocalJsonFetcher ljf = new LocalJsonFetcher();
        
        assertTrue(ljf.getCourseUnit(groupId).endsWith("\"uta-lvv-2023\"    ]}"));
    }
    
}
