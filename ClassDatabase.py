import requests
import re
from bs4 import BeautifulSoup

classNames = ['COMPSCI', 'STATS', 'IN4MATX', 'I&C\xa0SCI', 'MATH']

def courseInformation():
    response = requests.get('http://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/#courseinventory')
    soup = BeautifulSoup(response.text, 'html.parser')
    courseInfo = soup.find_all('div', 'courseblock')
    courseDatabase = dict()

    for i in range(0, 10):
        newCourseInfo = dict()
        courseTitle = courseInfo[i].find('p','courseblocktitle')
        courseDescription = courseInfo[i].find('div', 'courseblockdesc')
        description = list()
        courseTitle = courseTitle.string.split('.')
        courseName = courseTitle[0].split('\xa0')
        print(courseTitle[0])
        for k in range(0, len(courseDescription.contents)):
            if courseDescription.contents[k] != '\n':
                    description.append(courseDescription.contents[k])
                    
        newCourseInfo['Prerequisite'] = set()
        for j in range(0, len(description)):
            prereqList = set()
            if re.findall('Prerequisite', str(description[j])):
                strippedPrereqs = (description[j].text).split('.')
                strippedPrereqs = strippedPrereqs[0].split(':')
                prereq = strippedPrereqs[1].split(' ')
                del prereq[0]
                createPrereqList(prereq)
                
            if re.findall('Restriction', str(description[j])):
                newCourseInfo['Restrictions'] = description[j].string
            newCourseInfo['Name'] = courseTitle[1].strip()
            newCourseInfo['Units'] = re.sub(r'[a-zA-Z]', r'', courseTitle[2].replace(' ', ''))
            newCourseInfo['Description'] = description[0].text
            newCourseInfo['Offered'] = []
            courseDatabase[changeCourseName(courseTitle[0])] = newCourseInfo

    return courseDatabase


def courseOffering():
    response = requests.get('https://www.ics.uci.edu/ugrad/courses/listing.php?year=2019&level=ALL&department=ALL&program=ALL')
    soup = BeautifulSoup(response.text, 'html.parser')
    oddCourse = soup.find_all('tr', 'odd')
    evenCourse = soup.find_all('tr', 'even')
    instruction = soup.find_all('td', 'instruction')
    courseOffering = dict()
    evenCount = 0
    oddCount = 0
    instructionCount = 0
    for i in range(0, len(oddCourse) + len(evenCourse)):
        tempList = list()
        newCount = instructionCount + 4
        for j in range(instructionCount, instructionCount + 4):
                if instruction[j].text != u'\xa0':
                    tempList.append('Yes')
                else:
                    tempList.append('No')
        if i % 2 == 0:
            courseOffering[changeCourseName(oddCourse[oddCount].div.text)] = tempList
            oddCount = oddCount + 1
        else:
            courseOffering[changeCourseName(evenCourse[evenCount].div.text)] = tempList
            evenCount = evenCount + 1
        instructionCount = newCount

    return courseOffering

              
def changeCourseName(courseName):
    courseName = courseName.replace(u'\xa0', u' ')
    splitCourse = re.sub('[()]', r'', courseName).split(' ')
    
    if len(splitCourse) < 2:
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

def createPrereqList(prereqList):
    listOfCourses = list()
    orGrouping = list()
    i = 0
    while i < len(prereqList):
        grouping = ''
        previousElement = ''
        currentElement = prereqList[i]
        if re.search(r'[(]', currentElement) != None:
            if i != 0:
                previousElement = prereqList[i - 1]
            currentGrouping = list()
            currentGrouping.append(currentElement)
            
            while True:
                i = i + 1
                currentElement = prereqList[i]
                currentGrouping.append(changeCourseName(currentElement))
                if re.search(r'[)]', currentElement) != None:
                    break
        
            for elem in currentGrouping:
                if elem == 'or':
                    grouping += '/'
                elif elem == 'and':
                    grouping += '+'
                else:
                    grouping += elem

            print("Grouping: " + grouping)
            print(i)
            if i + 1 < len(prereqList):
                if prereqList[i + 1] == 'and':
                    listOfCourses.append(grouping)
                elif prereqList[i + 1] == 'or':
                    orGrouping.append(grouping)
                    
            elif i + 1 == len(prereqList):
                if previousElement == 'and':
                    listOfCourses.append(grouping)
                elif previousElement == 'or':
                    orGrouping.append(grouping)

        elif currentElement != 'and' and currentElement != 'or':
            listOfCourses.append(changeCourseName(currentElement))
                        
        if len(prereqList) == 0:
            break

        i = i + 1

    optionalCourseListing = ''
    for elem in orGrouping:
        if optionalCourseListing == '':
            optionalCourseListing = elem
        else:
            optionalCourseListing += '/' + elem

    listOfCourses.append(optionalCourseListing)
    print("Prereqs")
    print(listOfCourses)        
            
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


def createDatabase(courseDatabase, coursesOffered):
    undergradCourseDatabase = dict()
    for key in courseDatabase:
        courseDatabase[key]['Offered'] = coursesOffered[key]
        courseNumber = int(re.sub('[a-zA-Z]', '', key))
        if courseNumber < 195:
            undergradCourseDatabase[key] = courseDatabase[key]

    return undergradCourseDatabase


courseDatabase = courseInformation()
'''
coursesOffered = courseOffering()
courseDatabase = checkIfOffered(courseDatabase, coursesOffered)
undergradCourseDatabase = createDatabase(courseDatabase, coursesOffered)

for key in undergradCourseDatabase:
    print(key)
    print(undergradCourseDatabase[key]['Prerequisite'])
'''

    


    
    
