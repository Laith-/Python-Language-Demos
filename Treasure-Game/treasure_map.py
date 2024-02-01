import math

class TreasureMap:
    
    TREE_CHAR = " |"           # represents tree
    UNSEARCHED_CHAR = " ."     # represents unsearched location
    PLAYER_SCORE = 0           # represents how many chests player found
    PIRATE_SCORE = 0           # represents how many chests pirate found
    
    def __init__(self, size, chests, trees):
        '''
        Initialize treasure map.
        
        Parameters:
            - size (int): 
                Treasure map is square (size rows by size columns); 
                can assume that size is always a positive integer      
            - chests (list): 
                List of tuples (row, col) describing treasure chest locations     
            - trees (list): 
                List of tuples (row, col) describing tree locations
        
        Returns: None
        '''
        self.__treasure_map = size
        self.__chest_positions = chests
        self.__tree_positions = trees
        self.__num_chests_found = 0
        self.searched_pos = []          # coords that have already been searched by player
        
        self.grid = []
        #creates grid
        for i in range(self.__treasure_map):
            self.grid.append([])
        
        #checks coords and appends the required 'tile'
        for row in self.grid:
            for col in range(self.__treasure_map):
                self.tile_coord = (self.grid.index(row),col)
                if self.tile_coord in self.__tree_positions:
                    row.append(self.TREE_CHAR)
                else:
                    row.append(self.UNSEARCHED_CHAR)        
        
   
    def display_map(self):
        '''
        Print treasure map in grid format, along with column and row indices.
        
        Parameters: None
        
        Returns: None
        '''
        
        #prints coords for columns
        col = []
        for i in range(self.__treasure_map):
            col.append(str(i))
        print('  ','  '.join(col))
        
        #prints coords and rows
        for row in range(len(self.grid)): 
            print(row,' '.join(self.grid[row]))
        
        
    def is_position_valid(self, position):
        '''
        Checks if position is a searchable location on the treasure map.
        
        Parameters:
            - position (tuple or list): 
                Valid position has values, the row and column
        
        Returns: (Boolean, string)
            - Boolean:
                True if position is valid; 
                False if position has already been searched or contains a tree
            - string:
                Message describing why position is valid or not
        '''        
        
        #assertion errors to check validity of input
        assert  0 <= position[0] < self.__treasure_map and 0 <= position[1] < self.__treasure_map, 'out of range'
        assert float(position[0]).is_integer() and float(position[1]).is_integer(), 'error: not a whole number'
        
        valid = True
        message = 'searching row: '+str(position[0])+', col: '+str(position[1])
        
        if position in self.__tree_positions:
            valid = False

            message = "Cannot search there: there's a tree at that location!"
        elif position in self.searched_pos:
            valid = False
            message = 'Cannot search there: location has already been searched!'             
        else:
            self.searched_pos.append(position) 
        
        return (valid,message)
    
    def calculate_distance(self, pos):
        '''
        Calculate distances between searching position and all treasure chests, according to Pythagorean theorem.
        
        Parameters:
            - pos (tuple of two int): 
                Searching location (row, column)
        
        Returns: container of distances, all rounded to nearest integer
        '''
        distances = []
        #uses pythagorean theorem to find distance
        for chest in self.__chest_positions:
            b = pos[0] - chest[0]
            c = pos[1] - chest[1]
            
            a = math.sqrt(b**2 + c**2)
            distances.append(int(round(float(a))))

        return distances
 
    
    def closest_chest(self, distances):
        '''
        Determines the distance to the closest treasure chest, and if that
        distance is within reportable range of the current search position.
        
        Parameters:
            - distances (container of integers):
                Distances between current searching position and all chests
                
        Returns: (Boolean, int)
            - Boolean:
                True if distance to closest chest is not greater than half the number of columns in treasure map;
                False otherwise
            - int:
                Distance to closest chest
        '''
        sorted_distances = sorted(list(distances))
        least = sorted_distances[0]
        valid = False
        
        if least <= (self.__treasure_map/2):
            valid = True
            
        return (valid,least)
    
    def update_map(self, pos, player):
        '''
        Update treasure map with an 'X' if treasure is found at searching
        position, or a hint as to how far the closest treasure chest is from
        searching position.
        
        Parameters:
            - pos (tuple of ints): 
                Current searching location (row, column)      
            - player (int)
                Even number indicates that it's currently the player's turn; 
                Odd number indicates that it's currently the pirate's turn.     
        
        Returns: (int)
            - number of treasure chests found at current position (1 or 0)
        '''        
        turn = player%2
        distances = self.calculate_distance(pos)
        valid = self.closest_chest(distances)
        chests_found = 0

        player = ' '
        if turn == 1:
            player = 'P'

        if pos in self.__chest_positions:
            self.grid[pos[0]][pos[1]] = player+'X'
            self.__num_chests_found += 1
            chests_found = 1
            if turn == 0:
                print('Treasure found by player!\n')
                self.PLAYER_SCORE += 1
            else:
                print('Treasure found by pirate!\n')
                self.PIRATE_SCORE += 1
        elif valid[0]:
            if turn == 0:
                self.grid[pos[0]][pos[1]] = ' '+str(valid[1])
            else:
                self.grid[pos[0]][pos[1]] = 'P'+str(valid[1])
            chests_found = 0
        else:
            self.grid[pos[0]][pos[1]] = ' u'
            chests_found = 0
            
        return chests_found
             
    def auto_pirate(self):
        '''
        Find the first searchable position, starting at position (0, 0) and
        searching each column, then moving down a row and searching each column,
        etc.  
        
        Parameters: None
        
        Returns: (tuple)
            - tuple of 2 integers, representing the first valid position for
              the pirate to search (row, column)
        '''
        #returns first tile that is unsearched
        for x in range(self.__treasure_map):
            for y in range(self.__treasure_map):
                if self.grid[x][y] == self.UNSEARCHED_CHAR:
                    return (x,y)
        
    def is_hunt_over(self):
        '''
        Treasure hunt is over when all treasure chests have been found.
        
        Parameters: None
        
        Returns: Boolean
            - Boolean: True if all chests have been found; False otherwise
        '''        
        # delete pass and complete this method
        return self.__num_chests_found == len(self.__chest_positions)
    
    def chests_remaining(self):
        return len(self.__chest_positions) - self.__num_chests_found
    
    def fetch_score(self):
        return(self.PLAYER_SCORE,self.PIRATE_SCORE)
    
