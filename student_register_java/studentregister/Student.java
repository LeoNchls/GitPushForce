/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Other/File.java to edit this template
 */

/**
 *
 * @author leoma
 */
public class Student {
    
    private String student_name;
    private String id;
    
    public Student(String given_name, String studentNumber) {
        student_name = given_name;
        id = studentNumber;
    }
    
    public String getName() {
        return student_name;
    }
    
    public String getStudentNumber() {
        return id;
    }
}
