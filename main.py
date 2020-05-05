import os
import re
import table as tb

commandDict = {
    "createDB" : "create database",
    "dropDB" : "drop database",
    "use" : "use",
    "createTbl" : "create table",
    "dropTbl" : "drop table",
    "select" : "select",
    "alter" : "alter table",
    "insert" : "insert",
    "update" : "update",
    "delete" : "delete"
}

usingDB = False
currDB = ""

def main():
    print("Please enter commands")

    userInput = ""

    while userInput != ".EXIT":
        userInput = input("")
        splitInput = userInput.split()

        if userInput.lower().find(".exit") != -1:
            print("All done.")
            return

        # In case a user hits enter without entering anything into the prompt
        # then handles cases when commands are split into multiple lines.
        if userInput != "" and userInput[0] != "-":
            while userInput[-1] != ';':
                temp = input("")
                userInput += temp

            # Create database command
            # last word in split input will be the db name
            # run command stripEnd to remove semicolon from end of command
            if commandDict["createDB"] in userInput.lower():
                dbName = splitInput[-1]
                dbName = stripEnd(dbName)
                createDB(dbName)

            elif commandDict["dropDB"] in userInput.lower():
                dbName = splitInput[-1]
                dbName = stripEnd(dbName)
                dropDB(dbName)

            elif commandDict["use"] in userInput.lower():
                dbName = splitInput[-1]
                dbName = stripEnd(dbName)
                useDB(dbName)

            elif commandDict["createTbl"] in userInput.lower():
                createTable(userInput)

            elif commandDict["dropTbl"] in userInput.lower():
                dropTable(userInput)

            elif commandDict["select"] in userInput.lower():
                select(userInput)

            elif commandDict["alter"] in userInput.lower():
                alter(userInput)

            elif commandDict["insert"] in userInput.lower():
                insert(userInput)

            elif commandDict["update"] in userInput.lower():
                update(userInput)

            elif commandDict["delete"] in userInput.lower():
                delete(userInput)





def stripEnd(input):
    input = input[0:-1]
    return input

def createDB(dbName):
    path = os.getcwd() + "//" + dbName

    if os.path.isdir(path):
        print("!Failed to create database " + dbName + " because it already exists.")

    else:
        os.mkdir(path)
        print("Database " + dbName + " created.")


def dropDB(dbName):
    path = os.getcwd() + "//" + dbName

    if os.path.isdir(path):
        try:
            os.rmdir(path)
        except:
            print("Error: trying to delete database with files inside")

        print("Database " + dbName + " deleted.")

    else:
        print("!Failed to delete database " + dbName + " because it does not exist.")


def useDB(dbName):
    global currDB
    global usingDB

    path = os.getcwd() + "//" + dbName

    if os.path.isdir(path):
        usingDB = True
        currDB = dbName
        print("Using database " + currDB)

    else:
        print("!Failed to use database: " + dbName + " because it does not exist")


def createTable(input):
    global currDB
    global usingDB

    # 3rd argument in input will be table name

    splitInput = input.split()

    tblName = splitInput[2]

    # if the table name is connected i.e. create table Employee(id int, name varchar(10));

    tableConnect = tblName.find("(")

    if tableConnect != -1:
        tblName = tblName[:tableConnect]




    path = os.getcwd() + "//" + currDB + "//" + tblName + ".tbl.txt"

    if usingDB:
        if not os.path.isfile(path):

            # find first '(' -- will indicate start of the var definitions
            # then substring the input from that position to 1 from the end to remove the ';'

            headerLoc = input.find('(')
            headers = input[headerLoc:-1]

            # then split to individual headers by each ','

            splitHeaders = headers.split(',')

            # then remove first '(' and last ')' from headers



            splitHeaders[0] = splitHeaders[0][1:]
            splitHeaders[-1] = splitHeaders[-1][:-1]

            for i in range(0, len(splitHeaders)):
                splitHeaders[i] = splitHeaders[i].strip()

            out = open(path, "w+")
            out.write("|".join(splitHeaders))
            print("Table " + tblName + " created.")

        else:
            print("!Failed to create table " + tblName + " because it already exists.")
    else:
        print("!Failed to create table " + tblName + " because you have not entered a database.")





def dropTable(input):
    splitInput = input.split()
    tblName = stripEnd(splitInput[-1])

    path = os.getcwd() + "//" + currDB + "//" + tblName + ".tbl.txt"

    if os.path.isfile(path):
        os.remove(path)
        print("Table " + tblName + " deleted.")

    else:
        print("!Failed to delete " + tblName + " because it does not exist.")


