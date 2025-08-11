import numpy as np

outputLength = 10
nameThreshold = 10

# read CSV
numStats = np.genfromtxt("Poke-Search/pokemon.csv", dtype = (int), delimiter = ",", usecols=(0, 4, 5, 6, 7, 8, 9, 10, 11))
strStats = np.genfromtxt("Poke-Search/pokemon.csv", dtype = (str), delimiter = ",", usecols=(1, 2, 3, 12))

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

avgMag = 0
for pokemon in CSVStats:
    avgMag += np.linalg.norm(pokemon[5:11])
avgMag /= len(CSVStats)

# ANSI color codes
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[31m"
COLOR_YELLOW = "\033[33m"
COLOR_GREEN = "\033[32m"
COLOR_DIM = "\033[2m"

stat_labels = ["HP ", "Atk", "Def", "SpA", "SpD", "Spd"]
#stat_width = 9

#------------------------------------------------------------------------------

def color_stat(val):
    if val >= 100:
        color_code = COLOR_GREEN
    elif val >= 50:
        color_code = COLOR_YELLOW
    else:
        color_code = COLOR_RED
    val_str = str(val)
    # Pad val_str to stat_width without color for alignment
    padded_val = val_str.rjust(stat_width)
    # Insert color codes around the value only, keep padding outside
    # Since padding is included in the colored string, just color the val_str itself
    return color_code + val_str + COLOR_RESET + " " * (stat_width - len(val_str))

def statComparer(v1,v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    m1 = np.linalg.norm(v1)
    m2 = np.linalg.norm(v2)
    v1Adjusted = v1 / m1
    v2Adjusted = v2 / m2

    return np.dot(v1Adjusted, v2Adjusted) / (np.linalg.norm(v1-v2) / avgMag + 1)

def findName(searchName):
    matches = []
    # threshold varible at top

    # Find all partial matches
    for i in range(len(CSVStats)):
        if searchName.lower() in CSVStats[i][1].lower():
            matches.append((i, CSVStats[i]))  # store index + data

    if not matches:
        print("ERROR - no Pokémon found by that name - Note: not case-sensitive")
        return None

    elif len(matches) == 1:
        # Only one match — pick it automatically
        index, match = matches[0]
        return match

    else:
        # Multiple matches — handle threshold display
        start_count = min(len(matches), nameThreshold)
        shown_matches = matches[:start_count]

        while True:
            print(f"\nMatches found (showing {len(shown_matches)} of {len(matches)}):")
            for idx, (i, match) in enumerate(shown_matches, start=1):
                print(f"{idx}. {match[1]}")  # match[1] is the name

            if len(shown_matches) < len(matches):
                print("")
                print(f"{len(shown_matches)+1}. Show more")
                print(f"{len(shown_matches)+2}. Show all")

            choice = input("Select your Pokémon: ").strip()

            try:
                choice_num = int(choice)

                # Handle "show more" option
                if (len(shown_matches) < len(matches)
                    and choice_num == len(shown_matches) + 1):
                    # Extend the list
                    new_count = min(len(shown_matches) + nameThreshold, len(matches))
                    shown_matches = matches[:new_count]
                    continue

                # Handle "show all" option
                if (len(shown_matches) < len(matches)
                    and choice_num == len(shown_matches) + 2):
                    shown_matches = matches
                    continue

                # Handle valid Pokémon selection
                if 1 <= choice_num <= len(shown_matches):
                    index, match = shown_matches[choice_num - 1]
                    return match

                print("Invalid choice.")
            except ValueError:
                print("Invalid input.")


#------------------------------------------------------------------------------

while True:
    isVerbose = False
    isHelping = False
    sortBasedOnName = False
    sortBasedOnIndex = False
    sortBasedOnStats = False
    guessGame = False

    comparisonArray = []
    comparisonName = ""

    user_input = input(">")

    # Input commands
    command = user_input.split()
    for i in range(len(command)):
        if command[i] == "-v":
            isVerbose = True
        if command[i] == "-H" or command[i] == "--help":
            isHelping = True
        if command[i] == "--name" or command[i] == "-N":
            if i+1 <= len(command) - 1:
                sortBasedOnName = True
                searchName = command[i+1]
            else:
                print("ERROR - no name included")
                continue
        if command[i] == "--guess" or command[i] == "-G":
            if i+1 <= len(command) - 1:
                guessGame = True
                guessName = command[i+1]
            else:
                print("ERROR - no name included")
                continue
        if command[i] == "--index" or command[i] == "-I":
            if i+1 <= len(command) - 1:
                sortBasedOnIndex = True
                searchIndex = command[i+1]
            else:
                print("ERROR - no index included")
                continue
        if command[i] == "--stat" or command[i] == "-S":
            if i+1 <= len(command) - 1:
                sortBasedOnStats = True
                searchStat = command[i+1]
            else:
                print("ERROR - no stats included - enter as 54,34,23,45,46,12 for example")
                continue

    if not (isVerbose or isHelping or sortBasedOnName or sortBasedOnStats or sortBasedOnIndex or guessGame):
        print("ERROR - no conditions included - try '--help'")
        continue

    if isHelping:
        print("-v          : Verbose\n--help  -H  : Help\n--name  -N  : Search by Pokémon Name\n--index -I  : Search by Pokémon Index\n--stat  -S  : Search by Set of Stats\n--output -O : Set number of outputs\n--threshold -T : Set length of name selection threshold")
        continue

    if guessGame:
        # Set target Pokémon
        comparisonName = findName(guessName)
        comparisonArray = comparisonName[5:11]
        if comparisonArray is None:
            print("Invalid Name")
            continue

        # Clear the screen
        if not isVerbose: print("\n" * 50)
        print("**Pokémon Guessing Game**")
        print("-------------------------")

        # Get player count
        try:
            playerCount = int(input("Enter the number of players: "))
        except ValueError:
            print("Invalid number of players.")
            continue

        playerAnswers = []
        playerStats = []
        scores = []

        # Input each player guesses
        for i in range(playerCount):
            guess = input(f"Player {i+1}, enter a Pokémon: ")
            playerGuessName = findName(guess)
            stats = playerGuessName[5:11]
            if stats is None:
                print("Not a valid Pokémon — skipping.")
                playerAnswers.append(guess)
                playerStats.append(None)
                scores.append(float("-inf"))  # impossible score - ie filler score
            else:
                playerAnswers.append(playerGuessName)
                playerStats.append(stats)
                score = statComparer(comparisonArray, stats)
                scores.append(score)

        # Rank players by score
        print("\nResults:")
        ranked = sorted(zip(playerAnswers, scores), key=lambda x: x[1], reverse=True)
        for rank, (name, score) in enumerate(ranked, start=1):
            if score == float("-inf"):
                print(f"{rank}. {name} — Invalid guess")
            else:
                print(f"{rank}. {name} — Similarity: {score:.4f}")

        if not isVerbose: revealAnswerQuery = input("Reveal Pokémon?[y/n]: ")
        if revealAnswerQuery.lower() == "y" or isVerbose:
            print("\nThe target Pokémon was:", comparisonName)
            if not isVerbose: extraInfoQuery = input("Show Similar Pokémon?[y/n]: ")
            if revealAnswerQuery.lower() != "y" or not isVerbose:
                continue


    if sortBasedOnName:
        # Set target Pokémon
        comparisonName = findName(searchName)
        comparisonArray = comparisonName[5:11]
        if comparisonArray is None:
            print("Invalid Name")
            continue


    if sortBasedOnIndex:
        for i in range(len(CSVStats)):
            if CSVStats[i][0] == int(searchIndex):
                comparisonArray = CSVStats[i][5:11]
                break
        if comparisonArray == []:
            print("ERROR - no Pokémon found by that index")
            continue

    if sortBasedOnStats:
        comparisonArray = searchStat.split(",")
        tempArray = comparisonArray
        for i in range(len(comparisonArray)):
            comparisonArray[i] = int(tempArray[i])

    # Compare all Pokémon
    comparedStatsArray = []
    for i in range(len(CSVStats)):
        comparedStatsArray.append((CSVStats[i][1], statComparer(comparisonArray, CSVStats[i][5:11]),CSVStats[i][5:11]))
    comparedStatsArray = np.array(comparedStatsArray, dtype=[("name", 'U30'), ('comparisonValue', 'f8'),("values", "f8", (6,))])

    a = np.sort(comparedStatsArray, order="comparisonValue")


    if isVerbose:
        for i in range(outputLength):
            print(str(a[len(a) - i - 1]), str())
    else:
        print("\nSimilar Pokémon:")

        total_results = len(CSVStats)
        page_size = nameThreshold
        current_page = 0
        max_page = (total_results - 1) // page_size  # zero-based last page

        # Define widths for columns
        no_width = 4
        name_width = 30
        stat_width = 5  # width per stat column

        while True:
            start_idx = current_page * page_size
            end_idx = min(start_idx + page_size, total_results)
            shown_count = end_idx - start_idx

            # Print header: No, Name, then stat labels spaced evenly
            header_no = f"{'No.':<{no_width}}"
            header_name = f"{'Name':<{name_width - 2}}"
            header_stats = "".join(f"{label:>{stat_width}}" for label in stat_labels)
            print(header_no + header_name + header_stats)
            print("-" * (no_width + name_width + stat_width * len(stat_labels)))

            # Print current page entries
            for i in range(start_idx, end_idx):
                name = a[len(a) - i - 1][0]
                stats_row = next(row for row in CSVStats if row[1] == name)
                stats = stats_row[5:11]
                colored_stats = "".join(color_stat(val) for val in stats)
                print(f"{i + 1:<{no_width}}{name:<{name_width}}{colored_stats}")

            print("")

            # Menu options
            menu_options = ["show_all", "prior", "next", "close"]

            # Show All - always enabled
            print("1) Show All")

            # Prior Page
            if current_page == 0:
                print(COLOR_DIM + "2) Go to Prior Page (disabled)" + COLOR_RESET)
                prior_enabled = False
            else:
                print("2) Go to Prior Page")
                prior_enabled = True

            # Next Page
            if current_page == max_page:
                print(COLOR_DIM + "3) Next Page (disabled)" + COLOR_RESET)
                next_enabled = False
            else:
                print("3) Next Page")
                next_enabled = True

            # Close - always enabled
            print("4) Close")

            choice = input("Select an option: ").strip()

            try:
                choice_num = int(choice)

                if choice_num == 1:
                    action = "show_all"

                elif choice_num == 2:
                    if prior_enabled:
                        action = "prior"
                    else:
                        print("Prior page option is disabled on the first page.")
                        continue

                elif choice_num == 3:
                    if next_enabled:
                        action = "next"
                    else:
                        print("Next page option is disabled on the last page.")
                        continue

                elif choice_num == 4:
                    action = "close"

                else:
                    print("Invalid choice.")
                    continue

                if action == "prior":
                    current_page -= 1
                elif action == "next":
                    current_page += 1
                elif action == "show_all":
                    print("\nShowing all remaining results:\n")
                    print(header_no + header_name + header_stats)
                    print("-" * (no_width + name_width + stat_width * len(stat_labels)))

                    for i in range(current_page * page_size, total_results):
                        name = a[len(a) - i - 1][0]
                        stats_row = next(row for row in CSVStats if row[1] == name)
                        stats = stats_row[5:11]
                        colored_stats = "".join(f"{color_stat(val):>{stat_width}}" for val in stats)
                        print(f"{i + 1:<{no_width}}{name:<{name_width}}{colored_stats}")
                    break

                elif action == "close":
                    break

            except ValueError:
                print("Invalid input.")

        print("")  # Clean spacing after closing





