import pygame
from map import Map, Player

# Receives input (keyboard keys) and decides the course of action
def decide_input(map, event_key, is_valid_movement):
    
    # Setting directions
    left_direction = 0
    down_direction = 1
    right_direction = 2
    up_direction = 3

    # Player input changes snake directions
    if event_key == pygame.K_UP and map.player.direction != down_direction and is_valid_movement == True and not map.is_paused:
        map.player.direction = up_direction
        return False
    if event_key == pygame.K_DOWN and map.player.direction != up_direction and is_valid_movement == True and not map.is_paused:
        map.player.direction = down_direction
        return False
    if event_key == pygame.K_RIGHT and map.player.direction != left_direction and is_valid_movement == True and not map.is_paused:
        map.player.direction = right_direction
        return False
    if event_key == pygame.K_LEFT and map.player.direction != right_direction and is_valid_movement == True and not map.is_paused:
        map.player.direction = left_direction
        return False
    # Pause and unpause the game
    if event_key == pygame.K_SPACE and not map.player_is_dead:    
        if(map.is_paused):
            map.is_paused = False
        else:
            map.is_paused = True
    # Restart a game
    if event_key == pygame.K_SPACE and map.player_is_dead:
        # Reset player
        # map_x and map_y are abstract coordinates to represent the player's snake or food inside the 2D map matrix
        # Directions: 0 = left; 1 = down; 2 = right; 3 = up 
        # size: Player's snake number of segments
        player_configuration_dict = {
        'map_x': 10,
        'map_y': 5,
        'size': 3,
        'direction': 2
        }
        player = Player(player_configuration_dict)
        map.build_player(player)
        map.player_is_dead = False
        # Reset score
        map.score = 0
        # Ensures game is reseted
        map.is_paused = False
    return True

def draw_text_on_screen(font, screen, map):

    # RGB colors
    color_black = 0, 0, 0

    # Misc texts
    game_over_text = font.render("Game Over", 1, color_black)
    restart_text = font.render("Press SPACE to restart", 1, color_black)
    score_text = font.render("Score: "+str(map.score), 1, color_black)
    pause_text =font.render("Press SPACE to pause", 1, color_black)
    resume_text = font.render("Press SPACE to resume", 1, color_black)
    #fps_text = font.render("FPS: {:.2f}".format(fps_clock.get_fps()), 1, color_black)
    
    # Draw texts related to FPS and score on screen
    screen.blit(score_text, (map.initial_x, map.initial_y-(map.square_size*len(map.map_squares))-font.get_height()/2))
    #screen.blit(fps_text, (map.initial_x, map.initial_y-(map.square_size*len(map.map_squares))-(3*font.get_height()/2)))
    # Draw texts related to game over and restarting if player is dead
    if(map.player_is_dead):
        screen.blit(game_over_text, ((map.square_size*len(map.map_squares[0]))-game_over_text.get_width(), map.initial_y-(map.square_size*len(map.map_squares))-font.get_height()/2))
        screen.blit(restart_text, (map.initial_x, map.initial_y+font.get_height()))
    # Draw text:
    elif(not map.is_paused): 
        screen.blit(pause_text, (map.initial_x, map.initial_y+font.get_height()))
    # Draw text related to resuming the game if the player is not dead and the game is paused
    else: 
        screen.blit(resume_text, (map.initial_x, map.initial_y+font.get_height()))

def main():
    
    # Screen dimensions
    screen_dimensions = width, height = 720, 720

    # Map configuration and creation

    # Border offset is the distance between the window borders and the map borders
    border_offset = 4
    # number_of_lines and number_of_columns define the 2D map matrix dimensions
    # initial_x and initial_y are the true absolute position in the window
    # y_axis_orientation:  y_axis_orientation: -1 (up -> bottom) or 1 (bottom -> up)
    # square_size represents the square's width and the square's height in pixels
    map_configuration_dict = {
    'square_size': 15,
    'y_axis_orientation': -1
    }
    map_configuration_dict['number_of_lines'] = int(screen_dimensions[1]/map_configuration_dict['square_size']) - (2*border_offset)
    map_configuration_dict['number_of_columns'] = int(screen_dimensions[0]/map_configuration_dict['square_size']) - (2*border_offset)
    map_configuration_dict['initial_x'] = (map_configuration_dict['square_size']*border_offset)
    map_configuration_dict['initial_y'] = screen_dimensions[1] - (map_configuration_dict['square_size']*(border_offset+1))
    map = Map(map_configuration_dict)

    # Creating player

    # map_x and map_y are abstract coordinates to represent the player's snake or food inside the 2D map matrix
    # Directions: 0 = left; 1 = down; 2 = right; 3 = up 
    # size: Player's snake number of segments
    player_configuration_dict = {
    'map_x': 10,
    'map_y': 5,
    'size': 3,
    'direction': 2
    }
    player = Player(player_configuration_dict)

    # Build and assign player to the map
    map.build_player(player)

    # Flag/Boolean to validate movement (example: ensuring only one direction change happens per game step)
    is_valid_movement = True

    # Initializing pygame and font
    pygame.init()
    pygame.font.init()

    # RGB from 0 to 255
    color_black = 0, 0, 0
    color_white = 255, 255, 255

    # Set game window title
    pygame.display.set_caption('Snake Game')

    # Screen creation
    screen = pygame.display.set_mode(screen_dimensions)

    # Font creation
    font_size = 20
    monospace_font = pygame.font.SysFont("monospace", font_size)

    # Timed event
    game_step_timed_event = pygame.USEREVENT + 1
    game_step_delay = 130
    pygame.time.set_timer(game_step_timed_event, game_step_delay)

    # Defined FPS and FPS clock creation
    FPS_target = 63
    fps_clock = pygame.time.Clock()

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False      
            if event.type == pygame.KEYDOWN:
                is_valid_movement = decide_input(map, event.key, is_valid_movement)
            # Update the game for each game step (currently 130 milliseconds)
            if event.type == game_step_timed_event:
                if(not map.player_is_dead and not map.is_paused):
                    map.update_player()
                # Fill background with white color, quite inefficient operation as all pixels in the screen are repainted
                screen.fill(color_white)
                draw_text_on_screen(monospace_font, screen, map)
                # Draw map walls (borders), player snake and snake food
                map.draw_walls(screen)
                map.draw_player(screen)
                map.draw_snake_food(screen)
                is_valid_movement = True  
       
        # Update game cycle based on a fps target
        fps_clock.tick(FPS_target)
        # Update and possibly repaint window
        pygame.display.update()

if __name__ == "__main__": main()