def select(input):

    # example: "select name, price from product where pid != 2;"

    # first split the input on the "from"
    # then split the first section --> "select ___" by select
    # this will then give you the items on the query

    # then split the second side of "from" --> "tableName _____" where __ is the conditions
    # can take the 0'th element to be the table

    # search the input for where --> if it is found then there are additional conditions
    # then split entire string by where --> last element will be the conditions
    # then strip the ';' from the conditions

    # if there are multiple tables in the request, a flag is set
    # this is done by checking if there is a ',' in the tablename

    splitInput = input.split("from")
    command = splitInput[0].lower().split("select")[-1]
    command = command.strip()
    multipleTables = False

    if input.find("where") != -1:
        tblName = splitInput[1].split("where")[0]
        tblName = stripEnd(tblName)
        tblName = tblName.strip()

    else:
        tblName = input.split()[-1];
        tblName = stripEnd(tblName)

    # after from is where the tables in reference are -- only need it to see if there are multiple

    if input.find("FROM") != -1:
        tableLocation = input.split("FROM")
        tableLocation = input.split("FROM")[1]

    else:
        tableLocation = input.split("from")
        tableLocation = input.split("from")[1]

    if tableLocation.find(',') != -1 or tableLocation.find("join") != -1:
        multipleTables = True

    # query on conditions
    if input.lower().find("where") != -1 or input.lower().find("on") != -1:
        isJoin = False
        # conditions found when using select with where
        if input.lower().find("where") != -1:

            conditions = input.split("where")[-1]
            conditions = conditions.strip()

        # conditions found when using select with join
        # also have to find table name differently
        if input.lower().find("join") != -1:
            isJoin = True
            conditions = input.split("on")

        if multipleTables:

            if not isJoin:

                tables = tblName.split(", ")

                # first import data from file -- need tableNames
                # first table name, take first element -- similarly with second
                tbl1 = tables[0].split()[0]
                tbl2 = tables[1].split()[0]

                path1 = os.getcwd() + "//" + currDB + "//" + tbl1 + ".tbl.txt"
                path2 = os.getcwd() + "//" + currDB + "//" + tbl2 + ".tbl.txt"

                if os.path.isfile(path1) and os.path.isfile(path2):
                    file1 = open(path1, "r")
                    file2 = open(path2, "r")

                    data1 = file1.readlines()
                    data2 = file2.readlines()

                    # for easy header lookup
                    tbl1Header = tb.tableHeaders(data1[0])
                    tbl2Header = tb.tableHeaders(data2[0])


                    conditionsSplit = conditions.split("=")

                    # getting first table and value
                    cond1Tbl = conditionsSplit[0].split(".")[0]
                    cond1Val = conditionsSplit[0].split(".")[1]
                    cond1Val = cond1Val.strip()

                    # getting second table and value
                    cond2Tbl = conditionsSplit[1].split(".")[0]
                    cond2Val = conditionsSplit[1].split(".")[1]
                    cond2Val = cond2Val.strip()
                    cond2Val = stripEnd(cond2Val)

                    index1 = tbl1Header.headerLookup(cond1Val)
                    index2 = tbl2Header.headerLookup(cond2Val)

                    # removing additional endline character
                    print(data1[0][:-1] + "|" + data2[0][:-1])

                    for i in range(1, len(data1)):
                        currData1 = data1[i].split("|")

                        for j in range(1, len(data2)):

                            currData2 = data2[j].split("|")


                            if int(currData1[index1]) == int(currData2[index2]):
                                temp = data1[i][:-1] + "|" + data2[j]
                                temp = temp.strip()
                                print(temp)

                else:
                    print("Table " + tbl1 + " does not exist.")
                    print(" Or, table " + tbl2 + " does not exist.")


            else:
                # inner join
                # input will be different, parsing command from new
                # need 2 tables --> one in front of from
                #                   one behind on
                # for first table
                # split on from -- take elem 1
                # then split on inner -- take elem 0
                # left with table name

                # for second table
                # split by join, take elem 1
                # split that on "on", take elem 0
                # left with table name
                if input.find("inner") != -1:
                    firstTbl = input.split("from")[1].strip()
                    firstTbl = firstTbl.split("inner")[0].strip()
                    firstTbl = firstTbl.split()[0].strip()


                    secondTbl = input.split("join")[1].strip()
                    secondTbl = secondTbl.split("on")[0].strip()
                    secondTbl = secondTbl.split()[0].strip()

                    path1 = os.getcwd() + "//" + currDB + "//" + firstTbl + ".tbl.txt"
                    path2 = os.getcwd() + "//" + currDB + "//" + secondTbl + ".tbl.txt"

                    if os.path.isfile(path1) and os.path.isfile(path2):

                        # now have to get what searching for in tables

                        file1 = open(path1, "r")
                        file2 = open(path2, "r")

                        data1 = file1.readlines()
                        data2 = file2.readlines()

                        # for easy header lookup
                        tbl1Header = tb.tableHeaders(data1[0])
                        tbl2Header = tb.tableHeaders(data2[0])

                        conditions = input.split("on")[1].strip()
                        conditions = stripEnd(conditions)

                        cond1 = conditions.split("=")[0].strip()
                        cond1 = cond1.split(".")[1].strip()

                        cond2 = conditions.split("=")[1].strip()
                        cond2 = cond2.split(".")[1].strip()

                        index1 = tbl1Header.headerLookup(cond1)
                        index2 = tbl2Header.headerLookup(cond2)

                        print(data1[0][:-1] + "|" + data2[0][:-1])

                        for i in range(1, len(data1)):
                            currData1 = data1[i].split("|")

                            for j in range(1, len(data2)):

                                currData2 = data2[j].split("|")

                                if int(currData1[index1]) == int(currData2[index2]):
                                    temp = data1[i][:-1] + "|" + data2[j]
                                    temp = temp.strip()
                                    print(temp)

                    else:
                        print("Failed query because " + firstTbl + " or " + secondTbl + " does not exist")


                # left outer join
                # start with getting table names
                # split by left, then split by from
                # then remove additional var to get tblname
                elif input.find("left outer") != -1:
                    firstTbl = input.split("left")[0].strip()
                    firstTbl = firstTbl.split("from")[1].strip()
                    firstTbl = firstTbl.split()[0].strip()

                    secondTbl = input.split("join")[1].strip();
                    secondTbl = secondTbl.split("on")[0].strip();
                    secondTbl = secondTbl.split()[0].strip()

                    path1 = os.getcwd() + "//" + currDB + "//" + firstTbl + ".tbl.txt"
                    path2 = os.getcwd() + "//" + currDB + "//" + secondTbl + ".tbl.txt"

                    if os.path.isfile(path1) and os.path.isfile(path2):
                        file1 = open(path1, "r")
                        file2 = open(path2, "r")

                        data1 = file1.readlines()
                        data2 = file2.readlines()

                        # for easy header lookup
                        tbl1Header = tb.tableHeaders(data1[0])
                        tbl2Header = tb.tableHeaders(data2[0])

                        # getting conditions

                        conditions = input.split("on")[1].strip()

                        cond1 = conditions.split("=")[0]
                        cond1 = cond1.split(".")[1].strip()
                        cond2 = conditions.split("=")[1]
                        cond2 = cond2.split(".")[1].strip()
                        cond2 = stripEnd(cond2)

                        index1 = tbl1Header.headerLookup(cond1)
                        index2 = tbl2Header.headerLookup(cond2)

                        temp = data1[0].strip()
                        temp += "|"
                        temp += data2[0].strip()

                        print(temp)

                        for i in range(1, len(data1)):
                            currData1 = data1[i].split("|")
                            printed = False

                            for j in range(1, len(data2)):

                                currData2 = data2[j].split("|")

                                if int(currData1[index1]) == int(currData2[index2]):
                                    temp = data1[i][:-1] + "|" + data2[j]
                                    temp = temp.strip()
                                    print(temp)
                                    printed = True

                            if printed == False:
                                temp = data1[i][:-1] + "|"
                                print(temp)

                    else:
                        print("Failed query because " + firstTbl + " or " + secondTbl + " does not exist")




        else:
            path = os.getcwd() + "//" + currDB + "//" + tblName + ".tbl.txt"
            # != case
            if os.path.isfile(path) and conditions.find("!=") != -1:



                file = open(path, "r")
                data = file.readlines()


                table = tb.tableHeaders(data[0])

                # splits the queried tables into variables
                # if there is only one then it remains,
                # if not then they are seperated into a list
                selectedVars = command.split(", ")

                indices = []

                firstLine = data[0].split("|")

                for i in selectedVars:
                    index = table.headerLookup(i)
                    indices.append(index)
                    print(firstLine[index], end="|")



                # the condition searching for will be first elem in split of "!="
                search = conditions.split("!=")[0]
                search = search.strip()

                val = conditions.split("!=")[1]
                val = val.strip()
                val = stripEnd(val)

                index = table.headerLookup(search)



                for i in range(1, len(data)):

                    curr = data[i].split("|")

                    for j in range(0, len(curr)):
                        if j == index:
                            if val == curr[j]:
                                continue
                            else:
                                out = ""
                                for k in indices:
                                    out += curr[k] + "|"
                                out = out[:-1]
                                print(out)


            else:
                print("!Failed to query table " + tblName + " because it does not exist.")

        #print(conditions)
        #print(tblName)

    # No conditions only query
    else:
        path = os.getcwd() + "//" + currDB + "//" + tblName + ".tbl.txt"
        if os.path.isfile(path):
            command = command.split()[0].strip()

            if command == '*':
                file = open(path, "r")
                temp = file.readlines()
                for i in temp:
                    print(i.strip())


        else:
            print("!Failed to query table " + tblName + " because it does not exist.")

