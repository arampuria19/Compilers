import copy

# Perform grammar augmentation
def grammarAugmentation(rules, nonterm_userdef, start_symbol):
    # New rules store processed output rules
    newRules = []

    # Create unique 'symbol' to represent new start symbol
    newChar = start_symbol + "'"
    while newChar in nonterm_userdef:
        newChar += "'"

    # Adding rule to bring start symbol to RHS
    newRules.append([newChar, ['.', start_symbol]])

    # New format => [LHS,[.RHS]]
    # Can't use a dictionary since duplicate keys can be there
    for rule in rules:
        # Split LHS from RHS
        k = rule.split("->")
        lhs = k[0].strip()
        rhs = k[1].strip()

        # Split all rule at '|'
        # Keep single derivation in one rule
        multirhs = rhs.split('|')
        for rhs1 in multirhs:
            rhs1 = rhs1.strip().split()

            # ADD dot pointer at start of RHS
            rhs1.insert(0, '.')
            newRules.append([lhs, rhs1])

    return newRules

# Find closure
def findClosure(input_state, dotSymbol):
    global start_symbol, separatedRulesList, statesDict

    # ClosureSet stores processed output
    closureSet = []

    # If findClosure is called for the 1st time i.e., for I0,
    # then LHS is received in "dotSymbol",
    # add all rules starting with LHS symbol to closureSet
    if dotSymbol == start_symbol:
        for rule in separatedRulesList:
            if rule[0] == dotSymbol:
                closureSet.append(rule)
    else:
        # For any higher state than I0,
        # set the initial state as the received input_state
        closureSet = input_state

    # Iterate until new states are getting added in closureSet
    prevLen = -1
    while prevLen != len(closureSet):
        prevLen = len(closureSet)

        # "tempClosureSet" - used to eliminate concurrent modification error
        tempClosureSet = []

        # If dot points at a new symbol, add corresponding rules to tempClosure
        for rule in closureSet:
            indexOfDot = rule[1].index('.')
            if rule[1][-1] != '.':
                dotPointsHere = rule[1][indexOfDot + 1]
                for in_rule in separatedRulesList:
                    if dotPointsHere == in_rule[0] and in_rule not in tempClosureSet:
                        tempClosureSet.append(in_rule)

        # Add new closure rules to closureSet
        for rule in tempClosureSet:
            if rule not in closureSet:
                closureSet.append(rule)

    return closureSet

def computeGOTO(state):
    global statesDict, stateCount

    # Find all symbols on which we need to make function call - GOTO
    generateStatesFor = []
    for rule in statesDict[state]:
        # If the rule is not a "Handle"
        if rule[1][-1] != '.':
            indexOfDot = rule[1].index('.')
            dotPointsHere = rule[1][indexOfDot + 1]
            if dotPointsHere not in generateStatesFor:
                generateStatesFor.append(dotPointsHere)

    # Call GOTO iteratively on all symbols pointed by the dot
    if len(generateStatesFor) != 0:
        for symbol in generateStatesFor:
            GOTO(state, symbol)
    return

def GOTO(state, charNextToDot):
    global statesDict, stateCount, stateMap

    # New state stores processed new state
    newState = []
    for rule in statesDict[state]:
        indexOfDot = rule[1].index('.')
        if rule[1][-1] != '.':
            if rule[1][indexOfDot + 1] == charNextToDot:
                # Swapping element with dot to perform shift operation
                shiftedRule = copy.deepcopy(rule)
                shiftedRule[1][indexOfDot] = shiftedRule[1][indexOfDot + 1]
                shiftedRule[1][indexOfDot + 1] = '.'
                newState.append(shiftedRule)

    # Add closure rules for newState, call findClosure function iteratively on all existing rules in newState

    # addClosureRules - used to store new rules temporarily,
    # to prevent concurrent modification error
    addClosureRules = []
    for rule in newState:
        indexOfDot = rule[1].index('.')
        # Check that the rule is not a "Handle"
        if rule[1][-1] != '.':
            closureRes = findClosure(newState, rule[1][indexOfDot + 1])
            for rule in closureRes:
                if rule not in addClosureRules and rule not in newState:
                    addClosureRules.append(rule)

    # Add closure result to newState
    for rule in addClosureRules:
        newState.append(rule)

    # Find if newState already exists in the Dictionary
    stateExists = -1
    for state_num in statesDict:
        if statesDict[state_num] == newState:
            stateExists = state_num
            break

    # stateMap is a mapping of GOTO with its output states
    if stateExists == -1:

        # If newState is not in the dictionary,
        # then create a new state
        stateCount += 1
        statesDict[stateCount] = newState
        stateMap[(state, charNextToDot)] = stateCount
    else:

        # If state repetition is found,
        # assign that previous state number
        stateMap[(state, charNextToDot)] = stateExists
    return

