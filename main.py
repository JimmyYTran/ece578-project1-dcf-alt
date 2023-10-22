from parameters import *
from access_point import csmaCA
from station import Station

def main():
    arrivalsA = [10, 400, 500, 600, 700, 800, 5000, 30000000]
    arrivalsB = [10, 100, 300, 400, 500, 600, 30000000]

    stationA = Station('A', LAMBDAS[0], arrivalsA)
    stationB = Station('B', LAMBDAS[0], arrivalsB)

    csmaCA(stationA, stationB, False, False)

    print("\nCSMA with Collision Avoidance")
    print("-----------------------------------------------------------------")
    print("Number of successful transmissions for A: " + str(stationA.successes))
    print("Number of successful transmissions for B: " + str(stationB.successes))
    print("Number of collisions counted by A: " + str(stationA.collisions))
    print("Number of collisions counted by B: " + str(stationB.collisions))


if __name__ == '__main__':
    main()