def alter(input):

    # first split by table --> second half with contain the tablename as its first element
    # so simply split second half by space and use first element

    split1 = input.lower().split("table")
    split1 = split1[1].split()
    tblName = split1[0]

    path = os.getcwd() + "//" + currDB + "//" + tblName + ".tbl.txt"

    # split by add, the last element will contain what needs to be added
    # only currently supporting add, have not seen any other necessary implementations in sql scripts

    if input.lower().find("add") != -1:
        split2 = input.lower().split("add")
        addition = stripEnd(split2[-1])
        addition = addition.strip()

        if usingDB:
            if os.path.isfile(path):
                file = open(path, 'r')
                lines = file.readlines()
                lines.append(addition)

                out = open(path, "w+")
                out.write("|".join(lines))

                print("Table " + tblName + " modified.")

            else:
                print("!Failed to alter table " + tblName + " because it does not exist")
        else:
            print("Please enter a Database first")

def insert(input):


    # split by the word into --> tablename will be the first value on the right side [1]


    split1 = input.split("into")
    tblName = split1[1].split()[0]

    path = os.getcwd() + "//" + currDB + "//" + tblName + ".tbl.txt"

    # first remove all '/t' from the input
    # then find the first '(', values to enter will  follow
    # then split by ',' to get individual values

    input = re.sub(r'\t', '', input)

    valueLoc = input.find('(')

    values = input[valueLoc:]
    singleValues = values.split(',')

    singleValues[0] = singleValues[0][1:]
    singleValues[-1] = singleValues[-1][:-2].strip()


    if os.path.isfile(path):
        file = open(path, "a+")
        file.write("\n")
        file.write("|".join(singleValues))
        print("1 new record inserted")

    else:
        print("!Failed to insert into table " + tblName + " because it does not exist")



