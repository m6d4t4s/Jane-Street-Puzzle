"""
Jane Street Puzzle: Die Agony; December 2022

key words from problem statement: 
    
    starts with score of 0; every nth move, score += n*value; 
value is the number on die after move; 
die is only allowed to move into square if its score after the move matches the value in the square.
die cannot be translated or rotated in place in addition to these moves. 
answer to puzzle (ans) is the sum of values in the unvisited squares from the dies journey. 

thoughts: 

    for the six-sided die, opposite faces sum to 7 (key presupposition to solve problem). 
So, since we're starting at 0 in the lower-left hand corner, 
the first step is up to 5 (Problem Solvling Technique: solve a smaller problem).
The face up will be 5 since score(1)= 0 + 1*5; the pair face will be 2-5 (since 2+5=7)
side question: how would we represent die in data structure? Array? Will come back to this.
how do we determine where the 4-3 and 6-1 pairs face? 
judging from the orthogonal options available (-7, 23); the 4-3, 6-1 pairs paradigm doesn't allow a next move;
perhaps there are different numbers other than standard 1-6 die? But, pairs still sum to 7 (key consraint)
Suppose we moved to 23, the face of the number would have to be 9 (since score(2) = score(1) + 2*9)
If the face is 9, then the pair would be -2. 
So far, we have die = [2, 5, -2, 9, ?, ?] representing the opposite-face pairs. 
Our next orthogonal options are (2, -4, 77); below are the corresponding pairs for each scenario:
Remember: (x,y) where x+y=7.
1) 77: (18, 11)[77=23+3*x]
2) 2: (-7, 14)[2=23+3*x]
3) -4: (-9, 16)[-4=23+3*x]
Looking at these numbers, the negative values are too large given the fact that most of the numbers are 
large and positive. 

Suppose we took a different route; we still have 5-2 pair, but we go to -7 instead of 23 (from 5). 
If that's the case, then -7 = 5 + 2*x -> x = -6; then (-6, 13)

pairs_new = [2, 5, -6, 13, ?, ?]
From -7, let's say we go to 2 (186 seems too large); then 2 = -7 + 3*x
then, x = 3 -> (3, 4). 
If that's the case, then 
pairs_new = [2, 5, -6, 13, 3, 4]
Considering we have the prime numbers 2, 3, 5 and 13 in pairs_new, and given the 
prime factorization theorem of mathematics, it appears that pairs_new will be the die we go with. 

To recap, we were told that we have a 6 sided die in the problem statement. 
I don't have an interviewer to ask clarifying questions to, so I did some research
and realized that opposite faces on a die sum to 7. I did not know that beforehand. 
Then, solved a smaller problem by taking initial orthogonal steps to construct hypothetical die. 

So, my constructed die that I am going to use initially to solve problem 
is numbers = [2, 5, -6, 13, 3, 4]. Again, it seems more plausible given lower frequency 
of large, negative numbers in the array compared to the other 3 options. 

To give context on die, I created a cube, origami to help visualize the cube and 
think of a way to represent die in data structure. Trying to find a pattern. 

1st roll)
The die starts with 13 facing up at array[5][0]
2 is facing array[4][0] (aka north)
4 is facing array[5][1] (aka east)
the die rolls onto 5. 

2nd roll)
5 facing up
4 to east
13 to north
the die rolls onto -7

3rd roll)
-6 facing up
4 to east
5 to north
the die rolls onto 2

4th roll)
3 facing up
-6 to east
5 to north
etc. 

key words (more):
    we have to return the sum of all values of the unvisited squares from the 
    die's journey. My interpretation is that we add orthogonal square values (there's 4 of them:
    up, down, left, right) that we didn't visit to Hash Set (since they can't repeat), and 
    sum all the values in Hash Set. 
    I am assuming the problem statement doesn't mean to sum all the values in the 2-D matrix that are
    not on the path towards 732. 
    Suppose we finished at 2 (on array[3][1] after the 3rd roll), then the HashSet
    would be (77, 23, 186). So we would return, 286 as our answer. We would 
    not sum all the squares except values 0, 5, -7, and 2, and return that as our answer. 
    That's how I interpret the problem statement.

variables for algorithm: 
    start at array[3][1] (since this is the path we used to determine die)
    "score_previous": initialize to array[3][1]
    "score_next": would equal score_previous + n*value
    "n": determine which move
    "i, j": array[i][j]
    numbers:
        the numbers will be represented with directions
            1) north
            2) south
            3) east
            4) west
            5) up
            6) down
        these numbers will be initialized based on configuration at array[3][1]
        will be updated after each move
    "value": value of number on die
    "hashSet_notVisited": intially empty; numbers added to path that aren't visited. 
    "hashSet_Visited": intially empty; numbers added to path that are visited. 
    "target": set to 732 and break loop once reached and return sum of all values in 
    hashSet

steps for algorithm:
    use while loop to stay within array
    check step:
         i+1: use north as value
         i-1: use south as value
         j+1: use west as value
         j-1: use east as value
    
    if value in square equals score after move, 
        move onto square and append unvisted orthogonal values into hashSet_notVisited
    repeat until we reach target
    return sum of values in hashSet_notVisited
"""
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




