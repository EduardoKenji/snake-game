import pygame
import random

class MapSquare:
    def __init__(self, x, y, square_size, map_x, map_y):
        self.x = x
        self.y = y
        self.map_x = map_x
        self.map_y = map_y
        self.square_size = square_size

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
    def __init__(self, map_x, map_y, direction, size):
        self.map_x = map_x
        self.map_y = map_y
        # Directions: 0 = left; 1 = down; 2 = right; 3 = up 
        self.direction = direction
        self.size = size

# Map class contain a 2D matrix of MapSquares 
class Map:
    # y_axis_orientation: -1 (up -> bottom) or 1 (bottom -> up)
    def __init__(self, number_of_lines, number_of_columns, square_size, initial_x, initial_y, y_axis_orientation):
        
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.square_size = square_size
        self.is_paused = False
        # Instance from player class
        self.score = 0
        self.player = None
        self.player_is_dead = False
        self.player_squares = []
        # Snake food
        self.food_map_x = random.randint(1, number_of_columns-2)
        self.food_map_y = random.randint(1, number_of_lines-2)
        # Building 2D map by adding 1D lines of square to a 2D matrix
        self.map_squares = []
        for i in range(number_of_lines):
            line_of_squares = []
            for j in range(number_of_columns):
                line_of_squares.append(MapSquare(initial_x+(j*square_size),initial_y+(y_axis_orientation*i*square_size), square_size, j, i))
            self.map_squares.append(line_of_squares)

    # Draw map borders
    def draw_walls(self, surface):
        for i in range(len(self.map_squares)):
            self.map_squares[i][0].draw(surface)
            self.map_squares[i][len(self.map_squares[0])-1].draw(surface)
        for j in range(1, len(self.map_squares[0])):
            self.map_squares[0][j].draw(surface)
            self.map_squares[len(self.map_squares)-1][j].draw(surface)

    # Method to assign player to the map
    def build_player(self, player):
        self.player = player
        # If player starts pointing to the right
        self.player_squares = []
        if(player.direction == 2):
            for i in range(player.size-1):
                self.player_squares.append(self.map_squares[player.map_y][player.map_x-(player.size-1-i)])
            self.player_squares.append(self.map_squares[player.map_y][player.map_x])

    def randomize_snake_food_position(self):
        self.food_map_x = random.randint(1, len(self.map_squares[0])-2)
        self.food_map_y = random.randint(1, len(self.map_squares)-2)

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

    # Update player position
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
        
        # Check if snake got food
        snake_got_food = self.food_player_collision_check(self.player.map_x+x_offset, self.player.map_y+y_offset)
        # Check for game over, true is any condition for game over is met
        game_over = self.game_over_collision_check(self.player.map_x+x_offset, self.player.map_y+y_offset)
        # The snake is a list of map squares of variable size, the snake is walking through the map by inserting
        # the map square ahead and removing the map square in the tail. If the snake got food, we can extend the snake
        # by simply not deleting the map square in the tail of the snake.
        if(not snake_got_food):
            self.player_squares.pop(0)
        else: 
            # If snake got food, score is incremented by 1
            self.score += 1
        self.player_squares.append(self.map_squares[self.player.map_y+y_offset][self.player.map_x+x_offset])
        self.player.map_y += y_offset
        self.player.map_x += x_offset

    # Draw player and its segments (head is blue)
    def draw_player(self, surface):
        for i in range(len(self.player_squares)):
            if(i == len(self.player_squares) - 1): self.player_squares[i].draw_player_head(surface)
            else: self.player_squares[i].draw_player(surface)