def update(input):

    # split input by word "set", the first element will contain "update tablename"
    # so split first segment and [1] will be tablename

    temp = input.split("set")
    tblName = temp[0].split()[1]

    # have to get what is changing
    # use the previous split, as the other side of set will contain whats changing
    # split it by where first, take first element --> something = something
    # then split by '=' will give condition

    firstCond = temp[1].split("where")[0]
    firstCond = firstCond.split("=")
    firstCond[0] = firstCond[0].strip()
    firstCond[1] = firstCond[1].strip()

    # similarly to above, except using the other side of where
    # also removing end semicolon

    secondCond = temp[1].split("where")[1]
    secondCond = secondCond.split("=")
    secondCond[1] = secondCond[1][:-1]
    secondCond[0] = secondCond[0].strip()
    secondCond[1] = secondCond[1].strip()


    path = os.getcwd() + "//" + currDB + "//" + tblName + ".tbl.txt"

    if os.path.isfile(path):

        file = open(path, "r+")

        line = file.readlines()

        variables = line[0].split("|")
        counter = 0
        firstCondIndex = -1
        secondCondIndex = -1

        # loop through first line from file -- the variable names
        # check to find index of variables looking for, and save


        for i in variables:
            if i.find(firstCond[0]) != -1:
                firstCondIndex = counter

            if i.find(secondCond[0]) != -1:
                secondCondIndex = counter

            counter += 1

        totalVars = counter

        counter = 0


        # the following loops through each line of input
        # it splits each line into individual variables
        # then loops through those
        # counting at each variable to see if it is a trigger for update (counter == secondCondIndex)
        # if it is, it checks if it passes the condition
        # if it does, it will change the value
        # also if the value is the last one, it adds a newline character for formatting

        newValues = []

        modified = 0

        for i in line:
            values = i.split("|")


            for j in values:
                if counter == secondCondIndex:
                    if j.find(secondCond[1]) != -1:
                        values[firstCondIndex] = firstCond[1]
                        modified += 1
                        if firstCondIndex == totalVars-1:
                            values[firstCondIndex] += "\n"

                counter += 1
            counter = 0
            newValues.append(values)

        # reset file pointer then re-write file

        file.truncate(0)

        for i in newValues:
            file.write("|".join(i))

        print(str(modified) + " records modified")




    else:
        print("!Failed to update table " + tblName + " because it does not exist")
        print("Check the case of the table entered, it is case sensitive")



