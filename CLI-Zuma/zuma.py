from stack import Stack
from queue import Queue
from dll import DoublyLinkedList
from scoreboard import Scoreboard

    
class Zuma:
    """
    Defines the Zuma game and its text-based interface.
    """
   
    # constants used to identify specific user actions based on keyboard input.
    # Don't change these.
    MOVE_LEFT = 'a'
    MOVE_RIGHT = 'd'
    FIRE = 'w'
    QUIT = '/'

    # constants for displaying the game's state on screen. Don't change these.
    UP_ARROW = chr(8593)
    BOMB_CHARACTER = '*'
    
    
    def __init__(self, max_line_length, start_line_length, frames_per_globe,
                 game_globes, player_globes):
        """
        Sets up the game's state to play a new game.

        Parameters:
          max_line_length (int): the maximum number of globes that can be visible 
            before the game over condition is triggered (game lost).

          start_line_length (int): the number of globes that are visible at the 
            start of the level.

          frames_per_globe (int): the number of frames that pass before a new 
            globe appears on screen.

          game_globes (str): a sequence of values that will be used to initialize
            the visible globes and pending globes.

          player_globes (str): a sequence of values that will be used to initialize
            the globes that players can shoot/fire.
        """
        # globe containers
        self.__visible_globes = DoublyLinkedList()
        self.__pending_globes = Queue()
        self.__player_globes  = Stack()
        
        # additional private attributes
        self.__score = 0            
        self.__quit = False
        self.__player_position = 0  # index where player will insert a globe 
        self.__frame_count = 0      # num of frames since game started
        self.__frames_per_globe = frames_per_globe
        self.__frames = frames_per_globe
        self.__max_line_length = max_line_length # max len of visible globes, else game over
        
        self.right_pad = 0
        self.left_pad = self.get_line_length() - 2

        ########################################################################
        ########### COMPLETE THE INITIALIZATION OF THE ZUMA CLASS HERE #########
        ########################################################################
        
        player_globes = list(player_globes)
        game_globes = list(game_globes)
            
        max_display = len(game_globes) - max_line_length
        
        if len(game_globes) > max_line_length:
            for i in range(max_line_length):
                self.__visible_globes.append(game_globes[i])
                
            for i in range(max_display, len(game_globes)):
                self.__pending_globes.enqueue(game_globes[i])
        else:
            for i in game_globes:
                self.__visible_globes.append(i)
                
                
        for i in player_globes:
            self.__player_globes.push(i)
            
        self.visible_globes()
            

    ############################################################################
    # public interface -- do not edit this method.
    ############################################################################
    def play(self):
        """
        Runs the game's gameplay loop.
        """
        # display our frame zero before prompting for input the first time
        self.__display_frame()
        
        while not self.__check_game_over():
            self.__frame_count += 1
            self.__handle_input()
            self.__update_state()
            if not self.__quit:
                self.__display_frame() # display updated header + board + instructions

        # return to normal input handling after the game has finished
        self.__display_game_over()
        
    
    ############################################################################
    # public interface -- complete for the assignment.
    ############################################################################
    def get_score(self):
        """
        Returns the player's score in the game.
        """
        return self.__score

    ############################################################################
    # private methods -- to be completed for assignment.
    ############################################################################
    def __display_header(self):
        """
        Displays the player's score, the number of globes pending to be added to
        the globe row, the number of globes the shooter globes left, and the 
        number of turns remaining before a new globe automatically appears in 
        the visible globe line. The header will be printed before/above the game 
        board.
        """
        print('Score                :', self.get_score())
        print('Globes Remaining     :', self.get_pending_globes())
        print('Shooting Globes      :', self.get_player_globes())
        print('Turns Until New Globe:', self.get_turns_remaining())
        
                                             
    def __display_game_board(self):
        """
        Displays the game board's current state
        """
        
        self.visible_list = self.__visible_row 
        
        print('+' + '='*self.get_line_length() + '+')
        print('|', ' '.join(self.visible_list) + '|'.rjust(1 + self.get_line_length() - len(self.visible_list)*2))
        print('|' + ' ' * self.__player_position, '↑', '|'.rjust(self.left_pad)) 
        print('|' + ' ' * self.__player_position, self.get_next_globe(), '|'.rjust(self.left_pad))
        print('+' + '='*self.get_line_length() + '+')
            
    def __move_left(self):
        """
        Moves the player's shooting position one space to the left. Cannot move 
        to a negative position.
        """
        if self.__player_position > 0:
            self.__player_position -= 1
            self.left_pad += 1
            
    def __move_right(self):
        """
        Moves the player's shooting position one space to the right. Cannot move
        to a position greater than the number of globes on the screen.
        """
        if self.__player_position < self.get_line_length() - 3:
            self.__player_position += 1
            self.left_pad -= 1
        
    def __fire(self):
        """
        Removes the next globe from player globes and inserts it into the 
        visible globes at the player's shooting position. Does not allow a globe
        to be inserted if the player's position is out of bounds of the length of
        the visible globes. This method should NOT check for match-threes.
        """
        self.visible_list.insert(self.__player_position - 1, self.__player_globes.pop())
        
    def __handle_match_three(self, combo_length=1):
        """
        Removes all sequences of 3 or more matching globes in the visible globe
        line and returns the points earned from those match-3s.
        """
        for i in range(0,len(self.visible_list) - 2):
            current = i
            
        
    def __update_state(self):
        """
        Updates our game's current state.
          Check if any bombs are visible. If so, detonate them.
          Check if any 3-in-a-rows exist. If so, remove and score them.
          Check if a new globe needs to be added to the visible globes list. If
          so, add the new globe.
        """
        #adding new globe
        if self.get_turns_remaining() == 0:
            if not self.__visible_globes.is_empty:
                self.visible_list.insert(0, self.__visible_globes.pop())
            else:
                self.visible_list.insert(0, self.__pending_globes.dequeue())
            self.__frames_per_globe = self.__frames
        else:
            self.__frames_per_globe -= 1
            
        #bombs
        self.__handle_bombs()
        
        #3's
        self.__handle_match_three()
            
    def __check_game_over(self):
        """
        Checks if game over conditions have been met. If so, change our relevant
        game state variables.

        Lose condition: the visible globes line is at maximum capacity

        Win Condition: no globes in the pending globe line
          
        End game prematurely: by entering quit action.

        All result in the game being over.
        """
        game_over = False
        
        if len(' '.join(self.visible_list)) >= self.get_line_length() - 2:
            game_over = True
            
        return game_over
        

    def __display_game_over(self):
        """
        Displays appropriate game over message to the player.
        """
        print('===============================================================================')
        print('                             Game Over: try again!                             ')
        print('===============================================================================')
        
        
        
    def __handle_bombs(self):
        """
        Removes all bombs from the visible globe line. When bombs are removed,
        they explode and destroy the globe to either side. Explosions do not 
        earn any points.
        """
        bomb = '*'
        
        if bomb in self.visible_list:
            bomb_index = self.visible_list.index(bomb)
            if bomb_index > 0:
                before = bomb_index - 1
                self.visible_list.pop(before)
                
            if bomb_index < len(self.visible_list) - 1:
                after = bomb_index + 1
                self.visible_list.pop(after)
                
            
            self.visible_list.remove(bomb)
            
            return True
        
        return False
            
    ############################################################################
    # private methods -- define your own private methods here.
    ############################################################################

    def get_pending_globes(self):
        return len(self.__pending_globes)
    
    def get_player_globes(self):
        return len(self.__player_globes)
    
    def get_turns_remaining(self):
        return self.__frames_per_globe
    
    def get_line_length(self):
        return int(self.__max_line_length)
    
    def get_next_globe(self):
        return self.__player_globes.peek()
    
    def visible_globes(self):
        visible = [] 
        for i in range(4):
            visible.append(self.__visible_globes.pop())
        
        self.__visible_row = visible   
    

    ############################################################################
    # private methods -- do not edit these.
    ############################################################################
    def __display_frame(self):
        """
        Displays one frame of the game
        """
        self.__display_header()
        self.__display_game_board()
        self.__display_commands()
        
    def __display_commands(self):
        """
        Displays all of the input commands to the screen
        """
        print("Move Left  : " + Zuma.MOVE_LEFT)
        print("Move Right : " + Zuma.MOVE_RIGHT)
        print("Fire       : " + Zuma.FIRE)
        print("Quit       : " + Zuma.QUIT)
        
    def __handle_input(self):
        """
        Listens for and responds to keyboard input. Returns True if valid input
        was received and False otherwise.
        """
        char = input("> ").strip()
        if char == Zuma.MOVE_LEFT:
            self.__move_left()
        elif char == Zuma.MOVE_RIGHT:
            self.__move_right()
        elif char == Zuma.FIRE:
            self.__fire()
        elif char == Zuma.QUIT:
            self.__quit = True
        else:
            # ignore all other key presses
            return False
        return True

            

