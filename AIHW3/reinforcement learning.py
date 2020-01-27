#AI Assignment 3
import numpy as np

#Take input line by line
file=open("input.txt","r")
content = file.readlines()
content = [x.strip() for x in content]

#Parse input
n = int(content[0])
c = int(content[1])
o = int(content[2])

obsY = [0] * o
obsX = [0] * o
startsY = [0] * c
startsX = [0] * c
endsY = [0] * c
endsX = [0] * c

contentPtr = 3

for i in range(o):
    coorVal = content[contentPtr].split(",")
    obsY[i] = int(coorVal[0])
    obsX[i] = int(coorVal[1])
    contentPtr += 1

for i in range(c):
    coorVal = content[contentPtr].split(",")
    startsY[i] = int(coorVal[0])
    startsX[i] = int(coorVal[1])
    contentPtr += 1

for i in range(c):
    coorVal = content[contentPtr].split(",")
    endsY[i] = int(coorVal[0])
    endsX[i] = int(coorVal[1])
    contentPtr += 1

#Creating output file
f = open("output.txt", "w")

#Creating grid
grid = []
for i in range(n):
    row = []
    for j in range(n):
        row.append([-1,0])
    grid.append(row)

#Updating grid with obstacles
for i in range(o):
    obX = obsX[i]
    obY = obsY[i]
    grid[obX][obY][0] = -101
    grid[obX][obY][1] = -101

#Creating temporary grid
tempGrid = []
for i in range(n):
    row = []
    for j in range(n):
        row.append([0,0])
    tempGrid.append(row)

#Creating policy grid
policyGrid = []
for i in range(n):
    row = []
    for j in range(n):
        row.append("Exit")
    policyGrid.append(row)

#Function for north from given state
def north(coorX,coorY):
    if(coorX==0):
        return grid[coorX][coorY][1]
    else:
        return grid[coorX-1][coorY][1]

#Function for south from given state
def south(coorX,coorY):
    if(coorX==(n-1)):
        return grid[coorX][coorY][1]
    else:
        return grid[coorX+1][coorY][1]

#Function for east from given state
def east(coorX,coorY):
    if(coorY==(n-1)):
        return grid[coorX][coorY][1]
    else:
        return grid[coorX][coorY+1][1]

#Function for west from given state
def west(coorX,coorY):
    if(coorY==0):
        return grid[coorX][coorY][1]
    else:
        return grid[coorX][coorY-1][1]

#Utility Function
def utility(coorX,coorY):
    goNorth = (0.7*north(coorX,coorY))+(0.1*south(coorX,coorY))+(0.1*east(coorX,coorY))+(0.1*west(coorX,coorY))
    goSouth = (0.1*north(coorX,coorY))+(0.7*south(coorX,coorY))+(0.1*east(coorX,coorY))+(0.1*west(coorX,coorY))
    goEast = (0.1*north(coorX,coorY))+(0.1*south(coorX,coorY))+(0.7*east(coorX,coorY))+(0.1*west(coorX,coorY))
    goWest = (0.1*north(coorX,coorY))+(0.1*south(coorX,coorY))+(0.1*east(coorX,coorY))+(0.7*west(coorX,coorY))
    utilVal = grid[coorX][coorY][0]+(0.9*max(goNorth,goSouth,goEast,goWest))
    return utilVal

#Function to check if differences are less than or equal to 0.1
def checkDiff(givenTempGrid):
    for i in range(n):
        flag = 0
        for j in range(n):
            if(givenTempGrid[i][j][1]>(0.1/9)):
                flag = 1
                break
        if(flag==1):
            break
    if(flag==1):
        return True
    else:
        return False

#Function to calculate policy for a grid location
def getPolicy(coorX,coorY):
    goNorth = (0.7*north(coorX,coorY))+(0.1*south(coorX,coorY))+(0.1*east(coorX,coorY))+(0.1*west(coorX,coorY))
    goSouth = (0.1*north(coorX,coorY))+(0.7*south(coorX,coorY))+(0.1*east(coorX,coorY))+(0.1*west(coorX,coorY))
    goEast = (0.1*north(coorX,coorY))+(0.1*south(coorX,coorY))+(0.7*east(coorX,coorY))+(0.1*west(coorX,coorY))
    goWest = (0.1*north(coorX,coorY))+(0.1*south(coorX,coorY))+(0.1*east(coorX,coorY))+(0.7*west(coorX,coorY))
    direction = np.array([goNorth,goSouth,goEast,goWest])
    dirIndex = np.argmax(direction)
    if(dirIndex==0):
        return "North"
    elif(dirIndex==1):
        return "South"
    elif(dirIndex==2):
        return "East"
    elif(dirIndex==3):
        return "West"

