
import com.google.gson.Gson;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
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
public class CourseUnitReaderTest {
    
    public CourseUnitReaderTest() {
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
    public void testBuildCourseUnit() {
        CourseUnitReader cur = new CourseUnitReader(new UrlJsonFetcher());
        CourseUnit testCU = cur.buildCourseUnit("uta-ykoodi-47926");
        
        assertEquals(testCU.getName(), "Introduction to Analysis");
        assertEquals(testCU.getCode(), "MATH.MA.110");
        assertEquals(testCU.getCourseUnitGroupId(), "uta-ykoodi-47926");
        assertEquals(testCU.getMaxCredits(), 5);
        assertEquals(testCU.getId(), "otm-94ffcfc5-0db4-4507-b475-63f290639e04");
    }
    
    @Test
    public void testAdditionalInfo() {
        CourseUnitReader cur = new CourseUnitReader(new UrlJsonFetcher());
        CourseUnit testCU = cur.buildCourseUnit("uta-ykoodi-47926");
        
        assertTrue(testCU.getOutcome().endsWith(" muuttujan funktioita."));
        assertTrue(testCU.getPrerequisite().endsWith(" kurssit<br /></p>"));
        assertTrue(testCU.getContent().endsWith(" integrointi <br /></p>"));
        assertTrue(testCU.getMaterial().endsWith(" jaettava materiaali.</p>"));
    }
}
