import numpy as np
import math

class game_map:
    def __init__(self, map_file, guard_file):
        #the try and except code below uses the info given from map_file and stores it into a list.
        #if it changed in any way, or does not exist, the except case will run.
        try:
            self.map_file = map_file
            fileHandler = open(map_file)
        except:
            print("Error. There is no map file.")
            exit
        try:
            maplist = []
            for line in fileHandler:
                maplist.append(line.rstrip('\n'))
            arr = []
            for items in maplist:
                col = []
                for characters in items:
                    col.append(characters)
                arr.append(col)
                self.maparray = arr #adds the map array to self to access later
        except:
            print("Error. The map file was edited while reading.")
            exit
        #now that the map_file is converted into a permanent list, we no longer need try or excepts
        for i in maplist: #this prints the newly made maplist for each item inside, then adds a return for output
            print(i + "\r")
        #the try and except code below uses the info given from guard_file and stores it into a list.
        #if it changed in any way, or does not exist, the except case will run.
        try:
            guardinfolist = []
            self.guard_file = guard_file
            fileHandler = open(guard_file)
        except:
            print("There is no guard file.")
            exit
        try:
            for line in fileHandler:
                guardinfolist.append(line.rstrip())
                self.guardinfolist = guardinfolist #adds the guardinfolist to self so the code can access it later
        except:
            print("Error. The guard file was edited while reading.")
            exit
        #using the code above, map_file and guard_file are now two permament lists, which can be accessed without worry of editing or deletion

        #the code below scans the 2D array to find where the player is starting and stores it in a tuple
        row_counter = 0
        for items in maplist:
            col_counter = 0
            for characters in items:
                if characters == "P":
                    player_position = (row_counter, col_counter)
                    break
                else:
                    col_counter = col_counter + 1
            row_counter = row_counter + 1
        self.player_position = player_position #adds player position to self for accessing later

        #the code below scans the 2D array to find where the exit is located and stores it in a tuple
        row_counter = 0
        for items in maplist:
            col_counter = 0
            for characters in items:
                if characters == "E":
                    exit_position = (row_counter, col_counter)
                    break
                else:
                    col_counter = col_counter + 1
            row_counter = row_counter + 1
        self.exit_position = exit_position #adds it to self to access later

        #the code below is sorting the instruction list into something more readable
        instructionslist = [] #this is going to be a 2D array grouping each list of instructions for each guard
        for items in guardinfolist:
            string = "" #this is an empty string that will be added to
            guardinstructions = []
            counter = 1
            for characters in items: #this checks to see if the current character is a space
                if ord(characters) > 32:
                    string = string + str(characters) #if it is not a space, the current character is added to the string
                if ord(characters) == 32: #this runs if the character is a space
                    guardinstructions.append(string) #the string in its current form gets appended to a list
                    string = "" #the string is then reset to an empty string
                if counter == len(items) and ord(characters) != 32: #this checks if the character is the last character in the list
                    guardinstructions.append(string) #if it is it adds it to the list
                    string = "" #then it resets the string to empty
                counter = counter + 1 #this is a counter for the code to see where it is at in the list for the previous if statement
            instructionslist.append(guardinstructions) #adding each list of instruction to the list
        guardobjectlist = [] #this will become the list of guard objects made
        for items in instructionslist: #this sees how many different lists of instructions there are in the list
            row = int(items[0]) #this assigns the row number to be the first number in the instructions
            col = int(items[1]) #this assigns the col number to be the second number in the instructions
            attack_range = int(items[2]) #this assigns the attack range to be the third in the instructions.
            # note that in the making of the guard instructions list, double digit integers were grouped into one string to allow for this step to work.
            movements_list = [] #this makes a new list for the movements commands, which are not integers
            for i in range(3, len(items)): #this goes through the list after the first 2 items, which were not movements
                movements_list.append(items[i]) #this appends them to the movements list
            newguard = guard(row, col, attack_range, movements_list) #this now creates a guard object using all the previous variables
            guardobjectlist.append(newguard) #this appaends the guards that get made into a list
        self.guardobjectlist = guardobjectlist #adds it to self to access later
        return

    def get_grid(self):
        currentmap = self.maparray #this gets the grid which was made from the map_file in the init.
        exitposition = self.exit_position
        for guards in self.guardobjectlist: #this goes through each guard in the guard object list
            locationtuple = guards.get_location() #this gets the current location of the guard using the guard.get_location function
            currentmap[locationtuple[0]][locationtuple[1]] = "G" #the location given is now replaced with a G in the current map
            currentmap[exitposition[0]][exitposition[1]] = "E" #re adding the exit. this is incase a guard steps on one. the guard will disapear then reappear next turn as long as they move
        self.maparray = currentmap #this now changes self.maparray to be what was made in this code
        return currentmap

    def get_gaurds(self): #this just repeats the guard object list which was made in init
        return self.guardobjectlist

    def update_player(self, direction): #this will take player inputs and move them on the map
        pcurrent = self.player_position #calls back player position which had an initial value from init
        currentmap = self.maparray #calls back the maparray which will now change again
        if direction == "U" and pcurrent[0]-1 >= 0 and currentmap[pcurrent[0]-1][pcurrent[1]] != "#" and currentmap[pcurrent[0]-1][pcurrent[1]] != "G": #if player inputs up, and there is no wall above them.
            #pcurrent[0]-1>=0 checks if the value is out of bounds. otherwise the code would break
            currentmap[pcurrent[0] - 1][pcurrent[1]] = "P" #the value a row above them will now become the player
            currentmap[pcurrent[0]][pcurrent[1]] = " " #the value which was their original position will now become a space
            self.maparray = currentmap #the self mapparay will now become what has been changed
            self.player_position = (pcurrent[0]-1, pcurrent[1]) #the player position will now become what it has changed to
        else:
            pass #if the direction input was up, but up was a wall, it passes the players turn and does not move them
        if direction == "D" and pcurrent[0]+1 < 12 and currentmap[pcurrent[0]+1][pcurrent[1]] != "#" and currentmap[pcurrent[0]+1][pcurrent[1]] != "G": #same as up but for down
            currentmap[pcurrent[0]+1][pcurrent[1]] = "P"
            currentmap[pcurrent[0]][pcurrent[1]] = " "
            self.maparray = currentmap
            self.player_position = (pcurrent[0] + 1, pcurrent[1])
        else:
            pass
        if direction == "L" and pcurrent[1] - 1 >= 0 and currentmap[pcurrent[0]][pcurrent[1]-1] != "#" and currentmap[pcurrent[0]][pcurrent[1]-1] != "G": #same as up or down, but this time accessing the columns instead of rows
            currentmap[pcurrent[0]][pcurrent[1]-1] = "P"
            currentmap[pcurrent[0]][pcurrent[1]] = " "
            self.maparray = currentmap
            self.player_position = (pcurrent[0], pcurrent[1]-1)
        else:
            pass
        if direction == "R" and pcurrent[1] + 1 < 16 and currentmap[pcurrent[0]][pcurrent[1]+1] != "#" and currentmap[pcurrent[0]][pcurrent[1]+1] != "G": #same as left but for right
            currentmap[pcurrent[0]][pcurrent[1]+1] = "P"
            currentmap[pcurrent[0]][pcurrent[1]] = " "
            self.maparray = currentmap
            self.player_position = (pcurrent[0], pcurrent[1]+1)
        else:
            pass
        return

    def update_guards(self): #this calls to the guard move function and updates their positions
        maparray = self.maparray #accessing the current maparray
        for guards in self.guardobjectlist: #for each guard object in the list
            guards.move(maparray) #it calls for the guard to move, more explained in that function
        self.maparray = maparray #the self mapparray now updates with the new guard locations
        return

    def player_wins(self): #this will detect if the player has reached the exit
        player_wins = False #starts off as false
        playerposition = self.player_position #pulls current player position
        exit_position = self.exit_position #pulls exit position
        if playerposition[0] == exit_position[0] and playerposition[1] == exit_position[1]: #if the values in the tuples of player position and exit position are the same
            player_wins = True #then that means the player has reached the exit, making playerwins true
        return player_wins

    def player_loses(self): #this will detect if the player has been spotted by a guard
        player_loses = False #starts as flase
        playerposition = self.player_position #pulls current player position
        guardobjectlist = self.guardobjectlist #pulls the guard object list
        for guards in guardobjectlist: #this runs for each guard in the list
            if guards.enemy_in_range(int(playerposition[0]), int(playerposition[1])) == True:
                player_loses = True #the code uses the guard.enemy_in_range to see if the player is in range of the guard
        return player_loses