#Implementing turn_left and turn_right
def turn_right(givenMove):
    if(givenMove=="North"):
        return "East"
    elif(givenMove=="East"):
        return "South"
    elif(givenMove=="South"):
        return "West"
    elif(givenMove=="West"):
        return "North"

def turn_left(givenMove):
    if(givenMove=="North"):
        return "West"
    elif(givenMove=="West"):
        return "South"
    elif(givenMove=="South"):
        return "East"
    elif(givenMove=="East"):
        return "North"

#Function to make the move
def makeMove(coorX,coorY,givenMove):
    if(givenMove=="North"):
        if(coorX==0):
            return list([coorX,coorY])
        else:
            return list([coorX-1,coorY])
    elif(givenMove=="South"):
        if(coorX==(n-1)):
            return list([coorX,coorY])
        else:
            return list([coorX+1,coorY])
    elif(givenMove=="East"):
        if(coorY==(n-1)):
            return list([coorX,coorY])
        else:
            return list([coorX,coorY+1])
    elif(givenMove=="West"):
        if(coorY==0):
            return list([coorX,coorY])
        else:
            return list([coorX,coorY-1])

#Running for each car
for m in range(c):
    #Starting and ending locations
    startX = startsX[m]
    startY = startsY[m]
    endX = endsX[m]
    endY = endsY[m]

    #Updating reward for end location
    grid[endX][endY][0] = 99
    grid[endX][endY][1] = 99

    #Running first iteration of utility functions
    for i in range(n):
        for j in range(n):
            if(not(i==endX and j==endY)):
                tempGrid[i][j][0] = utility(i,j)

    for i in range(n):
        for j in range(n):
            if(not(i==endX and j==endY)):
                tempGrid[i][j][1] = abs(grid[i][j][1]-tempGrid[i][j][0])
                grid[i][j][1] = tempGrid[i][j][0]

    #Running subsequent iterations of utility functions
    while(checkDiff(tempGrid)):
        for i in range(n):
            for j in range(n):
                if(not(i==endX and j==endY)):
                    tempGrid[i][j][0] = utility(i,j)

        for i in range(n):
            for j in range(n):
                if(not(i==endX and j==endY)):
                    tempGrid[i][j][1] = abs(grid[i][j][1]-tempGrid[i][j][0])
                    grid[i][j][1] = tempGrid[i][j][0]

    #Calculate policy for each location
    for i in range(n):
        for j in range(n):
            if(not(i==endX and j==endY)):
                policyGrid[i][j] = getPolicy(i,j)

    #Running the car simulation

    reward = [0]*10

    for i in range(10):
        posX = startX
        posY = startY
        np.random.seed(i)
        swerve = np.random.random_sample(1000000)
        k = 0
        while(not(posX==endX and posY==endY)):
            move = policyGrid[posX][posY]
            if(swerve[k]>0.7):
                if(swerve[k]>0.8):
                    if(swerve[k]>0.9):
                        move = turn_right(turn_right(move))
                    else:
                        move = turn_right(move)
                else:
                    move = turn_left(move)
            newPos = makeMove(posX,posY,move)
            posX = newPos[0]
            posY = newPos[1]
            reward[i] += grid[posX][posY][0]
            k += 1

    reward = np.array(reward,dtype=np.float64)
    result = int(np.floor(np.average(reward)))
    print(result)
    f.write(str(result)+'\n')

    #Reset the grid
    for i in range(n):
        for j in range(n):
            if(grid[i][j][0]==-101):
                grid[i][j][1] = -101
            else:
                grid[i][j][0] = -1
                grid[i][j][1] = 0

    #Reset temporary grid
    for i in range(n):
        for j in range(n):
            tempGrid[i][j][0] = 0
            tempGrid[i][j][1] = 0

    #Reset policy grid
    for i in range(n):
        for j in range(n):
            policyGrid[i][j] = "Exit"
