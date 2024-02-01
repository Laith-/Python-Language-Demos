from treasure_map import TreasureMap

# function definitions go here

def main():
    error = True
    
    file_dir = input('Enter name of text file to initialize treasure map: ')
    
    while error:
        if file_dir.endswith('.txt'):
            error = False
        else:
            file_dir = input('Invalid file extension. Enter name of text file to initialize treasure map: ')
    try:    
        parameters = get_parameters(file_dir)
    except Exception as e:
        print(e)
    else:
        size = parameters[0]
        chests = parameters[1]
        trees = parameters[2]
        turn = 0
        
        play_again = True
        
        play_game(size,chests,trees,turn)
    

def play_game(size,chests,trees,turn):
    '''
    calls for game object and oversees the game by keeping turns and running it in a loop
    
    parameters:
        - size: size of map
        - chests: number of chests on map
        - trees: number of trees on map
        - turn: turn of player. even number = player turn, odd number = pirate turn
        
    returns: none
        
    '''        
    game_over = False
    while not game_over:
        game = TreasureMap(int(size),chests,trees)
        game.display_map()
        print('\n{} treasure chest(s) still hidden.\n'.format(str(game.chests_remaining())))
        while not game.is_hunt_over(): 
            if turn%2 == 0:
                #players turn
                print('Enter search coordinates: row col')
                player_input = input('>>')
                
                valid_coord = check_coord(player_input,size)
                valid = valid_coord[0]
                message = valid_coord[1]
                if valid:
                    turn_played = run_turn(valid_coord[2],turn,game)
                    if turn_played:
                        turn += 1
                else:
                    print(message)
                                        
            else:
                #pirates turn
                pirate_input = game.auto_pirate() # assuming pirate pos is always valid
                turn_played = run_turn(pirate_input,turn,game)
                if turn_played:
                        turn += 1
        score = game.fetch_score()
        print('You have found {} chests(s).'.format(score[0]))
        print('The pirate found {} chests(s).'.format(score[1]))  
        
        game_over_input = input('\nWould you like to start a new treasure hunt? [Y/N] ')
        if game_over_input.lower() == 'n':
            print('Goodbye.')
            game_over = True

def run_turn(pos,turn,game):
    '''
    calls all appropriate methods for the turn to play out
    
    parameters:
        - pos: player position
        - turn: number identifying whos turn it is
        - game: game object
    returns
        - bool: True if played out, False if not 
    '''    
    turn_played = True
    try:
        pos_valid = game.is_position_valid(pos)
        if pos_valid[0]:
            if turn%2 == 0:
                distances = game.calculate_distance(pos)
                update = game.update_map(pos,turn)  
                game.display_map()
                remaining = game.chests_remaining()
                if remaining > 0:
                    print('\n{} treasure chest(s) still hidden.\n'.format(str(remaining)))
                else:
                    print('\nAll treasure has been found!')
                                      
            
            else:
                print('Pirate is {}'.format(str(pos_valid[1])))
                distances = game.calculate_distance(pos)
                update = game.update_map(pos,turn)  
                game.display_map()
                remaining = game.chests_remaining()
                if remaining > 0:
                    print('\n{} treasure chest(s) still hidden.\n'.format(str(remaining)))
                else:
                    print('\nAll treasure has been found!')
                                      
                    
        else:
            print(pos_valid[1])
            turn_played = False
            
    except AssertionError as e:
        print(e)
        
    return turn_played
    

def get_parameters(file_dir):
    '''
    opens file and gets size chests and trees
    
    parameters:
        - file dir
    returns
        - size as index 0
        - chests as index 1
        - trees as index 2
    '''
    size = 0
    chests = []
    trees = []
    try:
        file = open(file_dir, 'r').read().strip().split()
    except FileNotFoundError:
        raise Exception("[Errno 2] No such file or directory: '{}'".format(str(file_dir)))
        
    else:
        for line in file:
            line = line.split(':')
            
            try:
                if type(int(line[0])) is int:
                    size = line[0]
            except ValueError:
                pass
               
            if line[0].upper() == 'TREASURE':
                coord = []
                for i in line[1].split(','):
                    coord.append(int(i))
                chests.append(tuple(coord))
                
            elif line[0].upper() == 'TREE':
                coord = []
                for i in line[1].split(','):
                    coord.append(int(i))
                trees.append(tuple(coord))
            
    return(size,chests,trees)

def check_coord(coord,size):
    '''
    checks for validity of user input
    ---check if theres 2 coords
    ---check if all coords are int
    ---check if coords are in range
    
    parameters:
        -coord: coords player inputed
        -size: range of acceptable coords
        
    return:
        -error (if there is one)
        -bool (True if coords are valid, False if error needs to be displayed)
        -coord: returns the player input, only converts to tuple for later use if input is valid
    '''
    error = ''
    valid = True
    final_coord = ()
    
    coord = coord.split()
    if ' ' in coord:
        coord.remove(' ')
    
    if len(coord) != 2:
        valid = False
        error = 'Incorrect number of coordinate values entered'
        
    elif len(coord) == 2:
        for i in coord:
            try:
                if 0 <= int(coord[0]) >= int(size):
                    valid = False
                    error = 'row-coordinate out of range'
                elif 0 <= int(coord[1]) >= int(size):
                    valid = False
                    error = 'col-coordinate out of range'
                
            except ValueError:
                valid = False
                error = 'Incorrect type of coordinate values entered' 
            else:
                for i in range(len(coord)):
                    coord[i] = (int(coord[i]))
                final_coord = tuple(coord)
           
    return (valid,error,final_coord)     
        
if __name__ == "__main__":
    main()