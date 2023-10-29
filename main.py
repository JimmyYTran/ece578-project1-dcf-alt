from parameters import *
from access_point import csmaCA
from station import Station

def main():

    user_input = ""
    while (not user_input.isnumeric()):
        user_input = input("\nEnter a frame rate (100, 200, 300, 500, 800, 1000): ")
    frame_rate = int(user_input)

    stationA = Station('A', frame_rate)
    stationB = Station('B', frame_rate)
    
    csmaCA(stationA, stationB, False, False)

    print("\n\nCSMA (Shared Collision Domain, No VCS)")
    print("-----------------------------------------------------------------------")
    print("Number of successful transmissions for A: " + str(stationA.successes))
    print("Number of successful transmissions for B: " + str(stationB.successes))
    print("Number of collisions counted by A: " + str(stationA.collisions))
    print("Number of collisions counted by B: " + str(stationB.collisions))

    stationA = Station('A', frame_rate)
    stationB = Station('B', frame_rate)
    csmaCA(stationA, stationB, True, False)

    print("\n\nCSMA (Hidden Terminals, No VCS)")
    print("-----------------------------------------------------------------------")
    print("Number of successful transmissions for A: " + str(stationA.successes))
    print("Number of successful transmissions for B: " + str(stationB.successes))
    print("Number of collisions counted by A: " + str(stationA.collisions))
    print("Number of collisions counted by B: " + str(stationB.collisions))

    stationA = Station('A', frame_rate)
    stationB = Station('B', frame_rate)
    csmaCA(stationA, stationB, False, True)

    print("\n\nCSMA (Shared Collision Domain, VCS Enabled)")
    print("-----------------------------------------------------------------------")
    print("Number of successful transmissions for A: " + str(stationA.successes))
    print("Number of successful transmissions for B: " + str(stationB.successes))
    print("Number of collisions counted by A: " + str(stationA.collisions))
    print("Number of collisions counted by B: " + str(stationB.collisions))

    stationA = Station('A', frame_rate)
    stationB = Station('B', frame_rate)
    csmaCA(stationA, stationB, True, True)

    print("\n\nCSMA (Hidden Terminals, VCS Enabled)")
    print("-----------------------------------------------------------------------")
    print("Number of successful transmissions for A: " + str(stationA.successes))
    print("Number of successful transmissions for B: " + str(stationB.successes))
    print("Number of collisions counted by A: " + str(stationA.collisions))
    print("Number of collisions counted by B: " + str(stationB.collisions))

if __name__ == '__main__':
    main()