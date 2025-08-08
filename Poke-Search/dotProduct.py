import numpy as np

isVerbose = False
isHelping = False
sortBasedOnName = False
sortBasedOnIndex = False
sortBasedOnStats = False
outputLength = 10

numStats = np.genfromtxt("pokemon.csv", dtype = (int), delimiter = ",", usecols=(0, 4, 5, 6, 7, 8, 9, 10, 11))
strStats = np.genfromtxt("pokemon.csv", dtype = (str), delimiter = ",", usecols=(1, 2, 3, 12))

CSVStats = []

for i in range(len(numStats)):
    tempArray = []
    tempArray.append(int(numStats[i][0]))
    tempArray.append(str(strStats[i][0]))
    tempArray.append(str(strStats[i][1]))
    tempArray.append(str(strStats[i][2]))
    tempArray.append(int(numStats[i][1]))
    tempArray.append(int(numStats[i][2]))
    tempArray.append(int(numStats[i][3]))
    tempArray.append(int(numStats[i][4]))
    tempArray.append(int(numStats[i][5]))
    tempArray.append(int(numStats[i][6]))
    tempArray.append(int(numStats[i][7]))
    tempArray.append(int(numStats[i][8]))
    tempArray.append(str(strStats[i][3]))
    CSVStats.append(tempArray)

comparisonArray = []

def statComparer(v1,v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    return (np.dot(v1/np.linalg.norm(v1), v2/np.linalg.norm(v2))) #/ (np.linalg.norm([v1,v2]) + 1)

# pokecomp -v -H --name --stat

user_input = input(">")

command = user_input.split()
for i in range(len(command)):
    if command[i] == "-v":
        isVerbose = True
    if command[i] == "-H" or command[i] == "--help":
        isHelping = True
    if command[i] == "-O" or command[i] == "--output":
        if i+1 <= len(command) - 1:
            outputLength = int(command[i+1])
        else:
            print("ERROR - no length included - defaulting to 10")
    if command[i] == "--name" or command[i] == "-N":
        if i+1 <= len(command) - 1:
            sortBasedOnName = True
            searchName = command[i+1]
        else:
            print("ERROR - no name included")
            breakpoint
    if command[i] == "--index" or command[i] == "-I":
        if i+1 <= len(command) - 1:
            sortBasedOnIndex = True
            searchIndex = command[i+1]
        else:
            print("ERROR - no index included")
            breakpoint
    if command[i] == "--stat" or command[i] == "-S":
        if i+1 <= len(command) - 1:
            sortBasedOnStats = True
            searchStat = command[i+1]
        else:
            print("ERROR - no stats included - enter as 54,34,23,45,46,12 for example")
            breakpoint

if not (isVerbose or isHelping or sortBasedOnName or sortBasedOnStats or sortBasedOnIndex):
    print("ERROR - no conditions included - try '--help'")
    breakpoint

if isHelping:
    print("-v         : Verbose\n--help  -H : Help\n--name  -N : Search by Pokemon Name\n--index -I : Search by Pokemon Index\n--stat  -S : Search by Set of Stats\n--output -O : Set number of outputs")

if sortBasedOnName:
    for i in range(len(CSVStats)):
        if CSVStats[i][1].lower() == searchName.lower():
            comparisonArray = CSVStats[i][5:11]
            break
    if comparisonArray == []:
        print("ERROR - no pokemon found by that name - Note: not case-sensitive")

if sortBasedOnIndex:
    for i in range(len(CSVStats)):
        if CSVStats[i][0] == int(searchIndex):
            comparisonArray = CSVStats[i][5:11]
            break
    if comparisonArray == []:
        print("ERROR - no pokemon found by that index")

if sortBasedOnStats:
    comparisonArray = searchStat.split(",")
    tempArray = comparisonArray
    for i in range(len(comparisonArray)):
        comparisonArray[i] = int(tempArray[i])

comparedStatsArray = []
#print(comparisonArray)
for i in range(len(CSVStats)):
    comparedStatsArray.append((CSVStats[i][1], statComparer(comparisonArray, CSVStats[i][5:11])))
comparedStatsArray = np.array(comparedStatsArray, dtype=[("name", 'U30'), ('comparisonValue', 'f8')])

a = np.sort(comparedStatsArray, order='comparisonValue')
arr = np.sort(a)[::-1]


for i in range(outputLength):
    print(arr[i])
