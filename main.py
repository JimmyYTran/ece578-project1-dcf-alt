from parameters import *
from access_point import csmaCA
from station import Station

def main():
    # TODO: replace test arrays with traffic generated via poisson
    arrivalsA = [10, 5000, 30000000]
    arrivalsB = [400, 30000000]

    stationA = Station('A', LAMBDAS[0], arrivalsA)
    stationB = Station('B', LAMBDAS[0], arrivalsB)

    csmaCA(stationA, stationB, False, False)

    print("\nCSMA with Collision Avoidance")
    print("-----------------------------------------------------------------")
    print("Number of successful transmissions for A: " + str(stationA.successes))
    print("Number of successful transmissions for B: " + str(stationB.successes))
    print("Number of collisions for A: " + str(stationA.collisions))
    print("Number of collisions for B: " + str(stationB.collisions))


if __name__ == '__main__':
    main()