#Import library of game functions
import pygame
import random
pygame.init()

# Define some colors
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)
LIME = (   0, 255,   0)
RED = ( 255,   0,   0)
CRIMSON = (220, 20, 60)
DARKRED = (139, 0, 0)
VIOLET = (199, 21, 133)
ORANGERED = (255, 69, 0)
ORANGE = (255, 165, 0)
TOMATO = (255, 69, 0)
SALMON = (255, 160, 122)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
PEACH = (255, 218, 185)
FUCHSIA = (255, 0, 255)
INDIGO = (75, 0, 130)
DARKSLATE = (72, 61, 139)
PURPLE = (128, 0, 128)
GREEN = (0, 128, 0)
DARKGREEN = (0, 100, 0)
TEAL = (0, 128, 128)
SEA = (32, 178, 170)
DARKSEA = (46, 139, 87)
SPRING = (0, 255, 127)
DARKBLUE = (0, 0, 139)
MUTEDBLUE = (65, 105, 225)
AQUA = (127, 255, 212)
GRAY = (80, 80, 80)
SILVER = (211, 211, 211)
BEIGE = (245, 245, 220)
LAVBACK = (255, 240, 245)
AZURE = (240, 248, 255)
MAROON = (128, 0, 0)
BROWN = (139, 69, 19)
SANDY = (244, 164, 96)
TAN = (210, 180, 140)
BACK = (250, 250, 240)

################################ GLOBAL VARS #######################################

#This value can be modified based on how much of the map you want to be pits.
pit_perc = 45

#These three lines load images.
robot = pygame.image.load('robot.bmp')
star = pygame.image.load('star.bmp')
goal = pygame.image.load('goal.bmp')

#An empty list where all of the boxes objects will eventually reside.
boxes = []

#An easy way to change the Clock of the game so that it moves slower or faster.
fps = 60

#A variable that we will later use to check whether a assigning a pit would block off empty squares.
two_exit = False

#Unused debugger tool so that print statements would only happen once.
#track = 0

#These variables change based on where the ball is. They are true if the ball is next to an outer boundary and will not allow the
#coordinates of the ball to head that direction.
north_wall = True
south_wall = False
east_wall = False
west_wall = True

#This list will later be used to store boxes that have already been checked for a pathway that 
#connects to empty boxes (checking if there are two exits).
box_list = []


#This variable will change the number of stars in the map.
orig_stars = 10


################################ GRID BOXES SETUP #######################################
################################ GRID BOXES SETUP #######################################
################################ GRID BOXES SETUP #######################################



#This class will define all of the boxes, allowing the program to randomize
#pits in a way that there is always a path to the goal

class Box:
    
    def __init__(self, name):
        self.name = name
        self.x_coord = None  #x coordinate
        self.y_coord = None  #y coordinate
        self.attr = "unassigned"  #tells whether it is a pit/star/path
        self.r_nei = None #right neighbour box
        self.l_nei = None #left neighbour box
        self.t_nei = None #etc.
        self.b_nei = None

    def nei(self, r_nei, l_nei, t_nei, b_nei): #List of neighbour boxes (the boxes that surround this box).
        self.r_nei = r_nei
        self.l_nei = l_nei
        self.t_nei = t_nei
        self.b_nei = b_nei
        