################################################################################
# custom exception class: do not edit
################################################################################
class CustomLevelFileError(Exception):
    """
    Exception type used for raising issues with the format/existence of the
    level input file when game details are read using zuma_from_file. Handled 
    as its own error type so these errors can be caught and reported in a 
    user-friendly way without interfering with generating tracebacks for other 
    errors that will need to be debugged.
    """
    def __init__(self, message):
        self.__message = message
    def __str__(self):
        return self.__message
    
    
################################################################################
# global constants
################################################################################

# If this is toggled to True, the scoreboard will be enabled. A high score
# board will be displayed at the beginninig and end of a level, and players
# will be prompted to input their name when a level finishes (win or lose)
SCOREBOARD_ON = False


################################################################################
# helper functions: do not edit
################################################################################
def zuma_from_file(filename):
    """
    Initializes a Zuma game from a file
    """
    try:
        fl = open(filename, 'r')
    except FileNotFoundError:
        raise CustomLevelFileError("Input file, {}, does not exist.".format(filename))
    
    # read in our width parameters
    try:
        max_line_length, start_line_length, frames_per_globe = fl.readline().strip().split()
        max_line_length = int(max_line_length)
        start_line_length = int(start_line_length)
        frames_per_globe = int(frames_per_globe)
    except:
        raise CustomLevelFileError("Level file is not correctly formatted.")

    # read in the queue of globes that will appear
    game_globes = fl.readline().strip()

    # read in the queue of globes that players can insert
    player_globes = fl.readline().strip()

    if len(game_globes) == 0 or len(player_globes) == 0:
        raise CustomLevelFileError("Level file is not correctly formatted.")
    
    fl.close()

    # construct and return the game
    game = Zuma(max_line_length, start_line_length, frames_per_globe, game_globes, player_globes)
    return game


