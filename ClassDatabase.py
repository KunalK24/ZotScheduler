import requests
import re
from bs4 import BeautifulSoup

classNames = ['COMPSCI', 'STATS', 'IN4MATX', 'I&C\xa0SCI', 'MATH']

'''
    These functions are for gathering data and storing in a database
    TODO: Store data in DynamoDB
          Get specialization information
          Get GE information
'''
def courseInformation():
    '''
        Description:
            Parses the department website to get information about all the courses offered.

        Args:
            None

        Return:
            Dictionary of courses
            {
                'ICS 31' : {
                    'Name' : 'Introduction to Programming',
                    'Units' : 4,
                    'Description' : 'Introduction to fundamental concepts and...',
                    'Offered' : list(),
                    'Prerequisite' : ['ICS 21']
                    'Resctriction' : 'School of Info & Computer Sci students...',
                }
            }
                    
    '''
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
        number = int(re.sub(r'[a-zA-Z]', '', courseName[len(courseName) - 1]))
        if number < 195:
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
                    if re.findall('Corequisite', str(description[j])):
                        strippedPrereqs = (description[j].text).split('.')
                        strippedPrereqs = strippedPrereqs[0].split(':')
                        prereq = strippedPrereqs[len(strippedPrereqs) - 1].split(' ')
                        del prereq[0]
                        newCourseInfo['Prerequisite'] = createPrereqList(prereq)
                    else:   
                        strippedPrereqs = (description[j].text).split('.')
                        strippedPrereqs = strippedPrereqs[0].split(':')
                        prereq = strippedPrereqs[1].split(' ')
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


def courseOffering():
    '''
        Description:
            Parses the academic year plan website and returns a database of when courses are offered.

        Args:
            None

        Return:
            Dictionary of course offerings
            {
                'CS 141' : ['Raymond O. Klefstad', 'Raymond O. Klefstad', 'Not Offered']
            }
                    
    '''
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
                    offeredList.append('Not Offered')
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


def categorizeCourses():
    '''
        TODO: Parse page to get specialization
        TODO: Store info into a list (could be required for multiple specialization)
    '''
    response = requests.get('http://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/departmentofcomputerscience/#majorstext')
    soup = BeautifulSoup(response.text, 'html.parser')
    
    

def changeCourseName(courseName):
    '''
        Description:
            Changes course name to match a standard naming convention. Removes all extra characters

        Args:
            Name of the course (CompSci 161)

        Return:
            Name of the course after removing characters and changing department name
            CompSci 161 ----> CS 161
                    
    '''
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

def handleSpecialCases(courseDatabase):
    '''
        Description:
            Adds courses that are not offered by Donald Bren School to the database.

        Args:
            Course database

        Return:
            Dictionary of courses (With added courses)
            {
                'Math 2B' : {
                    'Name' : 'Math 2B',
                    'Units' : 4,
                    'Description' : '',
                    'Offered' : ['Offered', 'Offered', 'Offered'],
                    'Prerequisite' : ['Math 2A']
                    'Resctriction' : '',
                }
            }

        TODO: Gather info from catalogue
                    
    '''
    #Add final course in the writing series to the prerequisites of uppder division writing course
    courseDatabase['ICS 139W']['Prerequisite'] = ['WRITING 39C']
    #Lists of courses required by students not offered through the Donald Bren School
    writingCourses = ['WRITING 39A', 'WRITING 39B', 'WRITING 39C']
    mathCourses = ['MATH 2A', 'MATH 2B']
    #Courses are offered all quarters
    offeredAllQuarters = ['Offered'] * 3
    #Works on the writing courses
    for i in range(0, len(writingCourses)):
        courseDatabase[writingCourses[i]] = dict()
        #Temp fix for now(Gather Info later from search catalogue)
        courseDatabase[writingCourses[i]]['Name'] = writingCourses[i]
        courseDatabase[writingCourses[i]]['Offered'] = offeredAllQuarters
        courseDatabase[writingCourses[i]]['Units'] = 4
        if i == 0:
            courseDatabase[writingCourses[i]]['Prerequisite'] = []
        else:
            courseDatabase[writingCourses[i]]['Prerequisite'] = [writingCourses[i - 1]]
            
    #Works on the math courses
    for i in range(0, len(mathCourses)):
        #Temp fix for now(Gather Info later from search catalogue)
        courseDatabase[mathCourses[i]] = dict()
        courseDatabase[mathCourses[i]]['Name'] = mathCourses[i]
        courseDatabase[mathCourses[i]]['Offered'] = offeredAllQuarters
        courseDatabase[mathCourses[i]]['Units'] = 4
        if i == 0:
            courseDatabase[mathCourses[i]]['Prerequisite'] = []
        else:
            courseDatabase[mathCourses[i]]['Prerequisite'] = [mathCourses[i - 1]]

    return courseDatabase