#This function looks around the box and assigns neighbouring boxes if that box exists.
def assign_nei():
    global boxes
	#This line creates all of the box objects from the Box class.
    boxes = [Box(i) for i in range(0, r)]
    for i in range (0, r):
        if i < row: #These lines are for the boxes that have no left neighbour (are on the far left side of the map)
            if i == 0:
                boxes[0].nei(boxes[row], None, None, boxes[1]) #upper left corner
            elif i == r/row-1:
                boxes[r/row-1].nei(boxes[(r/row-1)+row], None, boxes[(r/row-1)-1], None) #bottom left corner
            else:
                boxes[i].nei(boxes[i+row], None, boxes[i-1], boxes[i+1]) #boxes on the left side, but not in corners
        elif i >= r-row: #These lines are for the boxes that are on the right side, and have no right neighbour
            if i == r-row:
                boxes[r-row].nei(None, boxes[(r-row)-row], None, boxes[(r-row)+1]) #upper right corner
            elif i == r-1:
                boxes[r-1].nei(None, boxes[(r-1)-row], boxes[(r-1)-1], None) #bottom right corner
            else:
                boxes[i].nei(None, boxes[i-row], boxes[i-1], boxes[i+1]) #far right side, but not in the corners
        else: #These lines are for boxes that are in the centre, but not in any corners
            if i%row == 0:
                boxes[i].nei(boxes[i+row], boxes[i-row], None, boxes[i+1]) #these boxes have no top neighbour and are on the top row
            elif (i+1)%row == 0:
                boxes[i].nei(boxes[i+row], boxes[i-row], boxes[i-1], None) #these boxes have no bottom neighbour and are on the bottom row
            else:
                boxes[i].nei(boxes[i+row], boxes[i-row], boxes[i-1], boxes[i+1]) #these boxes are in the centre and have all four neighbours

#This function runs through and assigns a path from the start to the finish to ensure there is always a 
#way to get from start to finish
def assign_path():
    i = 0
	#These two lines assign attributes of path to the first and final box.
    boxes[0].attr = "path"
    boxes[r-1].attr = "path"
    while i != r-2 and i != (r-1)-row:
	#This while loop will continue until the current box number is one next to the final box.
        perc = random.randint(0, 99)
        if boxes[i].r_nei != None and perc < 50: #These take a 50 percent chance to assign path to the right or bottom box.
            boxes[i].r_nei.attr = "path"
            i = boxes[i].r_nei.name #This line then makes i, or the current box the box to the right
        elif boxes[i].b_nei != None:
            boxes[i].b_nei.attr = "path"
            i = boxes[i].b_nei.name #This line then makes i, or the current box the box to the bottom
        else:	#This else will activate if percentage is more than 50 percent (meaning path should go down), but there doesn't exist
					#a box to the bottom. Because the map is always square, there will always be a box to the bottom or the right.
            boxes[i].r_nei.attr = "path"
            i = boxes[i].r_nei.name
	#These lines assign path to the boxes surrounding the final goal so the user can always navigate around the goal, allowing them
		#to achieve all of the stars without ending the game.
    boxes[r-2].attr = "path"
    boxes[r-1-row].attr = "path"
    boxes[r-2-row].attr = "path"

#This is the primary function that will call two helper functions which allow for a randomly generated map of "empty" and "pit" squares.
def assign_pits():
    for i in range(1, r):	#This runs through every box except for the first, r is the total number of boxes.
        if boxes[i].attr == "unassigned": #This makes sure that it will only assign an attribute if there is not already an attribute
											#assigned. If this were not here it would write over "path" box attributes.
            neigh = check_no_empty(boxes[i]) #This checks if the neighbour boxes are empty, and if they are empty, it checks if there
												#is a way to a path (i.e. a way out).
            #print("box "+str(i)) # just debugging prints
            #print(neigh)
            if neigh == "one exit":
                boxes[i].attr = "empty" #if there is only one exit, the current box must be empty (i.e. a exit).
            elif neigh == "two exit or no empty": #if there are multiple exits or no empty boxes around this box, there is a chance for
													#it to be either a pit or an empty box
                perc = random.randint(0, 99)
                if perc < pit_perc:
                    boxes[i].attr = "hole"	#a percentage chance to be a hole or empty
                else:
                    boxes[i].attr = "empty"
            else:
                print("error")


