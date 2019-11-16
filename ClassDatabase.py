import requests
import re
from bs4 import BeautifulSoup

classNames = ['COMPSCI', 'STATS', 'IN4MATX', 'I&C\xa0SCI', 'MATH']

#Parses the department website to get information about all the courses offered
def courseInformation():
    response = requests.get('http://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/#courseinventory')
    soup = BeautifulSoup(response.text, 'html.parser')
    #Makes a list of all the courses
    courseInfo = soup.find_all('div', 'courseblock')
    courseDatabase = dict()

    #Parses each element to get information about the class
    for i in range(0, len(courseInfo)):
        newCourseInfo = dict()
        #Gets the title of the course
        courseTitle = courseInfo[i].find('p','courseblocktitle')
        courseTitle = courseTitle.string.split('.')
        courseName = courseTitle[0].split('\xa0')
        #Gets the descriptions of the course
        courseDescription = courseInfo[i].find('div', 'courseblockdesc')
        description = list()
        #Separates the descriptions
        for k in range(0, len(courseDescription.contents)):
            if courseDescription.contents[k] != '\n':
                    description.append(courseDescription.contents[k])
                    

        for j in range(0, len(description)):

            #Gets the prerequistes of the course
            prereqList = list()
            if re.findall('Prerequisite', str(description[j])):
                strippedPrereqs = (description[j].text).split('.')
                strippedPrereqs = strippedPrereqs[0].split(':')
                prereq = strippedPrereqs[1].split(' ')
                print(courseTitle[0])
                del prereq[0]
                newCourseInfo['Prerequisite'] = createPrereqList(prereq)

            #Checks for Restrictions on the course
            if re.findall('Restriction', str(description[j])):
                newCourseInfo['Restrictions'] = description[j].string
            else:
                newCourseInfo['Restrictions'] = ""
            #Places data in the database
            newCourseInfo['Name'] = courseTitle[1].strip()
            newCourseInfo['Units'] = re.sub(r'[a-zA-Z]', r'', courseTitle[2].replace(' ', ''))
            newCourseInfo['Description'] = description[0].text
            newCourseInfo['Offered'] = []
            courseDatabase[changeCourseName(courseTitle[0])] = newCourseInfo

    return courseDatabase

#Parses the academic year plan to find out when classes are offered for the current year
def courseOffering():
    response = requests.get('https://www.ics.uci.edu/ugrad/courses/listing.php?year=2019&level=ALL&department=ALL&program=ALL')
    soup = BeautifulSoup(response.text, 'html.parser')
    #Courses in the table are separated into even and odd courses. Creates a list of even course and a list of odd courses
    oddCourse = soup.find_all('tr', 'odd')
    evenCourse = soup.find_all('tr', 'even')
    #Creates a list of the cells(quarters) for all classes
    instruction = soup.find_all('td', 'instruction')
    courseOffering = dict()
    evenCount = 0
    oddCount = 0
    instructionCount = 0
    #Creates a database of when each course if offered
    for i in range(0, len(oddCourse) + len(evenCourse)):
        offeredList = list()
        newCount = instructionCount + 4
        #Iterates through 4 elements in the instruction list to check when a class is offered
        for j in range(instructionCount, instructionCount + 4):
                if instruction[j].text != u'\xa0':
                    if instruction[j].find_all('a'):
                        instructors = ''
                        for elem in instruction[j].find_all('a'):
                            if instructors == '':
                                instructors = elem.text
                            else:
                                instructors += '/' + elem.text
                    offeredList.append(instruction[j].a.text)
                else:
                    offeredList.append('No')
        #If i is even, then get the current course from the odd courses. Update the odd counter.
        #Else, the get the current course from the even courses. Update the even counter.
        if i % 2 == 0:
            courseOffering[changeCourseName(oddCourse[oddCount].div.text)] = offeredList
            oddCount = oddCount + 1
        else:
            courseOffering[changeCourseName(evenCourse[evenCount].div.text)] = offeredList
            evenCount = evenCount + 1
        instructionCount = newCount

    return courseOffering

#Changes the course name to match a set standard.
def changeCourseName(courseName):
    courseName = (courseName.replace(u'\xa0', u' ')).rstrip()
    splitCourse = re.sub('[()]', r'', courseName).split(' ')
    
    if len(splitCourse) < 2:
        courseName = re.sub('[()]', r'', courseName)
        return courseName
    
    if splitCourse[0] == 'COMPSCI':
        splitCourse[0] = 'CS'
    elif splitCourse[0] == 'I&C':
        splitCourse[0] = 'ICS'
        courseName = splitCourse[0] + ' ' + splitCourse[2].lstrip('0')
        return courseName
    elif splitCourse[0] == 'IN4MATX':
        splitCourse[0] = 'INF'
    elif splitCourse[0] == 'SWE':
        splitCourse[0] = 'SE'
    
    courseName = splitCourse[0] + ' ' + splitCourse[1].lstrip('0')
    return courseName.strip('\n')

