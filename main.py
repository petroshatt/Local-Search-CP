import random
import time
from collections import deque
import copy


# τυχαία αρχικοποίηση λίστας positions
def initPositions(positions):

    for i in range(0, n):
        positions[i] = random.randint(1, n)

    return positions


# λαμβάνει υπόψη τους περιορισμούς σειράς για όλη τη σκακιέρα
def boardRowConflicts(positions):

    conflicts_count = 0
    for i in range(len(positions)):
        conflicts_count += positions.count((positions[i])) - 1
    return int(conflicts_count / 2)


# λαμβάνει υπόψη τους περιορισμούς διαγωνίου για όλη τη σκακιέρα
def boardDiagConflicts(positions):

    conflicts_count = 0
    for i in range(len(positions)):
        for j in range(len(positions)):
            diff = abs(i - j)
            if diff != 0:           #αποφεύγει το εαυτό του
                if positions[i] == (positions[j] - diff):
                    conflicts_count += 1
    return conflicts_count


# υπολογίζει το σύνολο των συγκρούσεων της σκακιέρας
def calcBoardConflicts(conflicts, positions):

    board_conflicts = 0

    for i in range(0, len(positions)):
        for j in range(0, len(positions)):

            temp_positions = positions.copy()
            temp_positions[i] = j + 1

            row_conflicts = boardRowConflicts(temp_positions)
            diag_conflicts = boardDiagConflicts(temp_positions)
            queen_conflicts = row_conflicts + diag_conflicts
            conflicts[j][i] = queen_conflicts
            board_conflicts += queen_conflicts

    return conflicts, board_conflicts


# υπολογίζει το σύνολο των συγκρούσεων όλων των βασιλισσών
def totalQueenConflicts(conflicts, positions):

    totalConflicts = 0
    for i in range(0, len(positions)):
        totalConflicts += calcQueenConflicts(i, positions)
    return totalConflicts


# λαμβάνει υπόψη τους περιορισμούς σειράς για συγκεκριμένη βασίλισσα
def queenRowConflicts(queenPos, positions):

    conflicts_count = positions.count(positions[queenPos]) - 1
    return conflicts_count


# λαμβάνει υπόψη τους περιορισμούς διαγωνίου για συγκεκριμένη βασίλισσα
def queenDiagConflicts(queenPos,positions):

    conflicts_count = 0
    for j in range(len(positions)):
        diff = abs(queenPos - j)
        if diff != 0:               #αποφεύγει το εαυτό του
            if positions[queenPos] == (positions[j] - diff):
                conflicts_count += 1
            if positions[queenPos] == (positions[j] + diff):
                conflicts_count += 1
    return conflicts_count


# υπολογίζει το σύνολο των συγκρούσεων για συγκεκριμένη βασίλισσα
def calcQueenConflicts(queenPos, positions):
    return queenRowConflicts(queenPos, positions) + queenDiagConflicts(queenPos, positions)


# δημιουργεί λίστα με τις βασίλισσες που υπάρχουν σε κάποια σύγκρουση
def findQueensInConflict(conflicts, positions):

    queens_list = []
    for i in range(0, len(positions)):

        queen_conflicts = calcQueenConflicts(i, positions)

        if queen_conflicts > 0:
            queens_list.append(i)

    return queens_list


# δημιουργεί λίστα με τις βασίλισσες που έρχονται σε σύγκρουση με τη συγκεκριμένη βασίλισσα
def findQueensInConflictBetween(queenpos, positions):
    queens_list = []
    for i in range(len(positions)):
        if (queenpos != i):
            if positions[i]==positions[queenpos]:
                queens_list.append(i)

    for j in range(len(positions)):
        diff = abs(queenpos - j)
        if diff != 0:               #αποφεύγει το εαυτό του
            if positions[queenpos] == (positions[j] - diff):
                queens_list.append(j)
            if positions[queenpos] == (positions[j] + diff):
                queens_list.append(j)
    return queens_list


# βοηθητική συνάρτηση στην εύρεση ελαχίστου σε συγκεκριμένη στήλη
# (εφαρμόζεται σε δισδιάστατες λίστες)
def column(matrix, col, pos):
    column = []
    for i in range(0, len(matrix)):
        if i != pos - 1:
            column.append(conflicts[i][col])
    return column