"""
class Solution: 
    def dieAgony(self):

        array = [[57, 33, 132, 268, 492, 732], 
                [81, 123, 240, 443, 353, 508],
                [186, 42, 195, 704, 452, 228],
                [-7, 2, 357, 452, 317, 395],
                [5, 23, -4, 592, 445, 620],
                [0, 77, 32, 403, 337, 452]]

        # will be used to make sure we don't take steps back
        Visited = [0, 5, -7, 2]

        # will be used to return answer
        notVisited = [77, 23, 186]

        i, j = 3, 1

        #algorithm
        while i <= 5 and j <= 5 and i >= 0 and j >= 0:

            # initial variable values
            n = 4
            die = Die(3, 5, -6)
            score_previous = 2
            target = 732

            # target test case accepted 
            if (score_previous == target):
                return sum(notVisited)
            
             # move up declined test case
            if (score_previous + n*die.south != array[i-1][j]) and (array[i-1][j] not in notVisited):
                notVisited.append(array[i-1][j])
            
            # move down declined test case
            if (score_previous + n*die.north != array[i+1][j]) and (array[i+1][j] not in notVisited):
                notVisited.append(array[i+1][j])
            
            # move left declined test case
            if (score_previous + n*die.east != array[i][j-1]) and (array[i][j-1] not in notVisited):
                notVisited.append(array[i][j-1])

            # move right declined test case
            if (score_previous + n*die.west != array[i][j+1]) and (array[i][j+1] not in notVisited):
                notVisited.append(array[i][j+1])

            # move up accepted test case
            if (score_previous + n*die.south == array[i-1][j]) and (array[i-1][j] not in Visited):
                score_previous += n*die.south
                Visited.append(array[i-1][j])
                i -= 1
                n += 1
                die.move_up()

            # move down accepted test case
            if (score_previous + n*die.north == array[i+1][j]) and (array[i+1][j] not in Visited):
                score_previous += n*die.north
                Visited.append(array[i+1][j])
                i += 1
                n += 1
                die.move_down()

            # move left accepted test case
            if (score_previous + n*die.east == array[i][j-1]) and (array[i][j-1] not in Visited):
                score_previous += n*die.east
                Visited.append(array[i][j-1])
                j -= 1
                n += 1
                die.move_left()

            # move right accepted test case
            if (score_previous + n*die.west == array[i][j+1]) and (array[i][j+1] not in Visited):
                score_previous += n*die.west
                Visited.append(array[i][j+1])
                j += 1
                n += 1
                die.move_right()
            
            else:
                return sum(notVisited)
        return sum(notVisited)

print(Solution().dieAgony())
"""