def createPrereqList(prereqList):
    '''
        Description:
            Creates prerequisite list for classes

        Args:
            List of courses (Included paratheses for creating groupings

        Return:
            List of prerequisites for a class
            Prerequisites for CS 141 = ['ICS 51/CSE 31', 'ICS 46/CSE 46']

        TODO: Simplify this function and use recursion to handle nested groupings
                    
    '''
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

          
def checkIfOffered(courseDatabase, coursesOffered):
    '''
        Description:
            Checks if a course is offered by the Donald Bren School.
            Adds when a course is offered to the database.

        Args:
            Course database, Offered course database

        Return:
            Dictionary of courses
            {
                'ICS 31' : {
                    'Name' : 'Introduction to Programming',
                    'Units' : 4,
                    'Description' : 'Introduction to fundamental concepts and...',
                    'Offered' : ['Shannon Alfaro', '...', '...'],
                    'Prerequisite' : ['ICS 21']
                    'Resctriction' : 'School of Info & Computer Sci students...',
                }
            }
                    
    '''
    listOfClasses = list()
    listOfClassesNotOffered = list()
    for key in coursesOffered:
        listOfClasses.append(key)
    for key in courseDatabase:
        if key not in listOfClasses:
            listOfClassesNotOffered.append(key)
        else:
            courseDatabase[key]['Offered'] = coursesOffered[key]

    for elem in listOfClassesNotOffered:
        del courseDatabase[elem]

    return courseDatabase

'''
    These functions will be on the backend of the website.
    TODO: Need to convert all functions to JS.
'''

def createScoredDatabase(courseDatabase):
    '''
        Description:
            Creates a scored database based on what courses a person wants to take.

        Args:
            Course database

        Return:
            Dictionary of courses
            {
                'ICS 32' : {
                    'Score' : 26
                    'Prerequisite' : {'ICS 31'}
                    'PrereqOf' : {ICS 33', ...}
                    'Offered' : ['Kimberly A Hermans', ...]
                    'Units' : 4
                }
            }

        TODO: Eventually will take in the required and planned courses as arguments instead of hardcoded
                    
    '''
    requiredCourses = ['ICS 31', 'ICS 32', 'ICS 33', 'ICS 45C', 'ICS 46', 'ICS 51',
                       'ICS 53', 'ICS 53L', 'ICS 90', 'INF 43', 'ICS 6B', 'ICS 6D',
                       'ICS 6N', 'STATS 67', 'CS 161', 'ICS 139W', 'WRITING 39A', 'WRITING 39B',
                       'WRITING 39C', 'MATH 2A', 'MATH 2B']
    plannedCourses = ['CS 171', 'CS 178', 'CS 165', 'CS 167', 'CS 143B', 'CS 125', 'CS 143A',
                      'CS 121', 'CS 122A', 'INF 121', 'CS 132']

    courseScores = dict()
    for elem in requiredCourses:
        courseData = dict()
        courseData['Score'] = 3
        if 'Prerequisite' in courseDatabase[elem]:
            courseData['Prerequisite'] = set(courseDatabase[elem]['Prerequisite'])
        else:
            courseData['Prerequisite'] = set()
        courseData['PrereqOf'] = set()
        courseData['Offered'] = courseDatabase[elem]['Offered']
        courseData['Units'] = courseDatabase[elem]['Units']
        courseScores[elem] = courseData

    for elem in plannedCourses:
        courseData = dict()
        courseData['Score'] = 1
        courseData['Prerequisite'] = set(courseDatabase[elem]['Prerequisite'])
        courseData['PrereqOf'] = set()
        courseData['Offered'] = courseDatabase[elem]['Offered']
        courseData['Units'] = courseDatabase[elem]['Units']
        courseScores[elem] = courseData

    for course in courseScores:
        removeEmpty = set()
        if 'Prerequisite' in courseScores[course]:
            for prereq in courseScores[course]['Prerequisite']:
                if prereq != '' and prereq != ' ':
                    removeEmpty.add(prereq)
            courseScores[course]['Prerequisite'] = removeEmpty
            for prereq in courseScores[course]['Prerequisite']:
                if re.search(r'/', prereq) != None:
                    prereqList = prereq.split('/')
                    for elem in prereqList:
                        if elem in courseScores:
                            courseScores[elem]['PrereqOf'].add(course)
                else:
                    if prereq in courseScores:
                        courseScores[prereq]['PrereqOf'].add(course)

    rootCourses = list()
    for course in courseScores:
        if len(courseScores[course]['Prerequisite']) == 0 and len(courseScores[course]['PrereqOf']) != 0:
            rootCourses.append(course)

    for root in rootCourses:
        courseScores[root]['Score'] += findLeaves(root, courseScores)
    
    return courseScores