def generateStates(statesDict):
    prev_len = -1
    called_GOTO_on = []

    # Run loop until new states are getting added
    while len(statesDict) != prev_len:
        prev_len = len(statesDict)
        keys = list(statesDict.keys())

        # Make computeGOTO function call on all states in the dictionary
        for key in keys:
            if key not in called_GOTO_on:
                called_GOTO_on.append(key)
                computeGOTO(key)
    return

# Calculation of first
# Epsilon is denoted by '#' (semi-colon)

# Pass the rule in the first function
def first(rule):
    global rules, nonterm_userdef, term_userdef, diction, firsts

    # Recursion base condition (for terminal or epsilon)
    if len(rule) != 0 and (rule is not None):
        if rule[0] in term_userdef:
            return rule[0]
        elif rule[0] == '#':
            return '#'

    # Condition for Non-Terminals
    if len(rule) != 0:
        if rule[0] in list(diction.keys()):

            # Fresh temporary list of results
            fres = []
            rhs_rules = diction[rule[0]]

            # Call first on each rule of RHS fetched (& take union)
            for itr in rhs_rules:
                indivRes = first(itr)
                if type(indivRes) is list:
                    for i in indivRes:
                        fres.append(i)
                else:
                    fres.append(indivRes)

            # If no epsilon in the result, return fres
            if '#' not in fres:
                return fres
            else:

                # Apply epsilon rule => f(ABC) = f(A) - {e} U f(BC)
                newList = []
                fres.remove('#')
                ansNew = first(rule[1:])
                if ansNew != None:
                    if type(ansNew) is list:
                        newList = fres + ansNew
                    else:
                        newList = fres + [ansNew]
                else:
                    newList = fres
                return newList

    # Lastly, if epsilon still persists, keep it in the result of first
    fres.append('#')
    return fres

# Calculation of follow
def follow(nt):
    global start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows

    # For start symbol, return $ (recursion base case)
    solset = set()
    if nt == start_symbol:
        solset.add('$')

    # Check all occurrences
    # solset - is the result of computed 'follow' so far

    # For input, check in all rules
    for curNT in diction:
        rhs = diction[curNT]

        # Go through all productions of NT
        for subrule in rhs:
            if nt in subrule:

                # Call for all occurrences on non-terminal in subrule
                while nt in subrule:
                    index_nt = subrule.index(nt)
                    subrule = subrule[index_nt + 1:]

                    # Empty condition - call follow on LHS
                    if len(subrule) != 0:

                        # Compute first if symbols on RHS of the target Non-Terminal exist
                        res = first(subrule)

                        # If epsilon in the result, apply the rule (A->aBX) - follow of - follow(B) = (first(X) - {e}) U follow(A)
                        if '#' in res:
                            newList = []
                            res.remove('#')
                            ansNew = follow(curNT)
                            if ansNew != None:
                                if type(ansNew) is list:
                                    newList = res + ansNew
                                else:
                                    newList = res + [ansNew]
                            else:
                                newList = res
                            res = newList
                    else:

                        # When nothing in RHS, go circular and take the follow of LHS
                        # Only if (NT in LHS) != curNT
                        if nt != curNT:
                            res = follow(curNT)

                    # Add follow result in set form
                    if res is not None:
                        if type(res) is list:
                            for g in res:
                                solset.add(g)
                        else:
                            solset.add(res)
    return list(solset)

