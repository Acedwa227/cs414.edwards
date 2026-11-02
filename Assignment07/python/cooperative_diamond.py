# File: cooperative_diamond.py
# Author: Adam Edwards
# Date: 2026-11-01
# Purpose: Parts 3 and 4 (Python) of Assignment 07 (oo-comparison). Builds the
#          Person / Student / Employee / TeachingAssistant diamond with
#          cooperative multiple inheritance, inspects the MRO and instance
#          state, tests role() lookup, and uses duck typing with an unrelated
#          RobotAssistant and an integer.
# Template: Class hierarchy, cooperative __init__ pattern, constructor call,
#           ReversedTeachingAssistant, and announce() come from the Assignment 07
#           handout.
# AI Help: Claude (Anthropic) drafted this program and its comments.


class Person:
    def __init__(self, *, name, **kwargs):
        print(f"Entering Person.__init__             id(self) = {id(self)}")
        self.name = name
        # Continue to the next class in the MRO (object); no arguments should remain
        super().__init__(**kwargs)

    def role(self):
        return "Person"


class Student(Person):
    def __init__(self, *, major, **kwargs):
        print(f"Entering Student.__init__            id(self) = {id(self)}")
        self.major = major
        super().__init__(**kwargs)

    def role(self):
        return "Student"

    def set_student_name(self, new_name):
        self.name = new_name


class Employee(Person):
    def __init__(self, *, employee_id, **kwargs):
        print(f"Entering Employee.__init__           id(self) = {id(self)}")
        self.employee_id = employee_id
        super().__init__(**kwargs)

    def role(self):
        return "Employee"

    def set_employee_name(self, new_name):
        self.name = new_name


class TeachingAssistant(Student, Employee):
    def __init__(self, *, course, **kwargs):
        print(f"Entering TeachingAssistant.__init__  id(self) = {id(self)}")
        self.course = course
        super().__init__(**kwargs)

    # Experiments 4 and 5: comment out role() to see which inherited
    # role() the MRO finds, then restore it
    def role(self):
        return "Teaching Assistant"


# Same bases in the opposite order, with no role() override
class ReversedTeachingAssistant(Employee, Student):
    def __init__(self, *, course, **kwargs):
        print(f"Entering ReversedTeachingAssistant.__init__  id(self) = {id(self)}")
        self.course = course
        super().__init__(**kwargs)


# Part 4: unrelated class with a role() method, not derived from Person
class RobotAssistant:
    def role(self):
        return "Robot Assistant"


def announce(value):
    print(value.role())


def main():
    print("Constructing the TeachingAssistant:")
    ta = TeachingAssistant(
        name="Alex Rivera",
        major="Computer Science",
        employee_id=1042,
        course="CS 240",
    )
    print(f"id(ta) after construction:           {id(ta)}")

    # Experiment 1: method resolution order
    print("\nTeachingAssistant.__mro__:")
    print(TeachingAssistant.__mro__)

    # Experiment 2: instance state after construction
    print("\nvars(ta):")
    print(vars(ta))

    # Experiment 3: both methods write to the same single name attribute
    print("\nName changes:")
    ta.set_student_name("Alexandra Rivera")
    print(f"After set_student_name:  ta.name = {ta.name}")
    ta.set_employee_name("A. Rivera")
    print(f"After set_employee_name: ta.name = {ta.name}")

    # Experiments 4 and 5: role() lookup through the MRO
    print("\nta.role():")
    print(ta.role())

    # Experiment 6: reversed base order changes the MRO and the role() found
    print("\nConstructing the ReversedTeachingAssistant:")
    reversed_ta = ReversedTeachingAssistant(
        name="Alex Rivera",
        major="Computer Science",
        employee_id=1042,
        course="CS 240",
    )
    print("\nReversedTeachingAssistant.__mro__:")
    print(ReversedTeachingAssistant.__mro__)
    print("\nreversed_ta.role():")
    print(reversed_ta.role())

    # Part 4: duck typing, role() is only looked up when announce() runs
    print("\nPart 4 - announce():")
    robot = RobotAssistant()
    announce(ta)
    announce(robot)
    try:
        announce(42)
    except AttributeError as error:
        print(f"AttributeError: {error}")

    print("\nProgram finished normally.")


main()