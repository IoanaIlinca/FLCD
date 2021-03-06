class FAanalyzer:
    states = []
    alphabet = []
    transitions = {}
    finals = []
    initial = ''

    def __init__(self):
        self.states = []
        self.alphabet = []
        self.transitions = {}
        self.finals = []
        self.initial = ''

    def classify(self, probe, mode):
        if mode == "~states":
            self.states.extend(probe.split(", "))
        elif mode == "~initial":
            self.initial = probe
        elif mode == "~alphabet":
            self.alphabet.extend(probe.split(","))
        elif mode == "~transitions":
            probe = probe.replace(" ", "")
            values = probe.split("->")
            self.transitions.update(
                {(values[0], values[2]): values[1].split(",")})
        elif mode == "~final":
            tokens = probe.split(", ")
            self.finals.extend(tokens)

    def check(self, sequence):
        currentNode = self.initial
        for element in sequence:

            if element not in self.alphabet:
                return False
            addedEdge = False
            for edge in self.transitions.keys():
                if edge[0] == currentNode and element in self.transitions[edge]:
                    currentNode = edge[1]
                    addedEdge = True
                    break
            if addedEdge == False:
                return False
        return currentNode in self.finals

    def readFile(self, fileName):
        file = open(fileName, 'r')
        line = file.readline()

        while line:
            if line.strip() == "~states":
                mode = "~states"
            elif line.strip() == "~initial":
                mode = "~initial"
            elif line.strip() == "~alphabet":
                mode = "~alphabet"
            elif line.strip() == "~transitions":
                mode = "~transitions"
            elif line.strip() == "~final":
                mode = "~final"
            else:
                self.classify(line.strip(), mode)

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
    fa = FAanalyzer()
    fa.readFile(fileName)

    while True:
        printMenu()

        option = input("> ")
        if option == "0":
            break
        elif option == "1":
            print("States: ", fa.states, "\n")
        elif option == "2":
            print("Alphabet: ", fa.alphabet, "\n")
        elif option == "3":
            print("Transitions: ", fa.transitions, "\n")
        elif option == "4":
            print("Final state(s): ", fa.finals, "\n")
        elif option == "5":
            sequence = input("Enter sequence: ")
            print(fa.check(sequence))
        else:
            print("Invalid option")