def createParseTable(statesDict, stateMap, T, NT):
    global separatedRulesList, diction

    # Create rows and columns
    rows = list(statesDict.keys())
    cols = T + ['$'] + NT

    # Create an empty table
    Table = []
    tempRow = []
    for y in range(len(cols)):
        tempRow.append('')
    for x in range(len(rows)):
        Table.append(copy.deepcopy(tempRow))

    # Make shift and GOTO entries in the table
    for entry in stateMap:
        state = entry[0]
        symbol = entry[1]
        # Get index
        a = rows.index(state)
        b = cols.index(symbol)
        if symbol in NT:
            Table[a][b] = Table[a][b] + f"{stateMap[entry]} "
        elif symbol in T:
            Table[a][b] = Table[a][b] + f"S{stateMap[entry]} "

    # Start REDUCE procedure

    # Number the separated rules
    numbered = {}
    key_count = 0
    for rule in separatedRulesList:
        tempRule = copy.deepcopy(rule)
        tempRule[1].remove('.')
        numbered[key_count] = tempRule
        key_count += 1

    # Start REDUCE procedure
    # Format for follow computation
    addedR = f"{separatedRulesList[0][0]} -> " \
             f"{separatedRulesList[0][1][1]}"
    rules.insert(0, addedR)
    for rule in rules:
        k = rule.split("->")

        # Remove unnecessary spaces
        k[0] = k[0].strip()
        k[1] = k[1].strip()
        rhs = k[1]
        multirhs = rhs.split('|')

        # Remove unnecessary spaces
        for i in range(len(multirhs)):
            multirhs[i] = multirhs[i].strip()
            multirhs[i] = multirhs[i].split()
        diction[k[0]] = multirhs

    # Find 'handle' items and calculate follow.
    for stateno in statesDict:
        for rule in statesDict[stateno]:
            if rule[1][-1] == '.':

                # Match the item
                temp2 = copy.deepcopy(rule)
                temp2[1].remove('.')
                for key in numbered:
                    if numbered[key] == temp2:

                        # Put Rn in those ACTION symbol columns,
                        # who are in the follow of LHS of the current Item.
                        follow_result = follow(rule[0])
                        for col in cols:
                            index = cols.index(col)
                            if key == 0 and col == '$':
                                Table[stateno][index] = "Accept"
                            elif col in follow_result:
                                Table[stateno][index] = f"R{key} "

                        # Add the reduction action to all terminal elements in the row
                        if key != 0:
                            for col in cols:
                                if col in T:
                                    index = cols.index(col)
                                    Table[stateno][index] = f"R{key} "

    # Printing table
    print("\nLR(0) parsing table:\n")
    frmt = "{:>8}" * len(cols)
    print(" ", frmt.format(*cols), "\n")
    ptr = 0
    j = 0
    for y in Table:
        frmt1 = "{:>8}" * len(y)
        print(f"{{:>3}} {frmt1.format(*y)}"
              .format('I' + str(j)))
        j += 1

def printResult(rules):
    for rule in rules:
        print(f"{rule[0]} ->"
              f" {' '.join(rule[1])}")

def printAllGOTO(diction):
    for itr in diction:
        print(f"GOTO ( I{itr[0]} ,"
              f" {itr[1]} ) = I{stateMap[itr]}")

rules = ["D -> var L : T ;",
		"T -> integer | real",
		"L -> L , id | id",
		]
nonterm_userdef = ['D', 'T', 'L']
term_userdef = [',', ':', ';', 'id', 'integer', 'real', 'var']
start_symbol = nonterm_userdef[0]

# Rules section - *END*
print("\nOriginal grammar input:\n")
for y in rules:
    print(y)

# Print processed rules
print("\nGrammar after Augmentation: \n")
separatedRulesList = \
    grammarAugmentation(rules,
                        nonterm_userdef,
                        start_symbol)
printResult(separatedRulesList)

# Find closure
start_symbol = separatedRulesList[0][0]
print("\nCalculated closure: I0\n")
I0 = findClosure(0, start_symbol)
printResult(I0)

############################################################################################################
# Use statesDict to store the states
# Use stateMap to store GOTOs
statesDict = {}
stateMap = {}

# Add the first state to statesDict
# And maintain stateCount
# For newState generation
statesDict[0] = I0
stateCount = 0

# Computing states by GOTO
generateStates(statesDict)

# Print GOTO states
print("\nStates Generated: \n")
for st in statesDict:
    print(f"State = I{st}")
    printResult(statesDict[st])
    print()

print("Result of GOTO computation:\n")
printAllGOTO(stateMap)

# "Follow computation" for making REDUCE entries
diction = {}

# Call createParseTable function
createParseTable(statesDict, stateMap,
                 term_userdef,
                 nonterm_userdef)

import pygraphviz as pgv
from PIL import Image

# Create a PyGraphviz graph object
graph = pgv.AGraph(strict=False, directed=True)

# Add nodes for each state
for state, rules in statesDict.items():
    label = f"I{state}\n"
    label += "\n".join([f"{rule[0]} -> {' '.join(rule[1])}" for rule in rules])
    graph.add_node(state, label=label)

# Add edges for transitions (GOTO)
for (source_state, symbol), target_state in stateMap.items():
    graph.add_edge(source_state, target_state, label=symbol)

# Define the output file name and format (e.g., PNG)
output_file = "lr0_automaton.png"
graph.draw(output_file, prog="dot", format="png")

# Display the generated diagram (optional)
img = Image.open(output_file)
img.show()

print(f"Automaton diagram saved to {output_file}")