# τυπώνει τη σκακιέρα
def printBoard(conflicts, positions):

    for i in range(len(positions)):
        for j in range(len(positions)):
            if (positions[j] - 1 == i):
                if (conflicts[i][j] < 10):
                    print("\033[96m 0%d \033[0m|" % conflicts[i][j], end="")
                else:
                    print("\033[96m %d \033[0m|" % conflicts[i][j], end="")
            else:
                if (conflicts[i][j] < 10):
                    print(" 0" + str(conflicts[i][j]), "|", end = "")
                else:
                    print("", conflicts[i][j], "|", end = "")
        print()
        line_num = "-----"
        print(line_num * n)


# αλγόριθμος Min-Conflicts
def minConflicts(conflicts, positions, maxTries, maxChanges):

    for tries in range(1, maxTries+1):
        A = positions.copy()
        for changes in range(1, maxChanges+1):
            totalConflicts = totalQueenConflicts(conflicts, A)
            #print(totalConflicts)
            if totalConflicts == 0:
                # print("Solution Found!")
                # print("maxTries:", tries, "maxChanges", changes)
                # return A
                return 1, (changes*tries), totalConflicts
            else:
                x = random.choice(findQueensInConflict(conflicts, A))
                col = column(conflicts, x, A[x])
                cost_a = min(column(conflicts, x, A[x]))
                index_a = int(min(range(len(col)), key=col.__getitem__))

                if cost_a <= conflicts[A[x] - 1][x]:
                    if A[x] - 1 <= index_a:
                        index_a += 1
                    A[x] = index_a + 1
                    conflicts, _ = calcBoardConflicts(conflicts, A)

    # print("No Solution Found!")
    # return A
    return 0, (changes*tries), totalConflicts


# αλγόριθμος Min-Conflicts with Random Walk
def minConflictsWithRandomWalk(conflicts, positions, p, maxTries, maxChanges):

    for tries in range(1, maxTries+1):
        A = positions.copy()
        for changes in range(1, maxChanges+1):
            totalConflicts = totalQueenConflicts(conflicts, A)
            #print(totalConflicts)
            if totalConflicts == 0:     # satisfies P
                # print("\nSolution Found!")
                # print("maxTries:", tries, "maxChanges", changes)
                # return A
                return 1, (changes*tries), totalConflicts
            else:
                x = random.choice(findQueensInConflict(conflicts, A))
                probability = round(random.uniform(0, 0.15), 2)

                if p == probability:
                    index_a = random.randint(0, len(A) - 1)
                else:
                    col = column(conflicts, x, A[x])
                    index_a = int(min(range(len(col)), key=col.__getitem__))

                if A[x] - 1 <= index_a:
                    index_a += 1
                A[x] = index_a + 1
                conflicts, _ = calcBoardConflicts(conflicts, A)

    # print("\nNo Solution Found!")
    # return A
    return 0, (changes* tries), totalConflicts


def breakout(conflicts, positions, maxTries, maxChanges):

    for tries in range(1, maxTries+1):

        A = positions.copy()
        weights = [[1 for i in range(len(positions))] for j in range(len(positions))]

        for changes in range(1, maxChanges+1):
            conflicts, _ = calcBoardConflicts(conflicts, A)
            totalConflicts = totalQueenConflicts(conflicts, A)/2
            # print("totalConflicts", totalConflicts)
            # print("\n\nTries: ", tries, " Changes: ", changes)
            #for w in weights:      #τυπώνει την λίστα weights
            #    print(w)
            if totalConflicts == 0:
                # return A
                return 1, (changes*tries), totalConflicts
            else:
                tmpW = 0
                minW = 9999999
                rand_min = []
                for i in range(len(A)):
                    for j in range(len(A)):
                        tmpA = A.copy()
                        tmpA[i] = j + 1
                        conflicts, _ = calcBoardConflicts(conflicts, tmpA)
                        queenlist = findQueensInConflictBetween(i, tmpA)
                        #print(queenlist)
                        if queenlist:
                            tmpW=0
                            for k in queenlist:
                                tmpW+=weights[i][k]
                                tmpW+=weights[k][i]
                            tmpW += weights[i][j]
                            tmpW += weights[j][i]
                        else:
                            tmpW = weights[i][j] + weights[j][i]

                        if tmpW < minW:
                            # print(tmpW, "tmpW" ,i ,j)
                            minW = tmpW
                            rand_min.clear()
                            rand_min.append((i, j))

                            cost_a = totalQueenConflicts(conflicts, tmpA) / 2
                        elif tmpW == minW:
                            rand_min.append((i, j))
                        #print(i, j, tmpW)
                #print("queen with min sum: (index)", minIndex, "j", pos, "sum:", minW, "cost", cost_a)

                (x, pos) = random.choice(rand_min)

                conflicts, _ = calcBoardConflicts(conflicts, A)
                currentcost = totalQueenConflicts(conflicts, A)/2

                if(cost_a < currentcost):       # γίνεται η ανάθεση
                    A[x] = pos+1
                else:                           # αυξάνονται τα βάρη
                    tmpA = A.copy()
                    tmpA[x] = pos + 1
                    conflicts, _ = calcBoardConflicts(conflicts, tmpA)
                    quenlist2 = findQueensInConflictBetween(x, tmpA)
                    weights[x][pos] += 1
                    weights[pos][x] += 1
                    for m in quenlist2:
                        weights[x][m] += 1
                        weights[m][x] += 1

    # return A
    return 0, (changes*tries), totalConflicts