#This function is called by "assign_pits" and checks if there is an empty box around the cur_box.
def check_no_empty(cur_box): #cur_box is the current box
    global box_list
    global two_exit
    two_exit = False
    box_list = [cur_box.name] #this enters the cur_box into the box_list that the recursive function below won't check for an exit
    if cur_box.r_nei != None: #these two lines are in every conditional statement, because you can't call .attr if there is no object
        if cur_box.r_nei.attr == "empty":
            next_to_path(cur_box.r_nei) #this calls the next helper function which recursivly checks if there is a connection
											#from this empty box to a "path" or an "unassigned" box which would always have the potential
											#to lead to a path (which is a definite connection) in the future.
            box_list = [cur_box.name] #this resets the box list to only have the original box
            if two_exit == False: #if there isn't another exit, it returns "one_exit" and the cur_box must be an empty square
                return "one exit"
            two_exit = False
    if cur_box.l_nei != None: #these following conditional statements do the same thing as the above example, just with the left,
								#top, and bottom boxes
        if cur_box.l_nei.attr == "empty":
            next_to_path(cur_box.l_nei)
            box_list = [cur_box.name]
            if two_exit == False:
                return "one exit"
            two_exit = False
    if cur_box.t_nei != None:
        if cur_box.t_nei.attr == "empty":
            next_to_path(cur_box.t_nei)
            box_list = [cur_box.name]
            if two_exit == False:
                return "one exit"
            two_exit = False
    if cur_box.b_nei != None:
        if cur_box.b_nei.attr == "empty":
            next_to_path(cur_box.b_nei)
            box_list = [cur_box.name]
            if two_exit == False:
                return "one exit"
            two_exit = False
    return "two exit or no empty" #if there are no empty boxes around the cur_box, there is no empty box to block off, so it returns
									#two no empty
				


#This function is a helper function that is called by the above function. It recursively checks for a connected path or unassigned
	#box which would mean there are two exits (through the current box) and through the path connection.
def next_to_path(cur_box):
    global box_list
    global two_exit
    box_list.append(cur_box.name)
    if cur_box.attr == "path" or cur_box.attr == "unassigned": #This is the return condition for two_exit to be true. If any of the
									#recursions reach a path or unassigned box, there is another way for the empty square(s) to exit.
        two_exit = True 	#if no path or unassigned squares are found, two_exit will remain false and "check_no_empty" will return
								#"one_exit". if there are two exits, "check_no_empty" will not return anything, because the cur_box only
								#needs to be empty if there is only one exit, that is the only final activation condition.
        return
    if cur_box.r_nei != None:
			#This following line checks if the box to the right is empty, path, or unassigned
        if cur_box.r_nei.attr == "empty" or cur_box.r_nei.attr == "path" or cur_box.r_nei.attr == "unassigned":
            if cur_box.r_nei.name not in box_list:
				#if it has one of those attributes, it checks to see if that box has already been checked by my recursion
                next_to_path(cur_box.r_nei) #if it hasn't been checked, it runs through the neighbour recursively
    if cur_box.l_nei != None:				#this recursion will go until there are no unchecked boxes or it finds a path/unassigned
        if cur_box.l_nei.attr == "empty" or cur_box.l_nei.attr == "path" or cur_box.l_nei.attr == "unassigned":
            if cur_box.l_nei.name not in box_list:
                next_to_path(cur_box.l_nei)
    if cur_box.t_nei != None:
        if cur_box.t_nei.attr == "empty" or cur_box.t_nei.attr == "path" or cur_box.t_nei.attr == "unassigned":
            if cur_box.t_nei.name not in box_list:
                next_to_path(cur_box.t_nei)
    if cur_box.b_nei != None:
        if cur_box.b_nei.attr == "empty" or cur_box.b_nei.attr == "path" or cur_box.b_nei.attr == "unassigned":
            if cur_box.b_nei.name not in box_list:
                next_to_path(cur_box.b_nei)
#this function above can check for path or unassigned, because it runs through the boxes from top to bottom, then left to right. 
	#if it reaches a box that is unassigned, there will always be potential for the connected empty box to reach the final goal
	#because there are more unassigned boxes to the bottom and right (where the goal is).