"""
I honestly thought I would get this on the first try. Considering this was the first time
I implemented Object-Oriented Programming by constructing the Die Class, it would have been
remarkable if I solved the puzzle with two first tries. But, I didn't. 
I double checked my code and the algorithm functions as I wanted it to. However, we still returned false. 
In the beginning, I mentioned that negative values weren't desireable. But, perhaps they are when 
"n" becomes very large. Looking at the other 3 options:
1) 77: (18, 11)[77=23+3*x]
2) 2: (-7, 14)[2=23+3*x]
3) -4: (-9, 16)[-4=23+3*x]

For our second try, we will go with number 2. So, 
die_pairs = [[2,5], [-2, 9], [-7, 14]]. In that scenario, 
we go up, right, up. We would still start at array[3][1]. 
Visited = [0, 5, 23, 2]
notVisited = [77, -7, -4]
Using the origami cube I created,
Die should be 
up = -7
north = 9
east = 5
Let's code it up!!!

"""
"""
class Solution: 
    def dieAgony(self):

        array = [[57, 33, 132, 268, 492, 732], 
                [81, 123, 240, 443, 353, 508],
                [186, 42, 195, 704, 452, 228],
                [-7, 2, 357, 452, 317, 395],
                [5, 23, -4, 592, 445, 620],
                [0, 77, 32, 403, 337, 452]]

        # will be used to make sure we don't take steps back
        Visited = [0, 5, 23, 2]

        # will be used to return answer
        notVisited = [77, -7, -4]

        i, j = 3, 1

        #algorithm
        while i <= 5 and j <= 5 and i >= 0 and j >= 0:

            # initial variable values
            n = 4
            die = Die(-7, 9, 5)
            score_previous = 2
            target = 732

            # target test case accepted 
            if (score_previous == target):
                return sum(notVisited)
            
             # move up declined test case
            if (score_previous + n*die.south != array[i-1][j]) and (array[i-1][j] not in notVisited):
                notVisited.append(array[i-1][j])
            
            # move down declined test case
            if (score_previous + n*die.north != array[i+1][j]) and (array[i+1][j] not in notVisited):
                notVisited.append(array[i+1][j])
            
            # move left declined test case
            if (score_previous + n*die.east != array[i][j-1]) and (array[i][j-1] not in notVisited):
                notVisited.append(array[i][j-1])

            # move right declined test case
            if (score_previous + n*die.west != array[i][j+1]) and (array[i][j+1] not in notVisited):
                notVisited.append(array[i][j+1])

            # move up accepted test case
            if (score_previous + n*die.south == array[i-1][j]) and (array[i-1][j] not in Visited):
                score_previous += n*die.south
                Visited.append(array[i-1][j])
                i -= 1
                n += 1
                die.move_up()

            # move down accepted test case
            if (score_previous + n*die.north == array[i+1][j]) and (array[i+1][j] not in Visited):
                score_previous += n*die.north
                Visited.append(array[i+1][j])
                i += 1
                n += 1
                die.move_down()

            # move left accepted test case
            if (score_previous + n*die.east == array[i][j-1]) and (array[i][j-1] not in Visited):
                score_previous += n*die.east
                Visited.append(array[i][j-1])
                j -= 1
                n += 1
                die.move_left()

            # move right accepted test case
            if (score_previous + n*die.west == array[i][j+1]) and (array[i][j+1] not in Visited):
                score_previous += n*die.west
                Visited.append(array[i][j+1])
                j += 1
                n += 1
                die.move_right()
            
            else:
                return Visited[-1]
        return sum(notVisited)

print(Solution().dieAgony())
"""

"""
2nd try also returned false. 
Other 2 options:
3) -4: (-9, 16)[-4=23+3*x]
1) 77: (18, -11)[77=23+3*x]

Let's go with 1). 

So, for our third try, we will go with number 1. So, 
die_pairs = [[2,5], [-2, 9], [-11, 18]]. In that scenario, 
we go up, right, down. We would start at array[5][1]. 
Visited = [0, 5, 23, 77]
notVisited = [-7, 2, -4]
Using the origami cube I created,
Die should be 
up = 18
north = -2
east = 5
Let's code it up!!!

"""
"""
class Solution: 
    def dieAgony(self):

        array = [[57, 33, 132, 268, 492, 732], 
                [81, 123, 240, 443, 353, 508],
                [186, 42, 195, 704, 452, 228],
                [-7, 2, 357, 452, 317, 395],
                [5, 23, -4, 592, 445, 620],
                [0, 77, 32, 403, 337, 452]]

        # will be used to make sure we don't take steps back
        Visited = [0, 5, 23, 77]

        # will be used to return answer
        notVisited = [-7, 2, -4]

        i, j = 5, 1

        #algorithm
        while i <= 5 and j <= 5 and i >= 0 and j >= 0:

            # initial variable values
            n = 4
            die = Die(18, -2, 5)
            score_previous = 77
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
                return Visited[-1]
        return sum(notVisited)

print(Solution().dieAgony())
"""