def tabuSearch(conflicts, positions, maxTries, maxChanges, tabuLength):

    tabu = deque(maxlen=tabuLength)         # δημιουργία ουράς
    tabu.extend([] for w in range(tabuLength))

    for tries in range(1, maxTries+1):
        A = positions.copy()
        best = 999999999
        for changes in range(1, maxChanges+1):
            totalConflicts = totalQueenConflicts(conflicts, A)
            # print(totalConflicts)
            if totalConflicts == 0:

                return 1, (changes * tries), totalConflicts

            else:
                x = random.choice(findQueensInConflict(conflicts, A))
                index_b = A[x] - 1              # η γραμμή της βασίλισσας που προκαλούσε σύγκρουση πριν γίνει η αλλαγή

                col = column(conflicts, x, A[x])
                cost_a = min(column(conflicts, x, A[x]))
                index_a = int(min(range(len(col)), key=col.__getitem__))        # η καλύτερη θέση που μπορεί να πάει η βασίλισσα x

                if ([x, index_a] not in tabu) or ([x, index_a] in tabu and cost_a < best):
                    # if ([x, index_a] not in tabu):
                    if A[x] - 1 <= index_a:             # γίνεται η ανάθεση
                        index_a += 1
                    A[x] = index_a + 1
                    conflicts, _ = calcBoardConflicts(conflicts, A)
                    if cost_a<best:
                        best=cost_a

                    tabu.append([x, index_b])

    # return A
    return 0, (changes * tries), totalConflicts