"""
An 8x8 example:
0 8  16 24 32 40 48 56
1 9  17 25 33 41 49 57
2 10 18 26 34 42 50 58
3 11 19 27 35 43 51 59
4 12 20 28 36 44 52 60
5 13 21 29 37 45 53 61
6 14 22 30 38 46 54 62
7 15 23 31 39 47 55 63
These functions check boxes 0-7, then 8-15, and so on. Imagine a scenario like this:
key: un = unassigned, pa = path, ho = pit/hole, em = empty
pa ho un un un un un un
pa pa pa pa pa pa un un
ho ho un un un pa pa un
em em un un un un pa un
em un un un un un pa un
ho un un un un un pa un
ho un un un un un pa un
em un un un un un pa pa
In this scenario, the function would be in the process of assigning attributes to the boxes. The cur_box would be
box 12. Box 12 would then look at its neighbours. The box to its left is empty, initiating recursion. That box is box 4,
which now checks its surrounding boxes. The box above box 4 is empty, so it then recursively checks box 3. Which then recursively
checks box 11. Box 11 then checks box 19, which is unassigned. It is clear from the picture above, that an unassigned box always 
has the potential to reach a path, and therefore be connected to every other empty box. This function always recursively checks 
until it either has reached a path or unassigned, or ends (meaning that the original box checked must be empty to allow for a way out).
"""


#This function just assigns coordinates to each box so they can later be draw in pygame.
def assign_coords():
    for i in range(r):
        boxes[i].x_coords = (i/row)*51	#the coordinates correlate with the size of each row, and can be assigned in this way
        boxes[i].y_coords = (i%row)*51	#same here because it is a square.
        #print(boxes[i].x_coords) #just debugging print statements.
        #print(boxes[i].y_coords)

		
#This function assigns boxes with empty or path attributes, instead to have a star attribute, which will later draw a star in for
	#the player to get
def assign_stars():
    global stars_num
    squares = 0	#squares is the total number of empty/path boxes
    for i in range(1, r-2):
        #print str(i)+ "attr: " + boxes[i].attr
        if boxes[i].attr == "path" or boxes[i].attr == "empty":
            squares += 1	#iterates through boxes, adding up the empty and path ones
    squares -= 2	#subtracts two for the start and finish, which cannot contain stars
    tracker = 0         #to try and achieve random star placement, it will run through the boxes until there are 
    while stars_num != 0 and tracker != 20:  	#no more stars to assign, or it has run through the boxes 20 times
        tracker += 1							
        for i in range(1, r-2):
            if (boxes[i].attr == "path" or boxes[i].attr == "empty") and stars_num != 0: #This runs if the current box is path/empty
                rand2 = random.randint(1,squares) #this creates a random number between 1 and the number of squares
                if squares < stars_num:
                    stars_num = squares - (stars_num/2)
                #print(stars_num)
                #print(squares)
                #print(rand2 <= squares/stars_num)
                #print(squares/stars_num)
                #print(squares)
                if rand2 <= squares/stars_num:	#if the random number fulfills the ratio (i.e. creates probability)
                    star_nei = 0 #star nei is the variable which ensures there are no neighbouring stars, for nice star spacing
                    if boxes[i].r_nei != None: #these conditional statements make sure there are no neighbouring stars to the right, left, etc.
                        #print(boxes[i].r_nei.name)
                        if boxes[i].r_nei.attr == "star":
                            star_nei += 1
                    if boxes[i].l_nei != None:
                        #print(boxes[i].l_nei.name)
                        if boxes[i].l_nei.attr == "star":
                            star_nei += 1
                    if boxes[i].t_nei != None:
                        #print(boxes[i].t_nei.name)
                        if boxes[i].t_nei.attr == "star":
                            star_nei += 1
                    if boxes[i].b_nei != None:
                        #print(boxes[i].b_nei.name)
                        if boxes[i].b_nei.attr == "star":
                            star_nei += 1
                    if star_nei == 0:	#at the end, if there are no star_nei, the current box becomes a star
                        boxes[i].attr = "star"
                        stars_num -= 1
                    
        
        
