/*
File: virtual_diamond.cpp
Author: Adam Edwards
Date: 2026-11-01
Purpose: Parts 2 and 4 (C++) of Assignment 07 (oo-comparison). Builds the
         Person / Student / Employee / TeachingAssistant diamond with virtual
         inheritance so a TeachingAssistant holds one shared Person subobject,
         tests virtual role() dispatch, and compares inheritance-based
         polymorphism with a template on an unrelated RobotAssistant type.
Template: Class hierarchy, example data, virtual base syntax, role() interface,
          and the announce_person / announce_generic functions come from the
          Assignment 07 handout.
AI Help: Claude (Anthropic) drafted this program and its comments.
*/

#include <iostream>
#include <string>

class Person {
public:
    std::string name;

    /* No default constructor, so every Person must be given a name */
    Person(const std::string& person_name) : name(person_name) {
        std::cout << "Person constructor\n";
    }

    virtual std::string role() const {
        return "Person";
    }

    virtual ~Person() = default;
};

class Student : virtual public Person {
public:
    std::string major;

    /* Person(person_name) is skipped when Student is part of a TeachingAssistant,
       because the most-derived class builds the shared virtual base */
    Student(const std::string& person_name, const std::string& student_major)
        : Person(person_name), major(student_major) {
        std::cout << "Student constructor\n";
    }

    std::string role() const override {
        return "Student";
    }
};

class Employee : virtual public Person {
public:
    int employee_id;

    Employee(const std::string& person_name, int id)
        : Person(person_name), employee_id(id) {
        std::cout << "Employee constructor\n";
    }

    std::string role() const override {
        return "Employee";
    }
};

class TeachingAssistant : public Student, public Employee {
public:
    std::string course;

    /* The most-derived class must initialize the virtual base Person itself */
    TeachingAssistant(const std::string& person_name, const std::string& student_major,
        int id, const std::string& ta_course)
        : Person(person_name), Student(person_name, student_major),
        Employee(person_name, id), course(ta_course) {
        std::cout << "TeachingAssistant constructor\n";
    }

    /* Required: Student and Employee both override role(), so without this
       there is no single final overrider. Comment out to see the error. */
    std::string role() const override {
        return "Teaching Assistant";
    }
};

/* Part 4: unrelated type with a role() method, not derived from Person */
class RobotAssistant {
public:
    std::string role() const {
        return "Robot Assistant";
    }
};

/* Only accepts types derived from Person; uses virtual dispatch at run time */
void announce_person(const Person& person) {
    std::cout << person.role() << '\n';
}

/* Accepts any type that has role(); checked when the template is instantiated */
template<typename T>
void announce_generic(const T& value) {
    std::cout << value.role() << '\n';
}

int main() {
    /* Construct one TeachingAssistant */
    std::cout << "Constructing the TeachingAssistant:\n";
    TeachingAssistant ta("Alex Rivera", "Computer Science", 1042, "CS 240");

    /* Same experiments as Part 1 */
    Person& student_person = static_cast<Student&>(ta);
    Person& employee_person = static_cast<Employee&>(ta);

    std::cout << "\nBefore the name change:\n";
    std::cout << "student_person  address: " << &student_person
        << "  name: " << student_person.name << '\n';
    std::cout << "employee_person address: " << &employee_person
        << "  name: " << employee_person.name << '\n';

    student_person.name = "Alexandra Rivera";

    std::cout << "\nAfter changing the name through student_person:\n";
    std::cout << "student_person  name: " << student_person.name << '\n';
    std::cout << "employee_person name: " << employee_person.name << '\n';

    /* The two expressions rejected in Part 1 now compile: there is only one Person */
    std::cout << "\nExpressions rejected in Part 1:\n";
    std::cout << "ta.name: " << ta.name << '\n';
    Person* person = &ta;
    std::cout << "Person* person = &ta  address: " << person
        << "  name: " << person->name << '\n';

    /* Virtual dispatch through a Person& that refers to the TeachingAssistant */
    std::cout << "\nVirtual role() through Person&:\n";
    Person& person_ref = ta;
    std::cout << "person_ref.role(): " << person_ref.role() << '\n';

    /* Part 4: polymorphism without common ancestry */
    RobotAssistant robot;

    std::cout << "\nPart 4 - announce_person:\n";
    announce_person(ta);
    /* Error: RobotAssistant is not a Person, so it can't bind to const Person& */
    // announce_person(robot);

    std::cout << "\nPart 4 - announce_generic:\n";
    announce_generic(ta);
    announce_generic(robot);

    return 0;
}