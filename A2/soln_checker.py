# author 4n1rudh4
# created on: 2021-26-10
# check if solution satisfies following constraints
# 1. No nurse can cover more than one shift on a single day.
# 2. A nurse should not be allocated to work in two consecutive morning shifts (M).
# 3. A nurse cannot work in a morning shift (M) if he/she took the evening shift (E) the preceding day.
# 4. The shift coverage requirements are that there should be exactly (m) nurses in the morning shift, (a) nurses in the afternoon shift and (e) nurses in the evening shift every day. Note that  (m + a + e) <= N.
# 5. The hospital must ensure that each nurse gets at least one rest day in a week.

# read json
import json
import sys

with open("solution.json") as json_file:
    for line in json_file:
        data = json.loads(line)
        if data == {}:
            print("No solution found")
            continue
        key = list(data.keys())
        last_element = key[-1]
        # extract integer before _ from 'N20_6'
        N = int(last_element.split('_')[0][1:])+1
        # extract integer after _ from 'N20_6'
        D = int(last_element.split('_')[1][:])+1
        print("Nurses", N, "Days", D)
        # condition 1:
        # automatically satisfied.
        # condition 2:
        for nurse in range(N):
            for day in range(1, D):
                if data["N"+str(nurse)+'_'+str(day)] == "M":
                    if data["N"+str(nurse)+'_'+str(day-1)] == "M":
                        print("Nurse "+str(nurse) +
                              " is assigned to two consecutive shifts on day "+str(day))
                        sys.exit(1)
        # condition 3:
        for nurse in range(N):
            for day in range(1, D):
                if data["N"+str(nurse)+'_'+str(day)] == "M":
                    if data["N"+str(nurse)+'_'+str(day-1)] == "E":
                        print("Nurse "+str(nurse) +
                              " is assigned to morning shift on day "+str(day)+" and evening shift on day "+str(day-1))
                        sys.exit(1)
        # condition 4:
        for day in range(D):
            mornings = 0
            afternoons = 0
            evenings = 0
            for nurse in range(N):
                if data["N"+str(nurse)+'_'+str(day)] == "M":
                    mornings += 1
                elif data["N"+str(nurse)+'_'+str(day)] == "A":
                    afternoons += 1
                elif data["N"+str(nurse)+'_'+str(day)] == "E":
                    evenings += 1
            if mornings+afternoons+evenings > N:
                print("Mornings:", mornings, "Afternoons:",
                      afternoons, "Evenings:", evenings)

                print("More nurses assigned to shifts on day "+str(day))
                sys.exit(1)
        # condition 5:
        for nurse in range(N):
            for dayLeft in range(D):
                flag = False
                if dayLeft+7 <= D:
                    for datRight in range(dayLeft, dayLeft+7):
                        if data["N"+str(nurse)+'_'+str(datRight)] == "R":
                            flag = True
                            break
                    if flag == False:
                        print("Nurse "+str(nurse) +
                              " is not assigned to rest day on day "+str(dayLeft))
                        sys.exit(1)
        print("Solution is valid")