#Creates a list of prereqs
def createPrereqList(prereqList):
    course = ''
    optionalCourseListing = ''
    listOfCourses = list()
    orGrouping = list()
    i = 0

    #Handles empty Prereq list
    if len(prereqList) == 0:
        return None
    
    while i < len(prereqList):
        grouping = ''
        conditional = ''
        previousElement = ''
        currentElement = prereqList[i]
        if i != 0:
                previousElement = prereqList[i - 1]
        #Checks for nested courses
        if re.search(r'[(]', currentElement) != None:
            
            currentGrouping = list()
            currentGrouping.append(currentElement)
            
            #Creates a grouping for the nested courses(In parantheses)
            while True:
                i = i + 1
                currentElement = prereqList[i]
                currentGrouping.append(currentElement)
                if re.search(r'[)]', currentElement) != None:
                    break

            #Concatenate the elements in the grouping together
            for elem in currentGrouping:
                print(elem)
                if elem == 'or':
                    grouping += '/'
                elif elem == 'and':
                    grouping += '+'
                else:
                    grouping += changeCourseName(elem)


            #Checks next element outside the grouping to determine where to add the element
            if i + 1 < len(prereqList):
                if prereqList[i + 1] == 'and':
                    listOfCourses.append(grouping)
                elif prereqList[i + 1] == 'or':
                    orGrouping.append(grouping)
            #Case where the grouping is at the end of the prereqList
            elif i + 1 == len(prereqList):
                if previousElement == 'and':
                    listOfCourses.append(grouping)
                elif previousElement == 'or':
                    orGrouping.append(grouping)

        #Appends course to prereqList
        elif currentElement != 'and' and currentElement != 'or':
            validCourse = False
            courseSplit = currentElement.split('\xa0')
            for elem in classNames:
                if courseSplit[0] in elem:
                    validCourse = True
                    course = changeCourseName(currentElement)
                    break
            #Handles case where the class does not have a link attached to it
            #EX: CSE 45C
            if validCourse == False:
                if i + 1 < len(prereqList) and re.search(r'[0-9]', prereqList[i + 1]) != None:
                    course = currentElement + ' ' + prereqList[i + 1]

        if previousElement == 'and':
            conditional = 'and'
        elif previousElement == 'or':
            conditional = 'or'

        if i == 0 and re.search(r'[(]', currentElement) == None:
            nextElement = ''
            if i + 1 < len(prereqList):
                nextElement = prereqList[i + 1]
                if i + 2 < len(prereqList) and (nextElement != 'and' or nextElement != 'or'):
                    nextElement = prereqList[i + 1]

            if nextElement == 'and':
                conditional = 'and'
            elif nextElement == 'or':
                conditional = 'or'

        if conditional == 'and':
            listOfCourses.append(course)
        elif conditional == 'or':
            orGrouping.append(course)

        if len(prereqList) == 1:
            listOfCourses.append(course)

        i = i + 1

    #Creates string to add to the prereqList

    for elem in orGrouping:
        if optionalCourseListing == '':
            optionalCourseListing = elem
        else:
            optionalCourseListing += '/' + elem
            
    if optionalCourseListing != '':
        listOfCourses.append(optionalCourseListing)
        
    for elem in listOfCourses:
        elem = changeCourseName(elem)

    return listOfCourses

#Combines the data from the two different websites and returns a single database          
def checkIfOffered(courseDatabase, coursesOffered):
    listOfClasses = list()
    listOfClassesNotOffered = list()
    for key in coursesOffered:
        listOfClasses.append(key)
    for key in courseDatabase:
        if key not in listOfClasses:
            listOfClassesNotOffered.append(key)

    for elem in listOfClassesNotOffered:
        del courseDatabase[elem]

    return courseDatabase

#Creates the actual database for undergraduate classes.
def createDatabase(courseDatabase, coursesOffered):
    undergradCourseDatabase = dict()
    for key in courseDatabase:
        courseDatabase[key]['Offered'] = coursesOffered[key]
        courseNumber = int(re.sub('[a-zA-Z]', '', key))
        if courseNumber < 195:
            undergradCourseDatabase[key] = courseDatabase[key]

    return undergradCourseDatabase

print('Gathering Info')
courseDatabase = courseInformation()

print('Gathering Offering')
coursesOffered = courseOffering()
print('Checking if Offered')
courseDatabase = checkIfOffered(courseDatabase, coursesOffered)
print('Creating undergrad database')
undergradCourseDatabase = createDatabase(courseDatabase, coursesOffered)
print('Printing info')
for key in undergradCourseDatabase:
    print(key)
    '''
    print(undergradCourseDatabase[key]['Name'])
    print(undergradCourseDatabase[key]['Units'])
    print(undergradCourseDatabase[key]['Description'])
    print(undergradCourseDatabase[key]['Offered'])
    '''
    if 'Prerequisite' in undergradCourseDatabase[key]:
        print(undergradCourseDatabase[key]['Prerequisite'])