def createPriorityQueue(scoredDatabase):
    priorityQueue = list()
    for course in scoredDatabase:
        courseTuple = (course, scoredDatabase[course]['Score'])
        priorityQueue.append(courseTuple)

    print(sorted(priorityQueue, key=lambda x:x[1], reverse=True))
    return(sorted(priorityQueue, key=lambda x:x[1], reverse=True))

    
def findLeaves(start, courseScores):
    if len(courseScores[start]['PrereqOf']) != 0:
        for course in courseScores[start]['PrereqOf']:
            courseScores[start]['Score'] += findLeaves(course, courseScores)

    return courseScores[start]['Score']

'''
    TODO: Look over the logic of this function and see if we can simplify it.
'''
def createSchedule(priorityQueue, scoredDatabase): 
    maxNumberOfUnits = 16
    maxNumberOfQuarters = 12
    numOfQuarters = 0
    year = 0
    courseSchedule = dict()
    takenCourses = []
    quarters = {
        0: 'Fall',
        1: 'Winter',
        2: 'Spring',
    }
    yearName = {
        0: 'Freshman',
        1: 'Sophomore',
        2: 'Junior',
        3: 'Senior',
    }
    
    for i in range(0, 4):
        currentYear = i
        courseSchedule[yearName[currentYear]] = dict()
        
    for i in range(0, maxNumberOfQuarters):
        quarter = i % 3
        if numOfQuarters % 3 == 0 and numOfQuarters != 0:
            year += 1
        units = 0
        schedule = list()
        remove = list()
        if numOfQuarters == 0:
            schedule.append('ICS 90')
            remove.append(('ICS 90', 3))
        for i in range(0, len(priorityQueue)):
            courseTuple = priorityQueue[i]
            offered = scoredDatabase[courseTuple[0]]['Offered']
            if offered[quarter] != 'Not Offered' and courseTuple[0] not in takenCourses:
                prereqsCompleted = 0
                prereqList = scoredDatabase[courseTuple[0]]['Prerequisite']
                prereqsDone = False
                for prereq in prereqList:
                    if re.search(r'/', prereq) != None:
                        optionalPrereqs = prereq.split('/')
                        for course in optionalPrereqs:
                            if course in takenCourses:
                                prereqsCompleted += 1
                    else:
                        if prereq in takenCourses:
                            prereqsCompleted += 1
                            
                if prereqsCompleted == len(prereqList):
                    prereqsDone = True
                    
                if prereqsDone:
                    units += int(scoredDatabase[courseTuple[0]]['Units'])
                    if units < maxNumberOfUnits:
                        print('Appending: ', courseTuple[0])
                        schedule.append(courseTuple[0])
                        remove.append(courseTuple)
                    else:
                        units = 0
                        break

        for course in remove:
            takenCourses.append(course[0])
            priorityQueue.pop(priorityQueue.index(course))
            
        numOfQuarters += 1
        courseSchedule[yearName[year]][quarters[quarter % 3]] = schedule

    print(courseSchedule)
    if len(priorityQueue) != 0:
        for elem in priorityQueue:
            print('Could not take: ', elem[0])
            for course in scoredDatabase[elem[0]]['Prerequisite']:
                if re.search(r'/', course):
                    prereqList = course.split('/')
                    for prereq in prereqList:
                        if prereq not in takenCourses:
                            print('Need to take: ', prereq)
                            if prereq != prereqList[len(prereqList) - 1]:
                                print('OR')
                elif course not in takenCourses:
                    print('Need to take: ', course)
                
        

    
print('Gathering Info')
courseDatabase = courseInformation()

print('Gathering Offering')
coursesOffered = courseOffering()
print('Checking if Offered')
courseDatabase = checkIfOffered(courseDatabase, coursesOffered)
print('Handling special cases.')
courseDatabase = handleSpecialCases(courseDatabase)
print('Creating scored database')
scoredDatabase = createScoredDatabase(courseDatabase)
print('Creating priority queue')
priorityQueue = createPriorityQueue(scoredDatabase)
print('FINALLY CREATING THE SCHEDULE')
createSchedule(priorityQueue, scoredDatabase)
  
