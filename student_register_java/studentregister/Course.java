/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Other/File.java to edit this template
 */

/**
 *
 * @author leoma
 */
public class Course {

    private String course_code;
    private String course_name;
    private int course_credits;
    
    public Course(String code, String name, int credits) {
        course_code = code;
        course_name = name;
        course_credits = credits;
    }
    
    public String getCode() {
        return course_code;
    }
    
    public String getName() {
        return course_name;
    }
    
    public int getCredits() {
        return course_credits;
    }
}
