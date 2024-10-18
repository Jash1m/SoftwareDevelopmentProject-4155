

class student:
        def __init__(self, studentID, studentName, year, majorPreference, sharing ,quietHours, sleep, studyHabits, hobbies, roomClimate, cleanliness, resolutionStyle):
            self.studentID = studentID
            self.studentName = studentName
            self.year = year
            self.majorPreference = majorPreference
            self.sharing = sharing
            self.quietHours = quietHours
            self.sleep = sleep
            self.studyHabits = studyHabits
            self.hobbies = hobbies
            self.roomClimate = roomClimate
            self.cleanliness = cleanliness
            self.resolutionStyle = resolutionStyle

def matchStudent( student1, student2):
    likely = 0
    if(student1.year == student2.year):
        likely += 1
    if(student1.majorPreference == student2.majorPreference):
        likely += 1
    if(student1.sharing == student2.sharing):
        likely += 1
    if(student1.quietHours == student2.quietHours):
        likely += 1
    if(student1.sleep == student2.sleep):
        likely += 1
    if(student1.studyHabits == student2.studyHabits):
        likely += 1
    if(student1.hobbies == student2.hobbies):
        likely += 1
    if(student1.roomClimate == student2.roomClimate):
        likely += 1
    if(student1.cleanliness == student2.cleanliness):
        likely += 1
    if(student1.resolutionStyle == student2.resolutionStyle):
        likely += 1

    if(likely >= 6):
        return student1.studentName + " and " + student2.studentName + " are a match! " + "Compatibility score = " + str(likely)
    else:
        return student1.studentName + " and " + student2.studentName + " are not a match! " + "Compatibility score = " + str(likely)
        





print("Welcome to the roommate compatibility survey")

john = student(800262831,"John", "Junior", "no", 2, "8pm", "After Midnight", "Study Alone", "Art", "Warm", "Tidy", "Confront it")
bobby = student(80087676,"Bobby", "Senior", "yes", 5, "Midnight", "8pm- 10pm", "Study together", "Reading", "Cool", "Messy", "Avoid it")
james = student (8003428, "James", "Senior", "no", 5, "Midnight", "8pm- 10pm", "Study together", "Reading", "Cool", "Tidy", "Confront it")

print(matchStudent(john, bobby))
print(matchStudent(bobby, james))