################################ DEBUGGING #######################################
"""
0 8  16 24 32 40 48 56
1 9  17 25 33 41 49 57
2 10 18 26 34 42 50 58
3 11 19 27 35 43 51 59
4 12 20 28 36 44 52 60
5 13 21 29 37 45 53 61
6 14 22 30 38 46 54 62
7 15 23 31 39 47 55 63
"""
#This below debugging prints out the box attributes in the rows they should appear
"""
for k in range (0, row):
    for i in range(0, r-(row-1), row):
        if i+k < r-row:
            print(boxes[i+k].attr[:2]),
        else:
            print(boxes[i+k].attr[:2])
"""

################################ PYGAME EVENTS #######################################
################################ PYGAME EVENTS #######################################
################################ PYGAME EVENTS #######################################

#defines the size of the pygame screen
size = (800, 600)
screen = pygame.display.set_mode(size)
screen.fill(WHITE)	#sets the color to white

# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

event = True
pygame.display.set_caption("Wumpus")	#this line sets the window name to be ""Wumpus"
#These following three variables define which screen pygame should print, they control the GUI
final_screen = False
start_screen = True
game_screen = False

#This is the large loop for the game engine. While it is running, game commands are being executed, whether events or drawings.
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("User asked to quit.")
            done = True
            
################################ START SCREEN EVENTS #####################################

        if start_screen == True:
			#resets the position of the robot
            x_coord = 2	#these two variables determine the position of the robot
            y_coord = 2
            stars_num = orig_stars	#resets the number of stars
            collected_stars = 0	#resets the number of stars collected
            if event.type == pygame.KEYDOWN:	#All conditionals under this are key presses
                pressed = False	#only one key can be pressed at a time in this game
                if event.key == pygame.K_1 and pressed == False:	#if the user presses 1, the dif variable is set to 1
                    dif = 1
					#the screens change when these numbers are pressed
                    start_screen = False
                    game_screen = True
                    pressed = True
                if event.key == pygame.K_2 and pressed == False:	#same things happen in the following event conditionals
                    dif = 2
                    start_screen = False
                    game_screen = True
                    pressed = True
                if event.key == pygame.K_3 and pressed == False:
                    dif = 3
                    start_screen = False
                    game_screen = True
                    pressed = True
                if event.key == pygame.K_4 and pressed == False:
                    dif = 4
                    start_screen = False
                    game_screen = True
                    pressed = True
				
				#depending on which difficulty was selected, the total number of boxes and number of rows
					#because of this implementation, in the future it would be easy to implement user input for row size
                if dif == 1 or dif == 2:
                    row = 8		#which row size the user wants
                    r = row*row
                    if dif == 1:
                        timeleft = 30
                    else:
                        timeleft = 15
                else:
                    row = 11
                    r = row*row
                    if dif == 3:
                        timeleft = 15
                    else:
                        timeleft = 10
				
				#function calls happen here, so everytime the user returns to the start screen, a new map will be generated
                assign_nei()
                assign_path()
                assign_pits()
                assign_coords()
                assign_stars()
                secs = 0
                clock_check = 0

################################ FINAL SCREEN EVENTS #####################################
            
        if final_screen == True:
			# --- Again, reset the coordinates, and star numbers
            x_coord = 2
            y_coord = 2
            stars_num = orig_stars
            pressed = False	# --- Again the user can only press one key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:		# --- If y is pressed
                    #print("User pressed y.") #debugging
                    if final_screen == True:
                        # --- Changes state to start of game, because the user wants to play again!
                        final_screen = False
                        start_screen = True
                if event.key == pygame.K_n:
                    #print("User pressed n.") #debugging
                    # --- User wants to end program, :(
                    if final_screen == True:
                        pygame.quit()
                        done = True
                        break
                if event.key == pygame.K_1 and pressed == False: #these following key presses are just shortcuts to begin the game
																#and skip the start screen
                    dif = 1
                    start_screen = False
                    game_screen = True
                    final_screen = False
                    pressed = True
                    collected_stars = 0
                if event.key == pygame.K_2 and pressed == False:
                    dif = 2
                    start_screen = False
                    game_screen = True
                    final_screen = False
                    pressed = True
                    collected_stars = 0
                if event.key == pygame.K_3 and pressed == False:
                    dif = 3
                    start_screen = False
                    game_screen = True
                    final_screen = False
                    pressed = True
                    collected_stars = 0
                if event.key == pygame.K_4 and pressed == False:
                    dif = 4
                    start_screen = False
                    game_screen = True
                    final_screen = False
                    pressed = True
                    collected_stars = 0
                
				#These following lines are just the same as the start screen, to allow for the user shortcut specified above
                if dif == 1 or dif == 2:
                    row = 8
                    r = row*row
                    if dif == 1:
                        timeleft = 30
                    else:
                        timeleft = 15
                else:
                    row = 11
                    r = row*row
                    if dif == 3:
                        timeleft = 15
                    else:
                        timeleft = 10

                assign_nei()
                assign_path()
                assign_pits()
                assign_coords()
                assign_stars()
                secs = 0
                clock_check = 0