def play_without_scoreboard(level_file):
    """
    Plays a level of the game without showing/updating the scoreboard
    """
    game = zuma_from_file(level_file)
    game.play()
    
    
def play_with_scoreboard(level_file):
    """
    Plays a level of the game. Displays scoreboard before/after the game and
    also prompts to update after.
    """
    game = zuma_from_file(level_file)
    
    # start by showing our score board for this level
    scoreboard = Scoreboard("scores.txt")
    scoreboard.display(level_file)
    input("Press Enter to continue> ")
    
    # play the game
    game.play()

    # prompt for name and update the score log if the player has a score
    if game.get_score() > 0:
        name = None
        name_valid = False
        while not name_valid:
            name = input("Enter your name> ")
            if "," in name or len(name) == 0:
                print("Invalid name. Try again.")
            else:
                name_valid = True
        scoreboard.update(name, game.get_score(), level_file)

    # re-display the high scores
    scoreboard.display(level_file)

    
################################################################################
# initialization and main: do not edit
################################################################################
def main():

    # prompt for text file with level setup information
    ask_for_filename = True
    while ask_for_filename:
        try:
            level_file = input('Please enter level text file: ')
            if SCOREBOARD_ON:
                play_with_scoreboard(level_file)
            else:
                play_without_scoreboard(level_file)
            
        except CustomLevelFileError as e:
            print(e)
        # allow other error types to generate a traceback instead of handling; 
        # they are probably things that need to be debugged.        
        else:
            ask_for_filename = False

    
if __name__ == "__main__":
    main()
