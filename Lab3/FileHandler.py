
from SymbolTable import SymbolTable
from FAanalyzer import FAanalyzer
import re
import copy


pif = []
st = SymbolTable()

files = ["H:\\Faculta\\an 3\\Formal Languages and Compiler Design\\p1.TXT",
         "H:\\Faculta\\an 3\\Formal Languages and Compiler Design\\p2.TXT",
         "H:\\Faculta\\an 3\\Formal Languages and Compiler Design\\p3.TXT",
         "H:\\Faculta\\an 3\\Formal Languages and Compiler Design\\p2err.TXT"]

operatorsAndSeparators = []
reservedWords = []

file = open(
    "H:\\Faculta\\an 3\\Formal Languages and Compiler Design\\Lab3\\operatorsAndSeparators.txt", "r")

line = file.readline()

while line:
    line = line.strip()
    if line not in ["<space>", "<tab>", "<newline>", ""]:
        operatorsAndSeparators.append(line)
    line = file.readline()


file = open(
    "H:\\Faculta\\an 3\\Formal Languages and Compiler Design\\Lab3\\reservedWords.txt", "r")

line = file.readline()

while line:
    line = line.strip()
    if line not in ["<space>", "<tab>", "<newline>", ""]:
        reservedWords.append(line)
    line = file.readline()


followsReservedWords = copy.deepcopy(operatorsAndSeparators)


followsReservedWords.append(" ")
followsReservedWords.append("\\n")
followsReservedWords.append("\\t")


