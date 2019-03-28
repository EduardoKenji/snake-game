import pygame
import random

class MapSquare:
    def __init__(self, attrib_dict):
        # x and y are the true absolute position in the window
        # map_x and map_y are abstract coordinates to represent the player's snake or food inside the 2D map matrix
        # square_size represents the square's width and the square's height in pixels
        valid_attributes = ("x", "y", "map_x", "map_y", "square_size")
        for key in valid_attributes:
            self.__dict__[key] = attrib_dict[key]

     # Method used to draw player normal segments
    def draw_player(self, surface):
            # Parameters: Surface to draw; Color; (x, y, width, height); 0 = Empty, 1 = Filled
            pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.square_size, self.square_size), 1)

    # Method currently used to draw walls
    def draw(self, surface):
            pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.square_size, self.square_size), 0)

    # Method used to draw player head (in blue)
    def draw_player_head(self, surface):
            pygame.draw.rect(surface, (0, 0, 255), (self.x, self.y, self.square_size, self.square_size), 1)

    # Method to draw the snake food as a filled red square
    def draw_snake_food(self, surface):
            pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.square_size, self.square_size), 0)

# The player class tracks the snake head
class Player:
    def __init__(self, attrib_dict):
        # map_x and map_y are abstract coordinates to represent the player's snake or food inside the 2D map matrix
        # Directions: 0 = left; 1 = down; 2 = right; 3 = up 
        # size: Player's snake number of segments
        valid_attributes = ("map_x", "map_y", "direction", "size")
        for key in valid_attributes:
            self.__dict__[key] = attrib_dict[key]

# Map class contain a 2D map matrix of MapSquares 
class Map:
    # y_axis_orientation: -1 (up -> bottom) or 1 (bottom -> up)
    def __init__(self, attrib_dict):
        # number_of_lines and number_of_columns define the 2D map matrix dimensions
        # initial_x and initial_y are the true absolute position in the window
        # y_axis_orientation:  y_axis_orientation: -1 (up -> bottom) or 1 (bottom -> up)
        # square_size represents the square's width and the square's height in pixels
        valid_attributes = ("number_of_lines", "number_of_columns", "square_size",
            "initial_x", "initial_y", "y_axis_orientation")
        for key in valid_attributes:
            self.__dict__[key] = attrib_dict[key]
        # boolean that represents game paused state (true if game is paused, otherwise false)
        self.is_paused = False
        # Instance from player class
        # Player score
        self.score = 0
        self.player = None
        self.player_is_dead = False
        # Player's snake list of segments
        self.player_squares = []
        # Snake food position (random)
        self.food_map_x = random.randint(1, self.number_of_columns-2)
        self.food_map_y = random.randint(1, self.number_of_lines-2)
        # Building 2D map by adding 1D lines of square to a 2D matrix
        self.map_squares = []
        for i in range(self.number_of_lines):
            line_of_squares = []
            for j in range(self.number_of_columns):
                map_square_config_dict = {
                "x": self.initial_x+(j*self.square_size),
                "y": self.initial_y+(self.y_axis_orientation*i*self.square_size),
                "square_size": self.square_size,
                "map_x": j,
                "map_y": i
                }
                line_of_squares.append(MapSquare(map_square_config_dict))
            self.map_squares.append(line_of_squares)

    # Draw map borders
    def draw_walls(self, surface):
        for i in range(len(self.map_squares)):
            self.map_squares[i][0].draw(surface)
            self.map_squares[i][len(self.map_squares[0])-1].draw(surface)
        for j in range(1, len(self.map_squares[0])):
            self.map_squares[0][j].draw(surface)
            self.map_squares[len(self.map_squares)-1][j].draw(surface)

    # Method build and assign player to the map
    def build_player(self, player):
        self.player = player
        # If player starts pointing to the right
        self.player_squares = []
        if(player.direction == 2):
            for i in range(player.size-1):
                self.player_squares.append(self.map_squares[player.map_y][player.map_x-(player.size-1-i)])
            self.player_squares.append(self.map_squares[player.map_y][player.map_x])

    # Randomize food position inside the map, it is called when the game starts and when the player's snake collides with the food square
    def randomize_snake_food_position(self):

        self.food_map_x = random.randint(1, len(self.map_squares[0])-2)
        self.food_map_y = random.randint(1, len(self.map_squares)-2)
        # Check if the new food randomized position is inside snake. If true, the food position needs to be randomized again.
        need_to_randomize = True
        while(need_to_randomize):
            need_to_randomize = False
            for i in range(len(self.player_squares)):
                if(self.food_map_x == self.player_squares[i].map_x and self.food_map_y == self.player_squares[i].map_y):
                    need_to_randomize = True

    # Draw food as a red square in the map
    def draw_snake_food(self, surface):
        self.map_squares[self.food_map_y][self.food_map_x].draw_snake_food(surface)

    # Check is snake head collided with a food in the map
    def food_player_collision_check(self, map_x, map_y):
        # Compare player head coordinates
        if(map_x == self.food_map_x and map_y == self.food_map_y):
            self.randomize_snake_food_position()
            return True
        return False

    # Check for game over conditions
    def game_over_collision_check(self, map_x, map_y):
        # Check if snake hits the walls
        if(map_x == 0 or map_x == len(self.map_squares[0])-1 or map_y == 0 or map_y == len(self.map_squares)-1):
            self.player_is_dead = True
            return True
        # Check if snakes collides with itself (its own blocks)
        for i in range(len(self.player_squares)-1):
            if(map_x == self.player_squares[i].map_x and map_y == self.player_squares[i].map_y):
                self.player_is_dead = True
                return True    
        return False

    # Update player position ahd check if the player's snake collided with food or if a game should end
    def update_player(self):
        x_offset = 0
        y_offset = 0
        # Directions: 0 = left; 1 = down; 2 = right; 3 = up 
        if(self.player.direction == 2):
            x_offset=1
        if(self.player.direction == 3):
            y_offset=1
        if(self.player.direction == 0):
            x_offset=-1
        if(self.player.direction == 1):
            y_offset=-1
        
        # Check if snake got food (true if snake head is in the same position as the food)
        snake_got_food = self.food_player_collision_check(self.player.map_x+x_offset, self.player.map_y+y_offset)
        # Check for game over, true if any condition for game over is met
        game_over = self.game_over_collision_check(self.player.map_x+x_offset, self.player.map_y+y_offset)
        # The snake is a list of map squares of variable size, the snake is walking through the map by inserting
        # the map square ahead and removing the map square in the tail. If the snake got food, we can extend the snake
        # by simply not deleting the map square in the tail of the snake.
        if(not snake_got_food):
            self.player_squares.pop(0)
        else: 
            # If snake head collided with the food, the score is incremented by 1
            self.score += 1
        self.player_squares.append(self.map_squares[self.player.map_y+y_offset][self.player.map_x+x_offset])
        self.player.map_y += y_offset
        self.player.map_x += x_offset

    # Draw player's snake and its segments (currently, the player's snake head is the blue square)
    def draw_player(self, surface):
        for i in range(len(self.player_squares)):
            if(i == len(self.player_squares) - 1): self.player_squares[i].draw_player_head(surface)
            else: self.player_squares[i].draw_player(surface)








