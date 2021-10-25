class SymbolTable:

    def __init__(self):
        self.__hashTable = {}
        self.__firstEmpty = 0

    def add(self, value):
        initialValue = value
        value = str(value)
        sum = 0
        for character in value:
            sum += ord(character)

        if sum not in self.__hashTable.keys():
            self.__hashTable[sum] = [initialValue, -1]
            if sum == self.__firstEmpty:
                while self.__firstEmpty in self.__hashTable.keys():
                    self.__firstEmpty += 1
        else:
            if initialValue not in self.__hashTable[sum]:
                lastElement = ['somevalue', sum]
                element = self.__hashTable[sum]
                if (initialValue in self.__hashTable[sum]):
                    return (sum, initialValue)
                while element[1] != -1:
                    lastElement = element
                    element = self.__hashTable[element[1]]
                    if (initialValue in self.__hashTable[lastElement[1]]):
                        return (lastElement, initialValue)

                self.__hashTable[lastElement[1]][1] = self.__firstEmpty
                self.__hashTable[self.__firstEmpty] = [initialValue, -1]
                sum = self.__firstEmpty
                while self.__firstEmpty in self.__hashTable.keys():
                    self.__firstEmpty += 1

        return (sum, initialValue)

    def getContent(self):
        return self.__hashTable
