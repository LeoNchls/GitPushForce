/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Other/File.java to edit this template
 */

import java.util.ArrayList;
import java.util.TreeMap;

/**
 *
 * @author leoma
 */
public class StudentRegister {

    private ArrayList<Student> students;
    private ArrayList<Course> courses;
    private ArrayList<Attainment> attainments;
    
    // kinda cheating :DDD
    private TreeMap<String, String> course_codes_to_names;
    private TreeMap<String, String> student_ids_to_names;

    public StudentRegister() {
        students = new ArrayList<>();
        courses = new ArrayList<>();
        attainments = new ArrayList<>();
        
        course_codes_to_names = new TreeMap<>();
        student_ids_to_names = new TreeMap<>();
    }
    
    public ArrayList<Student> getStudents() {
        ArrayList<Student> temp_students = new ArrayList<>(students);
        
        temp_students.sort((a, b) -> (a.getName()).compareTo(b.getName()));
        
        return temp_students;
    }
    
    public ArrayList<Course> getCourses() {
        ArrayList<Course> temp_courses = new ArrayList<>(courses);
        
        temp_courses.sort((a, b) -> a.getName().compareTo(b.getName()));
        
        return temp_courses;
    }
    
    public void addStudent(Student student) {
        students.add(student);
        
        student_ids_to_names.put(student.getStudentNumber(), student.getName());
    }
    
    public void addCourse(Course course) {
        courses.add(course);
        
        course_codes_to_names.put(course.getCode(), course.getName());
    }
    
    public void addAttainment(Attainment att) {
        attainments.add(att);
    }
    
    public void printStudentAttainments(String studentNumber, String order) {
        // find if student exists
        Boolean exists = false;
        
        for ( var student : students ) {
            if ( student.getStudentNumber().equals(studentNumber) ) {
                exists = true;
            }
        }
        
        if ( !exists ) {
            System.out.format("Unknown student number: %s", studentNumber);
            System.out.println();
            return;
        }
        
        ArrayList<Attainment> student_attainments = new ArrayList<>();
        
        for ( var attainment : attainments ) {
            if ( attainment.getStudentNumber().equals(studentNumber) ) {
                student_attainments.add(attainment);
            }
        }
        
        // sort attainments
        if ( order.equals("by name") ) {
            student_attainments.sort((a, b) -> course_codes_to_names.get(a.getCourseCode()).compareTo(course_codes_to_names.get(b.getCourseCode())));
        } else if ( order.equals("by code")) {
            student_attainments.sort((a, b) -> a.getCourseCode().compareTo(b.getCourseCode()));
        }
        
        // Print.
        System.out.format("%s (%s)", student_ids_to_names.get(studentNumber), studentNumber);
        System.out.println();
        
        for ( var attainment : student_attainments ) {
            System.out.format("  %s %s: %d", attainment.getCourseCode(), course_codes_to_names.get(attainment.getCourseCode()), attainment.getGrade());
            System.out.println();
        }
    }
    
    public void printStudentAttainments(String studentNumber) {
        printStudentAttainments(studentNumber, "");
    }
}