################################ GAME SCREEN EVENTS ######################################

        if game_screen == True:
            if event.type == pygame.KEYDOWN:
				#These event keys just move the player robot a certain number of pixels
                if event.key == pygame.K_LEFT:
                    if not east_wall:	#This line checks to make sure the robot would not be leaving the bounds of the maps
                        x_coord += -51
                elif event.key == pygame.K_RIGHT:	#etc, the same as above
                    if not west_wall:
                        x_coord += 51
                elif event.key == pygame.K_UP:
                    if not north_wall:
                        y_coord += -51
                elif event.key == pygame.K_DOWN:
                    if not south_wall:
                        y_coord += 51
			
			#These lines set the walls to be true or false, based on where the robot's new position is
            if x_coord == 2:
                east_wall = True
            else:
                east_wall = False
                
            if x_coord >= ((51*row)-51):
                west_wall = True
            else:
                west_wall = False
                
            if y_coord == 2:
                north_wall = True
            else:
                north_wall = False
                
            if y_coord >= ((51*row)-51):
                south_wall = True
            else:
                south_wall = False

			#These next lines will cause events to happen if the robot steps on a star or a pit box
            pits = []
            stars = []
            star_id = {}
			#This loop makes a list of x and y coordinates that are the exact coordinates the robot will step on
            for i in range(len(boxes)):
                if boxes[i].attr == "hole":	#if it is a hole attribute, set those coordinates to the pits list
                    pits += [[boxes[i].x_coords+2, boxes[i].y_coords+2]]
                if boxes[i].attr == "star":	#if it is a star, add it to the stars list
                    stars += [[boxes[i].x_coords+2, boxes[i].y_coords+2]]
                    star_id[str(boxes[i].x_coords)+str(boxes[i].y_coords)] = i	#this line adds it to a dictionary which stores the 
																					#id of the stars which will be used to remove the stars
                    
			#This loop checks each time the robot moves if the robot's coordinates are in a pit
            if [x_coord, y_coord] in pits:
				#if they are, the user loses and goes to the final screen
                win = False
                final_screen = True
                game_screen = False
			
			#This loop checks each time the robot moves if the robot's coordinates are on a star
            if [x_coord, y_coord] in stars:
				#if they are, collected stars increases and the id of the boxed star changes to empty, removing the star
                collected_stars += 1
                boxes[star_id[str(x_coord-2)+str(y_coord-2)]].attr = "empty"
			
			#This loop checks if the robot is on the goal, the final bottom left corner, if it is, the user wins!
            if x_coord == ((row-1)*51)+2 and y_coord == ((row-1)*51)+2:
                win = True
                final_screen = True
                game_screen = False
                


################################ PYGAME DRAWING ######################################
################################ PYGAME DRAWING ######################################
################################ PYGAME DRAWING ######################################
    

	#This line checks if the user exited, it is just here to avoid an error where the screen will try to execute
		#drawing commands after the screen has closed
    if done == True:
        break


    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)

