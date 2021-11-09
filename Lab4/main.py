states = []
alphabet = []
transitions = {}
finals = []
initial = ''


def classify(probe, mode):
    if mode == "~states":
        states.extend(probe.split(", "))
    elif mode == "~initial":
        global initial
        initial = probe
    elif mode == "~alpha":
        alphabet.extend(probe.split(","))
    elif mode == "~trans":
        probe = probe.replace(" ", "")
        values = probe.split("->")
        transitions.update(
            {(values[0], values[2]): values[1].split(",")})
    elif mode == "~final":
        tokens = probe.split(", ")
        finals.extend(tokens)


def check(sequence):
    currentNode = initial
    for element in sequence:

        if element not in alphabet:
            return False
        addedEdge = False
        for edge in transitions.keys():
            if edge[0] == currentNode and element in transitions[edge]:
                currentNode = edge[1]
                addedEdge = True
                break
        if addedEdge == False:
            return False
    return currentNode in finals


def readFile(fileName):
    file = open(fileName, 'r')
    line = file.readline()

    while line:
        if line.strip() == "~states":
            mode = "~states"
        elif line.strip() == "~initial":
            mode = "~initial"
        elif line.strip() == "~alpha":
            mode = "~alpha"
        elif line.strip() == "~trans":
            mode = "~trans"
        elif line.strip() == "~final":
            mode = "~final"
        else:
            classify(line.strip(), mode)

        line = file.readline()


def printMenu():
    print("1: Display the states")
    print("2: Display the alphabet")
    print("3: Display the transitions")
    print("4: Display the final state(s)")
    print("5: Check sequence")
    print("\n0: Exit")


if __name__ == "__main__":
    fileName = input("File name: ")
    readFile(fileName)

    while True:
        printMenu()

        option = input("> ")
        if option == "0":
            break
        elif option == "1":
            print("States: ", states, "\n")
        elif option == "2":
            print("Alphabet: ", alphabet, "\n")
        elif option == "3":
            print("Transitions: ", transitions, "\n")
        elif option == "4":
            print("Final state(s): ", finals, "\n")
        elif option == "5":
            sequence = input("Enter sequence: ")
            print(check(sequence))
        else:
            print("Invalid option")