def delete(input):

    temp = input.split("where")
    tblName = temp[0].split()[-1]

    path = os.getcwd() + "//" + currDB + "//" + tblName + ".tbl.txt"

    if os.path.isfile(path):

        # if condition is >
        # split on where, will give you something like price > 150 on second split ([1])
        # then split on the > and remove leading/trailing whitespace & ';'
        if input.find(">") != -1:
            conditions = temp[1].split(">")
            conditions[0] = conditions[0].strip()
            conditions[1] = conditions[1].strip()
            conditions[1] = conditions[1][:-1]

            file = open(path, "r+")

            line = file.readlines()

            variables = line[0].split("|")
            counter = 0
            index = -1

            delLine = False
            newValues = []
            removed = 0

            # loop through initial line to find index of condition

            for i in variables:
                if i.find(conditions[0]) != -1:
                    index = counter
                counter += 1

            counter = 0

            firstLineSkip = True;

            # loop through each line individually skipping the first one
            # then loop through each value, if on index the condition is checked
            # if condition is passed, flag is set, and the line is not appended

            for i in line:
                values = i.split("|")
                if firstLineSkip == False:
                    for j in values:
                        if index == counter:

                            if float(j) > float(conditions[1]):
                                delLine = True

                        counter += 1

                    if delLine == False:
                        newValues.append(i)
                    else:
                        delLine = False
                        removed += 1

                    counter = 0
                else:
                    firstLineSkip = False
                    newValues.append(i)

            # reset file pointer then re-write file
            file.truncate(0)

            for i in newValues:
                file.write(i)

            print(str(removed) + " records deleted.")




        # same as above but diff sign
        elif input.find("=") != -1:
            conditions = temp[1].split("=")
            conditions[0] = conditions[0].strip()
            conditions[1] = conditions[1].strip()
            conditions[1] = conditions[1][:-1]

            file = open(path, "r+")

            line = file.readlines()
            variables = line[0].split("|")

            counter = 0
            index = -1

            delLine = False
            newValues = []
            newValues.append(line[0])
            removed = 0
            firstLineSkip = True

            for i in variables:
                if i.find(conditions[0]) != -1:
                    index = counter
                    break
                counter += 1

            counter = 0

            for i in line:
                values = i.split("|")
                if firstLineSkip == False:
                    for j in values:

                        if index == counter:

                            if j == conditions[1]:
                                delLine = True

                        counter += 1

                    if delLine == False:
                        newValues.append(i)
                    else:
                        delLine = False
                        removed += 1

                    counter = 0

                firstLineSkip = False

            # reset file pointer then re-write file
            file.truncate(0)


            for i in newValues:
                file.write(i)

            print(str(removed) + " records deleted.")


        # same as above but diff sign
        elif input.find("<") != -1:
            conditions = temp[1].split("<")
            conditions[0] = conditions[0].strip()
            conditions[1] = conditions[1].strip()
            conditions[1] = conditions[1][:-1]
            file = open(path, "r+")

            line = file.readlines()

            variables = line[0].split("|")
            counter = 0
            index = -1

            delLine = False
            newValues = []
            newValues.append(line[0])
            removed = 0

            # loop through initial line to find index of condition

            for i in variables:
                if i.find(conditions[0]) != -1:
                    index = counter
                counter += 1


            counter = 0

            firstLineSkip = True;

            # loop through each line individually skipping the first one
            # then loop through each value, if on index the condition is checked
            # if condition is passed, flag is set, and the line is not appended

            for i in line:
                values = i.split("|")
                if firstLineSkip == False:
                    for j in values:
                        if index == counter:

                            if float(j) < float(conditions[1]):
                                delLine = True

                        counter += 1

                    if delLine == False:
                        newValues.append(i)
                    else:
                        delLine = False
                        removed += 1

                    counter = 0

                firstLineSkip = False

            # reset file pointer then re-write file
            file.truncate(0)

            for i in newValues:
                file.write(i)

            print(str(removed) + " records deleted")


    else:
        print("!Failed to remove from table " + tblName + " because it does not exist")

if __name__ == "__main__":
    main()
