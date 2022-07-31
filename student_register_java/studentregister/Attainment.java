/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Other/File.java to edit this template
 */

/**
 *
 * @author leoma
 */
public class Attainment {

    private String course_id;
    private String student_id;
    private int grade_achieved;
    
    public Attainment(String courseCode, String studentNumber, int grade) {
        course_id = courseCode;
        student_id = studentNumber;
        grade_achieved = grade;
    }
    
    public String getCourseCode() {
        return course_id;
    }
    
    public String getStudentNumber() {
        return student_id;
    }
    
    public int getGrade() {
        return grade_achieved;
    }
}
