def check(X, param):
    if not len(X):
        # print("\nERROR\n")
        return False
    correct = True
    for r in range(len(X)):
        for c in range(len(X[0])):
            if (r >= 1):
                correct = arc_valid(X[r-1][c], X[r][c], X, param)
                if not correct:
                    return False
            if (c >= 1):
                correct = arc_valid(X[r][c-1], X[r][c], X, param)
                if not correct:
                    return False
            if (c+1) % 7 == 0:
                r_found = False
                for day in range(7):
                    if X[r][c-day].value == 'R':
                        r_found = True
                        break
                if not r_found:
                    return False
    return True
