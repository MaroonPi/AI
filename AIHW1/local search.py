import operator
#Create and initialize grid with given number

file=open("input.txt","r")
content = file.readlines()
content = [x.strip() for x in content]

n = int(content[0])
police = int(content[1])

currentIndex = 0
endIndex = police - 1
tempIndex = police - 1

grid = []

for x in range(n):
    row = []
    grid.append(row)
    for y in range(n):
        row.append([0,False])

#Reading each coordinate and incrementing corresponding value in grid
for x in range(3,len(content)):
    coorVal=content[x].split(",");
    coorX = int(coorVal[0]);
    coorY = int(coorVal[1]);
    grid[coorX][coorY][0]+=1;

#Creating dictionary
d = {}
for x in range(n):
    for y in range(n):
        d[(x,y)] = grid[x][y][0]

#Sorting dictionary
sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)

for i in range(len(sorted_d)):
    sorted_d[i] = list(sorted_d[i])
    sorted_d[i][0] = list(sorted_d[i][0])

ptrList = [0]*police
for i in range(police):
    ptrList[i] = i

#Function to check rows, columns and diagonals
def checkGrid(XCoor,YCoor):
    for j in range(n):
        if(grid[XCoor][j][1]==True and j!=YCoor):
            return False
    for i in range(n):
        if(grid[i][YCoor][1]==True and i!=XCoor):
            return False
    for i,j in zip(range(XCoor,-1,-1),range(YCoor,-1,-1)):
        if(grid[i][j][1]==True and i!=XCoor and j!=YCoor):
            return False
    for i,j in zip(range(XCoor,-1,-1),range(YCoor,n,1)):
        if(grid[i][j][1]==True and i!=XCoor and j!=YCoor):
            return False
    for i,j in zip(range(XCoor,n,1),range(YCoor,-1,-1)):
        if(grid[i][j][1]==True and i!=XCoor and j!=YCoor):
            return False
    for i,j in zip(range(XCoor,n,1),range(YCoor,n,1)):
        if(grid[i][j][1]==True and i!=XCoor and j!=YCoor):
            return False
    return True

#Place police on the board
for i in range(police):
    x = sorted_d[ptrList[i]][0][0]
    y = sorted_d[ptrList[i]][0][1]
    grid[x][y][1] = True

#Check value for each
while(currentIndex<=endIndex and tempIndex<(n*n)):
    x = sorted_d[ptrList[currentIndex]][0][0]
    y = sorted_d[ptrList[currentIndex]][0][1]
    if(checkGrid(x,y)==True):
        currentIndex += 1
    else:
        tempIndex += 1
        grid[x][y][1] = False
        if(tempIndex<(n*n)):
            x_next = sorted_d[tempIndex][0][0]
            y_next = sorted_d[tempIndex][0][1]
            grid[x_next][y_next][1] = True
            ptrList[currentIndex] = tempIndex

#Result
result = 0
officers = 0

for x in range(n):
    for y in range(n):
        if(grid[x][y][1]):
            result += grid[x][y][0]
            officers += 1

outFile = open("output.txt","w")
outFile.write(str(result))
