from venv import create
import pandas as pd
from datetime import date
StudentMajor = input('Enter major subject file name format "major.csv"')
GPAList = input('Enter gpalist file name format "GPAList.csv"')
GraduationDates = input(
    'Enter graduation date file name format "GraduationDates.csv"')


def check(df4, df5, df6):
    # Acceptable columns Format
    checkfirst = ['Student id',
                  'first_name',
                  'last_name',
                  'major',
                  'indicator']
    checksecond = ['Student id',
                   'GPA']
    checkthird = ['Student id',
                  'Graduation Date']

    cols = df4.columns.tolist()
    print(cols)
    cols2 = df5.columns.tolist()
    print(cols2)
    cols3 = df6.columns.tolist()
    print(cols3)
    if (cols == checkfirst and cols2 == checksecond and cols3 == checkthird):
        print("file1  file2 and file3 follow the naming convention of columns coded")
        return True
    else:
        print("follow this naming criteria for studentmajorlist file 'Student id'(num),'first_name','last_name','major','indicator'(bool true or false)")
        print(
            "follow this naming criteria for student gpa list file 'Student id'(num),'GPA'")
        print("follow this naming criteria for student graduation date file 'Student id'(num),'Graduation Date'")
        print("one of the files doesn't follow the column naming")
        return False


def a(df4, df5, df6):
    fullrost = df4.merge(df5, on='Student id').merge(df6, on='Student id')
    cols = fullrost.columns.tolist()
    cols = ['Student id',
            'major',
            'first_name',
            'last_name',
            'GPA',
            'Graduation Date',
            'indicator']
    fullrost = fullrost[cols]
    fullrost = fullrost.sort_values('last_name')

    return fullrost


def b(fullrost):
    splits = list(fullrost.groupby("major"))
    for i in range(0, len(splits)):
        name = splits[i][0]
        name = name.replace(" ", "")
        df = pd.DataFrame(splits[i][1])
        df.drop('major', inplace=True, axis=1)
        df.drop('GPA', inplace=True, axis=1)
        df = df.sort_values('Student id')
        print(df)
        df.to_csv("./majorf/{}{}".format(name, '.csv'))


def c(fullrost):
    eligible = fullrost[fullrost.GPA > 3.8]

    today = date.today()
    d3 = today.strftime("%m/%d/%y")
    eligible = eligible[eligible['indicator'] == False]
    eligible = eligible[eligible['Graduation Date'] <= d3]
    eligible.drop('indicator', inplace=True, axis=1)
    eligible.drop('Graduation Date', inplace=True, axis=1)
    eligible = eligible.sort_values('GPA', ascending=False)
    eligible.to_csv("{}".format('ScholarshipCandidates.csv'))
    return eligible


def d(fullrost):
    disciplined = fullrost[fullrost['indicator'] == False]
    disciplined.drop('indicator', inplace=True, axis=1)
    disciplined.drop('major', inplace=True, axis=1)
    disciplined.drop('GPA', inplace=True, axis=1)
    disciplined = disciplined.sort_values('Graduation Date')
    disciplined.to_csv("{}".format('DisciplinedStudents.csv'))
    return disciplined


try:

    df4 = pd.read_csv(StudentMajor)
    df4.drop('Unnamed: 0', inplace=True, axis=1)
    df4.to_csv("file1.csv")

    df5 = pd.read_csv(GPAList)
    df5.drop('Unnamed: 0', inplace=True, axis=1)
    df5.to_csv("file2.csv")

    df6 = pd.read_csv(GraduationDates)
    df6.drop('Unnamed: 0', inplace=True, axis=1)
    df6.to_csv("file3.csv")
    types = "Y"
    if(check(df4, df5, df6)):
        while(types == "Y"):
            option = input(""" \n * Press 1 to output and generate full roster
                        \n * Press 2 to Generate all list per majors 
                        \n * Press 3 to Generate scholarship eligible candidates list and view
                        \n * Press 4 to Generate Desciplined Student list and view 
                        \n * Press X to exit Y to perform other action
                        """)
            df = a(df4, df5, df6)
            if(option == '1'):
                df.to_csv("FullRoster.csv")
                print(df)
            elif(option == '2'):
                b(df)
            elif(option == '3'):
                ctask = c(df)
                print("Eligible student for scholarship ")
                print(ctask)
            elif(option == '4'):
                dtask = d(df)
                print("Desciplined students")
                print(dtask)
            elif(option == 'X' or option == 'x'):
                quit()
except:
    print("file not found")
