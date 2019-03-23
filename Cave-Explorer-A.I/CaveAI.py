from Agent import Agent
from random import randrange
from math import sqrt

class MyAI ( Agent ):

    def __init__ ( self ):
        #we update these x_limit and y_limit coordinates as we progress through the game
        #for now we assume that the limit is 10 since the max it can be is 7x7, the starting adjacent tiles will be valid
        self.X_LIMIT = 1000# contains upper boundary for X-coordinate
        self.Y_LIMIT = 1000#contains upper boundary for Y-coordinate
        self._return = False
        self.x_loc = 0
        self.y_loc = 0
        self.facing = 0 # +1 = turn right, -1 turn left. mod it by 4
        self.arrow = True
        self.gold = False
        self.move_queue = []
        self.safe_spaces = set()
        self.wumpus_local = tuple()
        self.recent_moves = []
        self.wumpus_dead = False
        self.undiscovered_count = 0
        self.MASTER_DICTIONARY = dict() #form in (tuple : int) (x,y) : score
        self.undiscovered = set([(0,1), (1,0)])

 
    def getAction( self, stench, breeze, glitter, bump, scream ): #if on 0, 0, no point going to -1, 0 or 0, -1
        if len(self.undiscovered) == 0:
            self._return = True

        self.purgeUndiscovered()  # steps on 0,1 purges and triggers return

        if scream:
            self.wumpus_dead = True

        if glitter:
            self._return = True
            self.gold = True
            return Agent.Action.GRAB #if grab gold, dont care about number of moves
            
        elif (self._return == True) and (self.x_loc == 0 and self.y_loc == 0):
            return Agent.Action.CLIMB

        elif (breeze) and (self.x_loc == 0 and self.y_loc == 0):
            return Agent.Action.CLIMB

        elif (stench) and (self.x_loc == 0 and self.y_loc == 0) and self.arrow == True:
            self.arrow = False
            return Agent.Action.SHOOT

        elif (stench) and (self.x_loc == 0 and self.y_loc == 0) and self.wumpus_dead == False:
            if (0,1) in self.undiscovered:
                self.undiscovered.remove((0,1))
            self.safe_spaces.add((self.x_loc, self.y_loc))
            self.addToRecentMoves((self.x_loc, self.y_loc))
            self.MASTER_DICTIONARY[(self.x_loc, self.y_loc)] = 100
            self.getDirectionsToBestSquare(stench=True)
            return self.Read_queue(self.move_queue.pop(0))


        elif len(self.move_queue) != 0:
            return self.Read_queue(self.move_queue.pop(0))

        elif bump:
            self.updateUpperBoundaries()
            self.getDirectionsToBestSquare() #write bump fix
            return self.Read_queue(self.move_queue.pop(0))

        elif breeze:
            self.safe_spaces.add((self.x_loc, self.y_loc))
            self.addToRecentMoves((self.x_loc, self.y_loc))
            self.MASTER_DICTIONARY[(self.x_loc, self.y_loc)] = 100
            self.getDirectionsToBestSquare(breeze = True)
            return self.Read_queue(self.move_queue.pop(0))

        elif stench and self.wumpus_dead == False:
            self.safe_spaces.add((self.x_loc, self.y_loc))
            self.addToRecentMoves((self.x_loc, self.y_loc))
            self.MASTER_DICTIONARY[(self.x_loc, self.y_loc)] = 100
            self.getDirectionsToBestSquare(stench = True)
            return self.Read_queue(self.move_queue.pop(0))

        elif self._return == True:
            self.getDirectionsSpecific((0,0))
            return self.Read_queue(self.move_queue.pop(0))

        #fix this, how to go specifically to the last spot
        #need something like this because sometimes it doesnt go towards last
        #creates an infiite loop
        #logic kind of similar to going home, but need to remember to update undiscovered if find new things
        elif len(self.undiscovered) == 1 and self.undiscovered_count == 5:
            self.addToRecentMoves((self.x_loc, self.y_loc))
            self.isInMaster((self.x_loc, self.y_loc))
            adjacent = self.getAdjacentSquares(self.x_loc, self.y_loc)
            self.updateUndiscovered(adjacent)
            for e in self.undiscovered:
                break
            self.getDirectionsSpecific(e)
            return self.Read_queue(self.move_queue.pop(0))

        else:
            self.addToRecentMoves((self.x_loc, self.y_loc))
            adjacent = self.getAdjacentSquares(self.x_loc, self.y_loc)
            self.undiscovered_count += 1
            self.updateUndiscovered(adjacent)
            self.safe_spaces.add((self.x_loc, self.y_loc))
            self.isInMaster((self.x_loc,self.y_loc))
            self.getDirectionsToBestSquare()
            return self.Read_queue(self.move_queue.pop(0))

        return Agent.Action.CLIMB
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================


    def isInMaster(self,curLoc:tuple):
        if(curLoc not in self.MASTER_DICTIONARY):
            self.MASTER_DICTIONARY[curLoc] = 100

    #this will pretty much set the boundaries throughout the game once the agent encounters a bump
    def updateUpperBoundaries(self):
        if (self.facing == -1 or self.facing == 3):
            self.y_loc -= 1 #since it assumes that we still move forward but we actually dont so we need to fix it
            self.Y_LIMIT = self.y_loc + 1 #we update our class variables so we now know where the boundaries are
        elif (self.facing == 0):
            self.x_loc -= 1 #same here as well if it does occur
            self.X_LIMIT = self.x_loc + 1 #if a bump occurs and the facing direction is right then we have found our x-limit

    def getDirectionsToBestSquare(self, breeze = False, stench = False):
        neighbors = self.getAdjacentSquares(self.x_loc,self.y_loc)
        scores = self.calculateSquareScores(neighbors, breeze, stench)
        bestMove = self.getBestMove(scores) #gives us the best move's coordinates
        turns = self.calculateNumOfTurns(bestMove) #will help us in adding # of turns to queue
        rightWay = self.getCorrectDirection(bestMove) #gets us the RIGHT DIRECTION BOI
        self.addToQueue(rightWay,turns)

    def getDirectionsSpecific(self, target):
        neighbors = self.getAdjacentSquares(self.x_loc, self.y_loc)
        neighbors = self.stopExploring(target, neighbors)
        scores = self.calculateSquareScores(neighbors)
        scores = self.closerSpot(scores, target)
        bestMove = self.getBestMove(scores)
        turns = self.calculateNumOfTurns(bestMove)  # will help us in adding # of turns to queue
        rightWay = self.getCorrectDirection(bestMove)  # gets us the RIGHT DIRECTION BOI
        self.addToQueue(rightWay, turns)

    def closerSpot(self, scores, target):
        selfdist = self.calculateDistance((self.x_loc, self.y_loc), target)
        for pts in scores.keys():
            ptsdist = self.calculateDistance(pts, target)
            if ptsdist < selfdist:
                scores[pts] -= 70
        return scores

    def stopExploring(self, target, neighbors):
        delet = []
        selfdist = self.calculateDistance((self.x_loc, self.y_loc), target)
        for i in neighbors:
            if i == target:
                continue
            neighdist = self.calculateDistance(i, target)
            if i not in self.MASTER_DICTIONARY.keys() and (neighdist > selfdist):
                    delet.append(i)

        for i in delet:
            neighbors.remove(i)
        return neighbors

    def calculateDistance(self, spot, target):
        return sqrt((spot[0] - target[0]) ** 2 + (spot[1] - target[1]) ** 2)

    #perhaps another way to do this function is to immediately add all the adjacent coordinates into a list
    #and then perform a for loop on that list and filter it out by checking:
    #   if the x_loc or y_loc is less than 0, pop it from the list or if the x_loc or y_loc is over their own respective LIMIT variable
    def getAdjacentSquares(self, x_loc: int, y_loc: int): #spits out coords for spaces around current local
        adjacent_squares = list()
        if (y_loc - 1 >= 0 ):
            adjacent_squares.append((x_loc, y_loc - 1))
        if (x_loc - 1 >= 0):
            adjacent_squares.append((x_loc - 1, y_loc))
        if (y_loc + 1 < self.Y_LIMIT):
            adjacent_squares.append((x_loc, y_loc + 1))
        if (x_loc + 1 < self.X_LIMIT):
            adjacent_squares.append((x_loc + 1, y_loc))
        return adjacent_squares #should return a list of valid tuples that the agent can actually reach


    #takes in a dictionary and sorts it by its keys by lowest score
    def getBestMove(self, move_dict:dict):
        return sorted(move_dict.items(),key=lambda x : x[1])[0][0]
        #or it could be written like
        # sorted_kvs = sorted(move_dict.items(),key=lambda x : x[1])
        #return sorted_kvs[0][0] since we want the 0th element of the 0th index in the list

    #so this function will calculate the scores each square in the valid_moves list created by getAdjacentSquares
    # it will calculate based on several categories and rank moves by lowest score to ensure the "best" possible
    #move

    def addToRecentMoves(self, coord):

        if len(self.recent_moves) == 5:  # five coordinates in it
            self.recent_moves.pop(0)  # remove the oldest visited tile
        if (self.x_loc, self.y_loc) not in self.recent_moves:
            self.recent_moves.append((self.x_loc, self.y_loc))



    def calculateSquareScores(self, valid_moves: list, breeze = False, stench = False):
        local_moves = dict()
        for move in valid_moves:
            local_score = 0
            if (move in self.MASTER_DICTIONARY.keys()): #pull the space scores from MASTER
                local_score += self.MASTER_DICTIONARY[move]

            if((move not in self.safe_spaces) and (move not in self.undiscovered)
                    and (breeze == True or stench == True)): #safe spaces to avoid marking the spot dangerous
                if (move not in self.MASTER_DICTIONARY.keys()):
                    if stench == True:
                        local_score += 2000
                        self.MASTER_DICTIONARY[(move[0], move[1])] = 2000
                    elif breeze == True:
                        local_score += 1000
                        self.MASTER_DICTIONARY[(move[0], move[1])] = 1000
                else:
                    if stench == True:
                        local_score += 2000
                        self.MASTER_DICTIONARY[(move[0], move[1])] += 2000
                        local_score += 1000
                        self.MASTER_DICTIONARY[(move[0], move[1])] += 1000

            else:
                if move in self.MASTER_DICTIONARY.keys() and self.MASTER_DICTIONARY[move] >= 1000:
                    del self.MASTER_DICTIONARY[move]
                    self.updateUndiscovered([move])
                    local_score = 0
                local_score += 1
                local_score += self.calculateNumOfTurns(move)
                if move in self.recent_moves:#currently not implemented yet
                    local_score += 50

            local_moves[move] = local_score

        return local_moves

    def updateUndiscovered(self, adjacent):
        for i in adjacent:
            if i not in self.MASTER_DICTIONARY:
                self.undiscovered.add(i)
                self.undiscovered_count = 0
            else:
                if i in self.undiscovered:
                    self.undiscovered.remove(i)

    def purgeUndiscovered(self):
        delet = []
        if (self.x_loc, self.y_loc) in self.undiscovered:
            self.undiscovered.remove((self.x_loc, self.y_loc))
        for i in self.undiscovered:
            if i[0] >= self.X_LIMIT:
                delet.append(i)
            if i[1] >= self.Y_LIMIT:
                delet.append(i)
        for i in delet:
            self.undiscovered.remove(i)

    def findWumpus(self):
        for i in self.MASTER_DICTIONARY.keys():
            if self.MASTER_DICTIONARY[i] >= 4000:
                self.wumpus_local = i

    def calculateNumOfTurns(self, target_location : tuple):
        turns = 0 #start at one since it takes a step to actually move towards the targeted square
        correctDirection = self.getCorrectDirection(target_location) #gives us the right direction from below function
        if(self.facing == 0):
            if(correctDirection == (0,1) or correctDirection == (0,-1)):
                turns += 1 #since it only takes one turn to face either of these directions
            elif(correctDirection == (-1,0)):
                turns += 2 #pretty much a 180 degree turn so taking 2 turns to face the square
            else:
                turns += 0 #meaning that the agent is already facing in the target squares location
        else: #going for the direction values
            if(self.facing == 1 or self.facing == -3):
                if(correctDirection == (-1,0) or correctDirection == (1,0)):
                    turns += 1
                elif(correctDirection == (0,1)):
                    turns += 2
                else:
                    turns += 0 #sake of logic
            elif(self.facing == 2 or self.facing == -2):
                if(correctDirection == (0,1) or correctDirection == (0,-1)):
                    turns += 1
                elif(correctDirection == (1,0)):
                    turns += 2
                else:
                    turns += 0
            elif(self.facing == 3 or self.facing == -1):
                if(correctDirection == (-1,0) or correctDirection == (1,0)):
                    turns += 1
                elif(correctDirection == (0,-1)):
                    turns += 2
                else:
                    turns += 0 # again for sake of logic
        return turns

    def getCorrectDirection(self, target_location : tuple):
        DIRECTION_LIST = [(0,1),(1,0),(-1,0),(0,-1)] #respective up,right,left,and down directions        
        #we need a list of the possible directions up,left,right,down
        #we already have the current  x_loc and y_loc of agent and we're passing in the target tile
        for direction in DIRECTION_LIST:
            temp_x = self.x_loc + direction[0]
            temp_y = self.y_loc + direction[1]
            if((temp_x,temp_y) == target_location): #comparing tuples making sure it is right
                return direction #one of the correct directions

    def addToQueue(self, rightWay, turns):
        for num in range(turns): #will determine how many turns we actually need to face best square
            #Turning(1) is right turn
            #Turning(-1) is left turn
            if(self.facing == -2 or self.facing == 2):
                if(rightWay == (1,0)):
                    self.move_queue.append("self.Turning(1)")
                elif(rightWay == (0,1)):
                    #add right turn
                    self.move_queue.append("self.Turning(1)")
                elif(rightWay == (0,-1)):
                    #add left turn
                    self.move_queue.append("self.Turning(-1)")
            elif(self.facing == -1 or self.facing == 3):
                if(rightWay == (0,-1)):
                    self.move_queue.append("self.Turning(1)")
                elif(rightWay == (-1,0)):
                    #add left turn
                    self.move_queue.append("self.Turning(-1)")
                elif(rightWay == (1,0)):
                    #add right turn
                    self.move_queue.append("self.Turning(1)")
            elif(self.facing == -3 or self.facing == 1):
                if(rightWay == (0,1)):
                    #add either turn as long as its the same lmao
                    self.move_queue.append("self.Turning(1)")
                elif(rightWay == (1,0)):
                    #add left turn
                    self.move_queue.append("self.Turning(-1)")
                elif(rightWay == (-1,0)):
                    #add right turn
                    self.move_queue.append("self.Turning(1)")
            else: #meaning that the facing direction MUST BE ZERO (0!)
                if(rightWay == (-1,0)):
                    #doesnt matter which turn to add
                    self.move_queue.append("self.Turning(1)")
                elif(rightWay == (0,1)):
                    #add left turn
                    self.move_queue.append("self.Turning(-1)")
                elif(rightWay == (0,-1)):
                    #add right turn
                    self.move_queue.append("self.Turning(1)")
        self.move_queue.append("self.Move_forward()")#itll automatically go to the square since there are no turns required it will just go to that square


    def Turning(self, degree: int):
        self.facing = (self.facing + degree) % 4
        if degree == 1:
            return Agent.Action.TURN_RIGHT
        else:
            return Agent.Action.TURN_LEFT


    def Move_forward(self):
        if self.facing == 0: #moving to the right
            self.x_loc += 1
        elif (self.facing == -1 or self.facing == 3): #moving up up
            self.y_loc += 1
        elif (self.facing == -2 or self.facing == 2): #moving to the left
            self.x_loc -= 1
        elif (self.facing == -3 or self.facing == 1): #moving down
            self.y_loc -= 1
        return Agent.Action.FORWARD

    def Read_queue(self, command: str):
        if command == "self.Turning(1)":
            return self.Turning(1)
        if command == "self.Turning(-1)":
            return self.Turning(-1)
        elif command =="self.Move_forward()":
            return self.Move_forward()
    
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
