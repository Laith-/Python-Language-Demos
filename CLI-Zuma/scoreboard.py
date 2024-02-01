"""
Implements a Scoreboard class. Scoreboards track scores, names, and levels.
"""
from dll import DoublyLinkedList

# You should read this file, but...
###############################################################################
########################## YOU MAY NOT EDIT THIS FILE #########################
###############################################################################


class Scoreboard:
    def __init__(self, logfile):
        """
        Load the score board from file. Filename is a file used to store records
        of previous play. Each record is on its own line and contains three
        parts: a name, a score, and a level. 
        """
        self.__records = DoublyLinkedList()
        self.__logfile = logfile

        # read in all of our records
        try:
            fl = open(self.__logfile, 'r')
        # no high scores have been created yet; nothing to read
        except FileNotFoundError:
            pass
        else:
            for line in fl:
                name, score, level = line.strip().split(",")
                record = Record(name, int(score), level)
                self.__records.append(record)
            fl.close()

            
    ###########################################################################
    # public interface
    ###########################################################################
    def display(self, level, n=10):
        """
        Display the top n (default, 10) high scores for a specified level. If
        n records for that level do not exist, they should be left as blank
        lines.
        """
        # filter records by only those on this level
        filtered_list = DoublyLinkedList()
        for record in self.__records:
            if record.get_level() == level:
                filtered_list.append(record)

        # sort the records that we found
        filtered_list.sort()
                
        # build the score board display based on the sorted, filtered records
        print((" " + level + " ").center(79, "="))
        for i in range(n):
            name = ""
            score= ""
            if i < len(filtered_list):
                record = filtered_list[i]
                name = record.get_name()
                score = record.get_score()
            print("  {:>2}. {:<40} {:>31}".format(i+1, name, score))
        print("="*79)
        
    def update(self, name, score, level):
        """
        Updates our records with a new entry. This includes our list of loaded
        records, but also saves the new record to our log file.
        """
        new_record = Record(name, score, level)
        self.__records.append(new_record)
        
        fl = open(self.__logfile, 'a')
        fl.write(str(new_record) + "\n")
        fl.close()


################################################################################
# record class
################################################################################
class Record:
    """
    The record class holds information about one "play" of a game. Includes
    player's name, their score, and which level they played.
    """
    def __init__(self, name, score, level):
        self.__name = name
        self.__score = score
        self.__level = level

    def get_name(self):
        """returns the name for this record"""
        return self.__name

    def get_score(self):
        """returns the score for this record"""
        return self.__score

    def get_level(self):
        """returns the level for this record"""
        return self.__level
        
    def __lt__(self, other):
        """implements less than comparison to other records, based on scores"""
        assert type(other) == Record, "Can only be compared to other records."
        return self.__score < other.__score
    
    def __gt__(self, other):
        """implements greater than comparison to other records, based on scores"""
        assert type(other) == Record, "Can only be compared to other records."
        return self.__score > other.__score

    def __eq__(self, other):
        """implements equals comparison to other records, based on scores"""
        assert type(other) == Record, "Can only be compared to other records."
        return self.__score == other.__score

    def __str__(self):
        """
        returns a string representation of the record; name, score, and level
        separated by commas.
        """
        return "{},{},{}".format(self.__name, self.__score, self.__level)