if __name__ == "__main__":
    '''
    tests are made by manipulating values and looking at output and seeing if it's expected
    '''
    
    # test init and display_map methods: should match sample output in assignment description.
    size = 5
    chests = [(1,1), (0,0)]
    trees = [(0,1), (2,3), (0,4)]

    game_map = TreasureMap(size, chests, trees)
    game_map.display_map()
        
    # test update map: does it work correctly when treasure chest location is guessed by player
    #expect X OR PX for chests depending on if player or pirate   
    pos = (1,1)
    
    found = game_map.update_map(pos, 0)
    
    game_map.display_map()
    
    # test update map: does it work correctly when player searches close to treasure chest location
    #expect 1 OR P1 for inrange guesses depending on if player or pirate    
    pos = (2,2)
    
    found = game_map.update_map(pos, 0)
    
    game_map.display_map()    
    # test update map: does it work correctly when player searches far from treasure chest location
    #expect u for out of range guesses 
    pos = (4,4)
    
    found = game_map.update_map(pos, 0)
    
    game_map.display_map()      
    # same update map tests as above, but for pirate: Do you get what you expect?
    #expect X OR PX for chests depending on if player or pirate
    #expect u for out of range guesses 
    #expect 1 OR P1 for inrange guesses depending on if player or pirate
    pos = (0,0)
    
    found = game_map.update_map(pos, 1)
    
    game_map.display_map()
    
    pos = (2,1)
    
    found = game_map.update_map(pos, 1)
    
    game_map.display_map()
    
    pos = (4,3)
    
    found = game_map.update_map(pos, 1)
    
    game_map.display_map()     
    # additional tests for the rest of the methods: what do you expect for each test?
    
    #test is_position_valid
    #expect either a tuple or an assertion error
    try:
        print(game_map.is_position_valid((4,0)))
    except AssertionError as e:
        print(e)
    
    #test calculate_distance
    #expect list with distances rounded to nearest int
    test = game_map.calculate_distance((1,1))
    print(test)
    
    #test closest_chest
    #expect lowest value from calculate_distance
    close = game_map.closest_chest(test)
    print(close)
    
    #check hunt over
    #expect True bool when all chests are found
    print(game_map.is_hunt_over())
    
    #test auto pirate
    #expcet tuple of first valid search pos
    print(game_map.auto_pirate())
    
    
    test = game_map.calculate_distance((1,2))
    close = game_map.closest_chest(test)
    print(close)    
    