for fileName in files:
    file = open(fileName, "r")
    lineNumber = 0
    line = file.readline()
    fileLog = ""
    while line:
        line = line.strip()
        identifiersAndConstants = line
        pattern = r"(\".+\")|(\<\!\-\-.+\-\-\>)"
        stringsAndComments = ["".join(x) for x in re.findall(
            pattern, line,  re.DOTALL)]

        strings = re.findall(r"(\".+\")", line,  re.DOTALL)
        comments = re.findall(r"(\<\!\-\-.+\-\-\>)", line,  re.DOTALL)

        for comment in comments:
            line = line.replace(comment, " ")

        identifiersAndConstants = line

        for item in strings:
            identifiersAndConstants = identifiersAndConstants.replace(
                item, "")

        # here there are the identifiersAndConstants and the reservedWordsSeparataorsOperatorsInLine left
        reservedWordsSeparataorsOperatorsInLine = identifiersAndConstants

        for token in reservedWords:
            regexString = "/[^A-Za-z0-9]/g" + \
                token + "/[^A-Za-z0-9]/g"

            indexes = [m.start()
                       for m in re.finditer(token, identifiersAndConstants)]
            for index in indexes:
                if (index > 0):
                    if index + len(token) < (len(identifiersAndConstants) - 1):
                        if (identifiersAndConstants[index - 1] in followsReservedWords) and (identifiersAndConstants[index + len(token)] in followsReservedWords):
                            identifiersAndConstants = identifiersAndConstants[:index] + \
                                " " + \
                                identifiersAndConstants[(index + len(token)):]
                    else:
                        if identifiersAndConstants[index - 1] in followsReservedWords:
                            identifiersAndConstants = identifiersAndConstants[:index] + \
                                " " + \
                                identifiersAndConstants[(index + len(token)):]
                else:
                    if index + len(token) < (len(identifiersAndConstants) - 1):
                        if (identifiersAndConstants[index + len(token)] in followsReservedWords):
                            identifiersAndConstants = identifiersAndConstants[:index] + \
                                " " + \
                                identifiersAndConstants[(index + len(token)):]
                    else:
                        identifiersAndConstants = identifiersAndConstants[:index] + \
                            " " + \
                            identifiersAndConstants[(index + len(token)):]

        for token in operatorsAndSeparators:
            identifiersAndConstants = identifiersAndConstants.replace(
                token, " ")

        for token in identifiersAndConstants:
            reservedWordsSeparataorsOperatorsInLine = reservedWordsSeparataorsOperatorsInLine.replace(
                token, " ")

        identifiersAndConstants = identifiersAndConstants.split()
        errors = []
        copyIdentifiersAndConstants = copy.deepcopy(identifiersAndConstants)

        faId = FAanalyzer()
        faId.readFile("FAidentifier.txt")
        faInt = FAanalyzer()
        faInt.readFile("FAintegerConstant.txt")
        for token in copyIdentifiersAndConstants:
            if token.find('\'') != -1:
                if (token[0] != '\'' or token[-1] != '\''):
                    errors.append(token)
                    identifiersAndConstants.remove(token)
                else:
                    if len(token) > 3 and (len(token) > 4 or token[1] != '\\'):
                        errors.append(token)
                        identifiersAndConstants.remove(token)
            else:
                isIdentifier = faId.check(token)
                isIntConstant = faInt.check(token)
                if not isIdentifier and not isIntConstant:
                    errors.append(token)
                    identifiersAndConstants.remove(token)

        for token in reservedWords:
            if token not in ["if", "for"]:
                reservedWordsSeparataorsOperatorsInLine = reservedWordsSeparataorsOperatorsInLine.replace(
                    token, " " + token + " ")
            else:
                reservedWordsSeparataorsOperatorsInLine = reservedWordsSeparataorsOperatorsInLine.replace(
                    "elif", "alabala")
                reservedWordsSeparataorsOperatorsInLine = reservedWordsSeparataorsOperatorsInLine.replace(
                    "foreach", "portocala")
                reservedWordsSeparataorsOperatorsInLine = reservedWordsSeparataorsOperatorsInLine.replace(
                    token, " " + token + " ")
                reservedWordsSeparataorsOperatorsInLine = reservedWordsSeparataorsOperatorsInLine.replace(
                    "alabala", "elif")
                reservedWordsSeparataorsOperatorsInLine = reservedWordsSeparataorsOperatorsInLine.replace(
                    "portocala", "foreach")

        reservedWordsSeparataorsOperatorsInLine = reservedWordsSeparataorsOperatorsInLine.split()

        for index in range(len(reservedWordsSeparataorsOperatorsInLine)):
            token = reservedWordsSeparataorsOperatorsInLine[index]
            if token not in operatorsAndSeparators and token not in reservedWords:
                token = list(token)
                reservedWordsSeparataorsOperatorsInLine = reservedWordsSeparataorsOperatorsInLine[:index] + \
                    token + reservedWordsSeparataorsOperatorsInLine[index + 1:]

        while(len(strings) > 0 or len(identifiersAndConstants) > 0 or len(reservedWordsSeparataorsOperatorsInLine) > 0):
            if (len(strings) > 0):
                indexFirstString = line.find(strings[0])

            else:
                indexFirstString = 0x3f3f3f3f

            if (len(identifiersAndConstants) > 0):
                indexFirstIdConst = line.find(identifiersAndConstants[0])

            else:
                indexFirstIdConst = 0x3f3f3f3f

            if (len(reservedWordsSeparataorsOperatorsInLine) > 0):
                indexFirstRWSO = line.find(
                    reservedWordsSeparataorsOperatorsInLine[0])

            else:
                indexFirstRWSO = 0x3f3f3f3f

            minIndex = min(indexFirstString, indexFirstIdConst, indexFirstRWSO)

            if (minIndex == indexFirstString):
                index = st.add(strings[0])
                pif.append([strings[0], index[0]])
                line = line.replace(strings[0], "", 1)
                strings.pop(0)
            if (minIndex == indexFirstIdConst):
                index = st.add(identifiersAndConstants[0])
                pif.append([identifiersAndConstants[0], index[0]])

                line = line.replace(identifiersAndConstants[0], "", 1)
                identifiersAndConstants.pop(0)
            if (minIndex == indexFirstRWSO):
                pif.append([reservedWordsSeparataorsOperatorsInLine[0], 0])
                line = line.replace(
                    reservedWordsSeparataorsOperatorsInLine[0], "", 1)
                reservedWordsSeparataorsOperatorsInLine.pop(0)

        if len(errors) > 0:
            fileLog += "Lexical error on line " + \
                str(lineNumber) + " with the following: "
            fileLog += str(errors) + '\n'

        line = file.readline()
        lineNumber += 1

    fileName = fileName.split(".")
    fileName = fileName[0].split("\\")
    fileName = fileName[-1]
    f = open(fileName + "PIF.out", "w")
    f.write(str(pif))
    f.close()
    f = open(fileName + "ST.out", "w")
    f.write("Hash table with coalesced chaining\n")
    f.write(str(st.getContent()))
    f.close()
    f = open(fileName + "status.out", "w")
    if fileLog == "":
        fileLog = "lexically correct"
    f.write(fileLog)
    f.close()