################################ GAME SCREEN DRAWING ####################################

    if game_screen == True:        
		#This loop will draw black holes and stars on the screen
        for i in range(len(boxes)):
            if boxes[i].attr == "hole":
                pygame.draw.rect(screen,BLACK,[boxes[i].x_coords, boxes[i].y_coords, 51,51],0)
            if boxes[i].attr == "star":
                screen.blit(star,(boxes[i].x_coords, boxes[i].y_coords))
            
        #draws lines on the map to differentiate the boxes for the user
        for i in range(0, 51*(row+1), 51):
            pygame.draw.line(screen,BLACK,[0,0+i],[51*row,0+i],2)	#draws horizontal lines    
            pygame.draw.line(screen, BLACK,[0+i,0],[0+i,51*row],2)	#draws vertical lines
            
		#draws the robot on the screen at the position of the x and y coordinates associated with the player
        screen.blit(robot,(x_coord,y_coord))

        #draws the GOAL
        screen.blit(goal,(((row-1)*51)+2, ((row-1)*51)+2))



        #Seconds Timer
        Clock = pygame.time.get_ticks()
        if Clock/1000 != clock_check:
            secs += 1
            clock_check = Clock/1000

#########These next lines differentiate based on what the map size is for a different game screen.
###Most of these lines are just drawing lines using the syntax for pygame.
        if dif > 2:
			# --- Defines the font type, font size, italics, and bold
            font = pygame.font.SysFont('Calibri', 30, True, False)
			# --- Renders the actual font, gives the string to print and the color
            timer = font.render(str(timeleft-secs+1),True,CRIMSON)
			# --- Then actually puts it on the screen using a pygame blit command, at the coordinates specified
            screen.blit(timer, [670, 270])
            if secs > timeleft: #When there is no time left (which counts down), the game ends and state changes
                final_screen = True
                win = False
                game_screen = False
            #title, font uses the same format explained above
            font = pygame.font.SysFont('Euphemia', 45, True, True)
            text = font.render("WUMPUS", True, TEAL)
            screen.blit(text, [575, 50])
            #instructions
            font = pygame.font.SysFont('Times New Roman', 17, False, False)
            text = font.render("Instructions: Move using the", True, BLACK)
            screen.blit(text, [575, 400])
            font = pygame.font.SysFont('Times New Roman', 17, False, False)
            text = font.render("arrow keys. Collect as many", True, BLACK)
            screen.blit(text, [590, 420])
            font = pygame.font.SysFont('Times New Roman', 17, False, False)
            text = font.render("stars as you can and get", True, BLACK)
            screen.blit(text, [590, 440])
            font = pygame.font.SysFont('Times New Roman', 17, False, False)
            text = font.render("yourself to the goal within", True, BLACK)
            screen.blit(text, [590, 460])
            font = pygame.font.SysFont('Times New Roman', 17, False, False)
            text = font.render("the time limit. Remember,", True, BLACK)
            screen.blit(text, [590, 480])
            font = pygame.font.SysFont('Times New Roman', 17, False, False)
            text = font.render("don't fall in the pits!", True, BLACK)
            screen.blit(text, [590, 500])
            #stars collected, visual effect and calls them "Points"
            font = pygame.font.SysFont('Courier', 25, False, False)
            text = font.render("Points: " + str(collected_stars), True, VIOLET)
            screen.blit(text, [620, 200])
        else:	#If the difficulty is higher, then the map size is different, and the GUI has to shift around on the screen.
					#The main changes are the coordinate position on the canvas
            #timeleft = 30
            font = pygame.font.SysFont('Calibri', 30, True, False)
            timer = font.render(str(timeleft-secs+1),True,CRIMSON)
            screen.blit(timer, [580, 300])
			#same as above
            if secs > timeleft:
                final_screen = True
                win = False
                game_screen = False
            #title
            font = pygame.font.SysFont('Euphemia', 75, True, True)
            text = font.render("WUMPUS", True, TEAL)
            screen.blit(text, [425, 20])
            #"Instructions for game"
            font = pygame.font.SysFont('Times New Roman', 17, False, False)
            text = font.render("Instructions: Move using the arrow keys. Collect as many stars", True, BLACK)
            screen.blit(text, [170, 470])
            font = pygame.font.SysFont('Times New Roman', 17, False, False)
            text = font.render("as you can and get yourself to the goal within", True, BLACK)
            screen.blit(text, [260, 490])
            font = pygame.font.SysFont('Times New Roman', 17, False, False)
            text = font.render("the time limit. Remember, don't fall in the pits!", True, BLACK)
            screen.blit(text, [260, 510])
            #stars collected
            font = pygame.font.SysFont('Courier', 25, False, False)
            text = font.render("Points: " + str(collected_stars), True, VIOLET)
            screen.blit(text, [530, 210])
            