"""
3rd try also returned false. 
But, learned something new!
Forgot to do test case for when we go outside of matrix. 
Solution: 
    add if i, j comparision statements at edges
Other option:
3) -4: (-9, 16)[-4=23+3*x]

Let's go with 3). 

So, for our fourth try, we will go with number 3. So, 
die_pairs = [[2,5], [-2, 9], [-9, 16]]. In that scenario, 
we go up, right, right. We would start at array[4][2]. 
Visited = [0, 5, 23, -4]
notVisited = [-7, 2, 77]
Using the origami cube I created, I was able to discern that the path isn't able to be completed 
since we move up first onto 5, then (after right, right) the new face is forced to be 2 when we need
-9. Therefore, this path is impossible. 

The other paths available to us are: 
1) right, up, right [[-70, 77], [-27, 34], [-9, 16]]; up = -9, north = 77, east = -27
2) right, up, left [[-70, 77], [-27, 34], [-6, 13]]; up = -6, north = 77, east = 34

Let's go with 1). 

So, for our fourth try, we will go with number 1. So, 
die_pairs = [[-70,77], [-27, 34], [-9, 16]]. In that scenario, 
we go right, up, right. We would start at array[4][2]. 
Visited = [0, 77, 23, -4]
notVisited = [5, 32, 2]

Let's code it up!!!

"""


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
                return Visited[-1]
        return sum(notVisited)

print(Solution().dieAgony())



"""
Well, let's try the last one. 
2) right, up, left [[-70, 77], [-27, 34], [-6, 13]]; up = -6, north = 77, east = 34

die_pairs = [[-70,77], [-27, 34], [-6, 13]]. In that scenario, 
we go right, up, left. We would start at array[4][0]. 
Visited = [0, 77, 23, 5]
notVisited = [-4, 32, 2]
previous_value = 5

Let's code it up!!!
"""

"""
class Solution: 
    def dieAgony(self):

        array = [[57, 33, 132, 268, 492, 732], 
                [81, 123, 240, 443, 353, 508],
                [186, 42, 195, 704, 452, 228],
                [-7, 2, 357, 452, 317, 395],
                [5, 23, -4, 592, 445, 620],
                [0, 77, 32, 403, 337, 452]]

        # will be used to make sure we don't take steps back
        Visited = [0, 77, 23, 5]

        # will be used to return answer
        notVisited = [-4, 32, 2]

        i, j = 4, 0

        #algorithm
        while i <= 5 and j <= 5 and i >= 0 and j >= 0:

            # initial variable values
            n = 4
            die = Die(-6, 77, 34)
            score_previous = 5
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
                return Visited[-2]
        return sum(notVisited)

print(Solution().dieAgony())
"""

"""
Went through each algorithm and returned the sum(notVisited) to gauge the most effective
algorithm. The results are as follows (in order written): 
1st: 678
2nd: 488
3rd: 46
4th: 1011
5th: 1011

So, it appears the last two are the closest. Let's focus on the last one. 

"""
"""
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
            score_previous = notVisited[-1]
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
            
            # remove any values from notVisited if we took odd route
            for i in Visited:
                if i in notVisited:
                    notVisited.remove(i)
            
            else:
                return Visited[-1]
        return sum(notVisited)

print(Solution().dieAgony())
"""

"""
Incorporating for loop; the answer becomes 988. 
"""

"""
I went through the the 5 paths and printed out Visited[-1] for them all. Below are the results:
1) 2
2) 2
3) 77
4) -4

It appears my algorithm isn't working. I double checked my approach and it appears that I
might be miss understanding the question prompt. Maybe my assumption for opposite pairs to equal 7
is misguided. However, given my time constraints for application season, 
I will leave my answer the way it is. 

I took 8 hours from start to finish to code, watch OOP tutorial, and navigate Stack OverFlow. 

I wasn't able to solve the problem. But, 
I was able to teach myself OOP from sratch through watching a tutorial and checking 
Stack OverFlow when errors appeared. Overall, this was a great learning experience that helped me
familiarize myself with VSCode/VSCode shortcuts, refine my problem solving framework for the future, 
incorporate Data Structures and Algorithms thought process in program design, 
and learn new python functions/methods. 

Thank you for your time, and I hope you enjoyed a lens into my thinking/coding for my first project!!!
"""