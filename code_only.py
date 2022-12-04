class Die:
    def __init__(self, up, north, east): 
        # key contraint
        sumOfdie = 7

        self.up = up
        self.north = north
        self.east = east
        self.down = sumOfdie - up
        self.south = sumOfdie - north
        self.west = sumOfdie - east
    
    def move_right(self):
        up = self.up
        east = self.east
        down = self.down
        west = self.west
        
        self.up = west
        self.east = up
        self.down = east
        self.west = down

    def move_left(self):
        up = self.up
        east = self.east
        down = self.down
        west = self.west

        self.up = east
        self.east = down
        self.down = west
        self.west = up

    def move_up(self):
        up = self.up
        north = self.north 
        down = self.down
        south = self.south 

        self.up = south
        self.north = up
        self.down = north
        self.south = down

    def move_down(self):
        up = self.up
        north = self.north 
        down = self.down
        south = self.south 

        self.up = north
        self.north = down
        self.down = south
        self.south = up

class Solution: 
    def dieAgony(self):

        array = [[57, 33, 132, 268, 492, 732], 
                [81, 123, 240, 443, 353, 508],
                [186, 42, 195, 704, 452, 228],
                [-7, 2, 357, 452, 317, 395],
                [5, 23, -4, 592, 445, 620],
                [0, 77, 32, 403, 337, 452]]

        # will be used to make sure we don't take steps back
        Visited = [0, 77, 23, -4]

        # will be used to return answer
        notVisited = [5, 32, 2]

        i, j = 4, 2

        #algorithm
        while i <= 5 and j <= 5 and i >= 0 and j >= 0:

            # initial variable values
            n = 4
            die = Die(-9, 77, -27)
            score_previous = -4
            target = 732

            # target test case accepted 
            if (score_previous == target):
                return sum(notVisited)
            
             # move up declined test case
            if (i != 0) and (score_previous + n*die.south != array[i-1][j]) and (array[i-1][j] not in notVisited):
                notVisited.append(array[i-1][j])
            
            # move down declined test case
            if (i != 5) and (score_previous + n*die.north != array[i+1][j]) and (array[i+1][j] not in notVisited):
                notVisited.append(array[i+1][j])
            
            # move left declined test case
            if (j != 0) and (score_previous + n*die.east != array[i][j-1]) and (array[i][j-1] not in notVisited):
                notVisited.append(array[i][j-1])

            # move right declined test case
            if (j != 5) and (score_previous + n*die.west != array[i][j+1]) and (array[i][j+1] not in notVisited):
                notVisited.append(array[i][j+1])

            # move up accepted test case
            if (i != 0) and (score_previous + n*die.south == array[i-1][j]) and (array[i-1][j] not in Visited):
                score_previous += n*die.south
                Visited.append(array[i-1][j])
                i -= 1
                n += 1
                die.move_up()

            # move down accepted test case
            if (i != 5) and (score_previous + n*die.north == array[i+1][j]) and (array[i+1][j] not in Visited): 
                score_previous += n*die.north
                Visited.append(array[i+1][j])
                i += 1
                n += 1
                die.move_down()

            # move left accepted test case
            if (j != 0) and (score_previous + n*die.east == array[i][j-1]) and (array[i][j-1] not in Visited):
                score_previous += n*die.east
                Visited.append(array[i][j-1])
                j -= 1
                n += 1
                die.move_left()

            # move right accepted test case
            if (j != 5) and (score_previous + n*die.west == array[i][j+1]) and (array[i][j+1] not in Visited):
                score_previous += n*die.west
                Visited.append(array[i][j+1])
                j += 1
                n += 1
                die.move_right()
            
            else:
                return False
        return sum(notVisited)

print(Solution().dieAgony())