################################ START SCREEN DRAWING ####################################

    
    #font list: key word 'typeface windows' #just a tool to remember which kinds of fonts pygame supports
    if start_screen == True:
        win = False
        #Title
        font = pygame.font.SysFont('Euphemia', 100, True, True)
        #Render text
        text = font.render("WUMPUS", True, TEAL)
        # Put the image of the text on the screen
        screen.blit(text, [150, 50])

        #"Choose difficulty"
        font = pygame.font.SysFont('Calibri', 25, True, False)
        text = font.render("Choose Difficulty:", True, SANDY)
        screen.blit(text, [200, 250])
        #The difficulties
        font = pygame.font.SysFont('Calibri', 22, False, False)
        text = font.render("Easy- Press 1", True, INDIGO)
        screen.blit(text, [220, 280])
        font = pygame.font.SysFont('Calibri', 22, False, False)
        text = font.render("Medium- Press 2", True, INDIGO)
        screen.blit(text, [220, 310])
        font = pygame.font.SysFont('Calibri', 22, False, False)
        text = font.render("Hard- Press 3", True, INDIGO)
        screen.blit(text, [220, 340])
        font = pygame.font.SysFont('Calibri', 22, False, False)
        text = font.render("Very Hard- Press 4", True, INDIGO)
        screen.blit(text, [220, 370])

        #"Instructions for game"
        font = pygame.font.SysFont('Times New Roman', 17, False, False)
        text = font.render("Instructions: Move using the arrow keys. Collect as many stars", True, BLACK)
        screen.blit(text, [170, 500])
        font = pygame.font.SysFont('Times New Roman', 17, False, False)
        text = font.render("as you can and get yourself to the goal within", True, BLACK)
        screen.blit(text, [260, 520])
        font = pygame.font.SysFont('Times New Roman', 17, False, False)
        text = font.render("the time limit. Remember, don't fall in the pits!", True, BLACK)
        screen.blit(text, [260, 540])

        
################################ FINAL SCREEN DRAWING ####################################
        
    if final_screen == True:
        if win == True:
            #Define font
            font = pygame.font.SysFont('Georgia', 100, True, False)
            #Render text
            text = font.render("YOU WIN", True, CRIMSON)
            # Put the image of the text on the screen
            screen.blit(text, [150, 200])
            #stars collected, tells you how many points you got
            font = pygame.font.SysFont('Courier', 35, False, False)
            text = font.render("Points: " + str(collected_stars), True, DARKGREEN)
            screen.blit(text, [300, 500])
        else:
            # --- Define font
            font = pygame.font.SysFont('Georgia', 100, True, False)
            # --- Render font
            text = font.render("YOU LOSE",True,CRIMSON)
            # --- Put the image of the text on the screen
            screen.blit(text, [130, 200])
        font = pygame.font.SysFont('Calibri', 25, True, False)
        text = font.render("Play again? (y,n)",True,GRAY)
        screen.blit(text, [310, 400])
        # --- Border fancy blue diagonal streaks, this uses a nice loop to define lines along the sides of the screen
				#credit to the pygame website, which provided this code
        y_offset = 0
        for y_offset in range(-150, 600, 10):
            pygame.draw.line(screen,DARKBLUE,[0,0+y_offset],[100,100+y_offset],5)
        y_offset = 0
        for y_offset in range (-150, 600, 10):
            pygame.draw.line(screen,DARKBLUE,[800,0+y_offset],[700,100+y_offset],5)



    # --- Updates the screen with what we've drawn.
    pygame.display.flip()
    
    # --- Limit to 60 frames per second
    clock.tick(fps)


 
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