if __name__ == '__main__':

    n = int(input("Enter n: "))
    positions = [0 for i in range(n)]
    positions = initPositions(positions)


    conflicts = [[0 for i in range(n)] for i in range(n)]
    conflicts, _ = calcBoardConflicts(conflicts, positions)


    maxChanges = int(input("Enter maxChanges: "))
    maxTries = int(input("Enter maxTries: "))
    p = float(input("Enter p: "))
    tabuLength = int(input("Enter tabu length: "))

    printBoard(conflicts, positions)

    # sums = (Λησεις, αλλαγες, συγκρουσης, χρονος)
    sums = [[0, 0, 0, 0.0] for i in range(8)]
    tries = 20
    startTimeTotalnoBO = time.time()
    positionsArray = []
    for i in range(tries):
        positions = initPositions(positions)
        conflicts, _ = calcBoardConflicts(conflicts, positions)

        # Επειδή τρέχουμε τον breakout ξεχωριστά, κρατάμε τις τυχαίες τοποθετήσεις
        # για να τρέξει σε αυτές ο breakout
        positionsArray.append(positions.copy())

        #sums[0] minConflicts με restarts
        print("MCR ", end='')
        startTime = time.time()
        # return 1, (changes*tries+1), totalConflicts
        solutionTmp, changesTmp, conflictsTmp = minConflicts(conflicts, positions, maxTries, maxChanges)
        sums[0][0] += solutionTmp
        sums[0][1] += changesTmp
        sums[0][2] += conflictsTmp
        sums[0][3] += time.time() - startTime
        # print(sums[0])



        print("MC ", end='')
        # sums[1] minConflicts χωρις restarts
        conflicts, _ = calcBoardConflicts(conflicts, positions)
        startTime = time.time()
        solutionTmp, changesTmp, conflictsTmp = minConflicts(conflicts, positions, 1, maxChanges,) # no restarts
        sums[1][0] += solutionTmp
        sums[1][1] += changesTmp
        sums[1][2] += conflictsTmp
        sums[1][3] += time.time() - startTime
        # print(sums[1])

        print("MCWR ", end='')
        # sums[2] minConflicts randomWalk με restarts
        conflicts, _ = calcBoardConflicts(conflicts, positions)
        startTime = time.time()
        solutionTmp, changesTmp, conflictsTmp = minConflictsWithRandomWalk(conflicts, positions, p, maxTries, maxChanges)
        sums[2][0] += solutionTmp
        sums[2][1] += changesTmp
        sums[2][2] += conflictsTmp
        sums[2][3] += time.time() - startTime
        # print(sums[2])

        print("MCW ", end='')
        # sums[3] minConflicts randomWalk χωρις restarts
        conflicts, _ = calcBoardConflicts(conflicts, positions)
        startTime = time.time()
        solutionTmp, changesTmp, conflictsTmp = minConflictsWithRandomWalk(conflicts, positions, p, 1, maxChanges)
        sums[3][0] += solutionTmp
        sums[3][1] += changesTmp
        sums[3][2] += conflictsTmp
        sums[3][3] += time.time() - startTime
        # print(sums[3])



        print("TR ", end='')
        # sums[6] tabu με restarts
        conflicts, _ = calcBoardConflicts(conflicts, positions)
        startTime = time.time()
        solutionTmp, changesTmp, conflictsTmp = tabuSearch(conflicts, positions, maxTries, maxChanges, tabuLength)
        sums[4][0] += solutionTmp
        sums[4][1] += changesTmp
        sums[4][2] += conflictsTmp
        sums[4][3] += time.time() - startTime
        # print(sums[6])

        print("T ", end='')
        # sums[7] tabu χωρις restarts
        conflicts, _ = calcBoardConflicts(conflicts, positions)
        startTime = time.time()
        solutionTmp, changesTmp, conflictsTmp = tabuSearch(conflicts, positions, 1, maxChanges, tabuLength)
        sums[5][0] += solutionTmp
        sums[5][1] += changesTmp
        sums[5][2] += conflictsTmp
        sums[5][3] += time.time() - startTime
        # print(sums[7])
        print()
    TimeTotalnoBO = time.time() - startTimeTotalnoBO


    print()
    # sums = (Λησεις, αλλαγες, συγκρουσης, χρονος)
    dum = [" MCR", "  MC", "MCWR", " MCW", "  TR", "   T", " BOR", "  BO"]
    print("n: %d, maxChanges: %d, maxTries: %d, p: %.2f, tabuLen:%d" % (n, maxChanges, maxTries, p, tabuLength))
    print("\t Λύσεις Αλλαγές Συγκρούσεις Χρόνος")
    for i in range(6):
        print(" %s \t  %d \t %.1f \t %.1f \t     %.3f" % (dum[i], sums[i][0], sums[i][1]/tries, sums[i][2]/tries, sums[i][3]/tries))
    print("Execution Time: %.3fs" % TimeTotalnoBO)


    timeTotal = 0.0
    ans = input("Press enter to proceed to breakout (input 'n' for no): ")
    if not ans:
        print("Running breakout separately from other algorithms but on the same random starting positions")
        startTimeTotal = time.time()
        for positions in positionsArray:

            print("BOR ", end='')
            # sums[4] breakout με restarts
            conflicts, _ = calcBoardConflicts(conflicts, positions)
            startTime = time.time()
            solutionTmp, changesTmp, conflictsTmp = breakout(conflicts, positions, maxTries, maxChanges)
            sums[6][0] += solutionTmp
            sums[6][1] += changesTmp
            sums[6][2] += conflictsTmp
            sums[6][3] += time.time() - startTime
            # print(sums[4])

            print("BO ", end='')
            # sums[5] breakout χωρις restarts
            conflicts, _ = calcBoardConflicts(conflicts, positions)
            startTime = time.time()
            solutionTmp, changesTmp, conflictsTmp = breakout(conflicts, positions, 1, maxChanges)
            sums[7][0] += solutionTmp
            sums[7][1] += changesTmp
            sums[7][2] += conflictsTmp
            sums[7][3] += time.time() - startTime
            # print(sums[5])
            print()
        timeTotal = time.time() - startTimeTotal
        print()
        print("n: %d, maxChanges: %d, maxTries: %d, p: %.2f, tabuLen:%d" % (n, maxChanges, maxTries, p, tabuLength))
        print("\t Λύσεις Αλλαγές Συγκρούσεις Χρόνος")
        for i in range(8):
            print(" %s \t  %d \t %.1f \t %.1f \t     %.3f" % (dum[i], sums[i][0], sums[i][1]/tries, sums[i][2]/tries, sums[i][3]/tries))
        print("6 algorithms execution Time: %.3fs" % TimeTotalnoBO)
        print("Breakout execution time: %.3fs" % timeTotal)

    print("Total execution time: %.3fs" % (TimeTotalnoBO + timeTotal))
    input()
    print("Exiting")