/*
File: nonvirtual_diamond.cpp
Author: Adam Edwards
Date: 2026-11-01
Purpose: Part 1 of Assignment 07 (oo-comparison). Builds the Person / Student /
         Employee / TeachingAssistant diamond with ordinary (nonvirtual) public
         inheritance to show that a TeachingAssistant holds two separate Person
         subobjects.
Template: Class hierarchy, example data, static_cast lines, and the two invalid
          expressions come from the Assignment 07 handout.
AI Help: Claude (Anthropic) drafted this program and its comments.
*/

#include <iostream>
#include <string>

class Person {
public:
    /* Public on purpose so the two copies are easy to inspect */
    std::string name;

    Person(const std::string& person_name) : name(person_name) {
        std::cout << "Person constructor\n";
    }
};

class Student : public Person {
public:
    std::string major;

    Student(const std::string& person_name, const std::string& student_major)
        : Person(person_name), major(student_major) {
        std::cout << "Student constructor\n";
    }
};

class Employee : public Person {
public:
    int employee_id;

    Employee(const std::string& person_name, int id)
        : Person(person_name), employee_id(id) {
        std::cout << "Employee constructor\n";
    }
};

class TeachingAssistant : public Student, public Employee {
public:
    std::string course;

    /* Each base gets its own copy of the name, so Person is built twice */
    TeachingAssistant(const std::string& person_name, const std::string& student_major,
        int id, const std::string& ta_course)
        : Student(person_name, student_major), Employee(person_name, id), course(ta_course) {
        std::cout << "TeachingAssistant constructor\n";
    }
};

int main() {
    /* Experiment 1: construct one TeachingAssistant */
    std::cout << "Constructing the TeachingAssistant:\n";
    TeachingAssistant ta("Alex Rivera", "Computer Science", 1042, "CS 240");

    /* Experiment 2: get a reference to each Person subobject */
    Person& student_person = static_cast<Student&>(ta);
    Person& employee_person = static_cast<Employee&>(ta);

    /* Experiment 3: print each subobject's address and name */
    std::cout << "\nBefore the name change:\n";
    std::cout << "student_person  address: " << &student_person
        << "  name: " << student_person.name << '\n';
    std::cout << "employee_person address: " << &employee_person
        << "  name: " << employee_person.name << '\n';

    /* Experiment 4: change the name through student_person only */
    student_person.name = "Alexandra Rivera";

    std::cout << "\nAfter changing the name through student_person:\n";
    std::cout << "student_person  name: " << student_person.name << '\n';
    std::cout << "employee_person name: " << employee_person.name << '\n';

    /* Experiment 5: both lines are rejected because ta has two Person subobjects.
       Uncomment one at a time to see the compiler diagnostic. */

       /* Error: ambiguous, the compiler can't tell which Person's name is meant */
       // std::cout << ta.name << '\n';

       /* Error: ambiguous, there are two Person subobjects the pointer could point to */
       // Person* person = &ta;

    return 0;
}