class guard: #guard class
    def __init__(self, row, col, attack_range, movements):
        self.row = row #these self commands will store the values in the perameters to each individual guard
        self.col = col
        self.attack_range = attack_range
        self.movements = movements
        self.turncount = 0 #this will be used for the move function later
        return

    def get_location(self): #this just returns the guards position. self.row and self.col will be changing from the move function
        tuple = (int(self.row), int(self.col))
        return tuple

    def move(self, current_grid): #the move function
        movements = self.movements #calls the movements list (remember this happens for each individual guard)
        if self.turncount >= (len(movements)): #if the counter goes beyond the amount of moves in the movelist
            self.turncount = 0 #it gets reset to the first move
        if movements[self.turncount] == "L" and (self.col-1 >= 0) and current_grid[self.row][(self.col)-1] != "#" and current_grid[self.row][(self.col)-1] != "P" and current_grid[self.row][(self.col)-1] != "E" and current_grid[self.row][(self.col)-1] != "G": #if the guards current move in the movelist is left, and position to the left of the guard is not a wall
            current_grid[self.row][self.col] = " " #the guards original position is now a space in the array
            current_grid[self.row][(self.col)-1] = "G" #the guards new position is now a G in the array
            self.col = self.col - 1 #this changes this specific guards position, which in this case, the col was affected
            self.turncount = self.turncount + 1 #this adds one to the turn count, so it can get the next move next time it is called
        elif movements[self.turncount] == "R" and (self.col+1 < 16) and current_grid[self.row][(self.col)+1] != "#" and current_grid[self.row][(self.col)+1] != "P" and current_grid[self.row][(self.col)+1] != "E" and current_grid[self.row][(self.col)+1] != "G": #same as left but for right
            current_grid[self.row][self.col] = " "
            current_grid[self.row][(self.col)+1] = "G"
            self.col = self.col + 1 #updates the guard position this time to the right one column
            self.turncount = self.turncount + 1
        elif movements[self.turncount] == "D" and (self.row + 1 < 12) and current_grid[(self.row)+1][(self.col)] != "#" and current_grid[(self.row)+1][(self.col)] != "P" and current_grid[(self.row)+1][(self.col)] != "E" and current_grid[(self.row)+1][(self.col)] != "G": #same as left or right, but this time its up or down, which means we now access rows instead of cols
            current_grid[(self.row) + 1][(self.col)] = "G"
            current_grid[self.row][self.col] = " "
            self.row = self.row + 1 #adds one to the row, which inversely moves it down
            self.turncount = self.turncount + 1
        elif movements[self.turncount] == "U" and (self.row - 1 >= 0) and current_grid[(self.row)-1][(self.col)] != "#" and current_grid[(self.row)-1][(self.col)] != "P" and current_grid[(self.row)-1][(self.col)] != "E" and current_grid[(self.row)-1][(self.col)] != "G": #same as down but for up
            current_grid[(self.row) - 1][(self.col)] = "G"
            current_grid[self.row][self.col] = " "
            self.row = self.row - 1
            self.turncount = self.turncount + 1
        else: #this runs if none of the other conditions have been met, more specifically, if the gaurd runs into a wall
            self.turncount = self.turncount + 1 #it will increase the turn, meaning it goes to the next move
            pass #but it will not move cuz it hit a wall
        return

    def enemy_in_range(self, enemy_row, enemy_col): #enemy in range function
        inrange = False #starts as false
        if self.attack_range == 0: #this covers 0 attack range case. if this is the case, the guard has to be on you to be in range
            if enemy_row == self.row and enemy_col == self.col:
                inrange = True
        if abs(enemy_row - self.row) <= self.attack_range and enemy_col == self.col: #this covers the obvious case, the direct line of sight one
            inrange = True
        if abs(enemy_col - self.col) <= self.attack_range and enemy_row == self.row: #this covers the same as the last, but for the other dimension
            inrange = True
        if abs(enemy_row - self.row) <= self.attack_range - 1 and (enemy_col == self.col + 1 or enemy_col == self.col - 1):
            inrange = True #this covers if the column is off by 1. if it is off by 1, the attack range is reduced by one in that dimension
        if abs(enemy_col - self.col) <= self.attack_range - 1 and (enemy_row == self.row + 1 or enemy_row == self.row - 1):
            inrange = True #this covers the same as the last but for the other dimension
        if abs(enemy_col - self.col) <= self.attack_range - 2 and abs(enemy_row - self.row) <= self.attack_range - 2:
            inrange = True #this covers diagnals. if it is off by 1 in both dimensions, the attack range is reduced by 2
        return inrange