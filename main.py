from access_point import csmaCA
from parameters import *

def main():
    # TODO: replace test arrays with traffic generated via poisson
    arrivalsA = [10, 5000, 30000000]
    arrivalsB = [400, 30000000]

    successesA, successesB, collisions = csmaCA(arrivalsA, arrivalsB)
    print("\nCSMA with Collision Avoidance")
    print("-----------------------------------------------------------------")
    print("Number of successful transmissions for A: " + str(successesA))
    print("Number of successful transmissions for B: " + str(successesB))
    print("Number of collisions: " + str(collisions))


if __name__ == '__main__':
    main()