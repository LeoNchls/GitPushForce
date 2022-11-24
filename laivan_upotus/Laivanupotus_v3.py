"""

Projekti: Laivanupotus. Ohjelma lukee annetusta tiedostosta laivojen tietoja
          muodossa "Laivan_tyyppi;koordinaatti_1;...;koordinaatti_n". Sitten
          käyttäjä   voi   antamillaan   koordinaateilla   ampua  "ohjuksia"
          koordinaatteihin.  Jos  ohjus  osuu,  laiva,  johon  se osui ottaa
          vahinkoa.  Kun  kaikki  laivat  on  upotettu,  peli  päättyy  ja
          käyttäjä voittaa.

StudentId               x
Firstname Lastname      Leo Mandara
Email                   x
"""

# all the ship types and their respective healths.
SHIP_TYPES = {
    "battleship": 4,
    "cruiser": 3,
    "destroyer": 2,
    "submarine": 1
}

# global variables. I used these so that I could extend the board easily if
# I wanted to.
BOARD_COLUMNS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
NUMBER_OF_ROWS = 10
QUIT_COMMAND = "Q"


class Ship:

    def __init__(self, ship_type, list_of_coordinates):

        # type of ship
        self.__ship_type = ship_type

        # all coordinates the ship covers
        self.__coordinate_list = list_of_coordinates

        # how many hits the ship can sustain before sinking
        self.__ship_health = SHIP_TYPES[ship_type]

    def get_ship_type(self):
        """Getter for ship type

        :return: str, ship type
        """

        return self.__ship_type

    def get_coordinate_list(self):
        """Getter for coordinate list

        :return: list, list of ship coordinates
        """

        return self.__coordinate_list

    def get_ship_health(self):
        """Getter for amount of sunken coordinates

        :return: int, amount of sunken coordinates
        """

        return self.__ship_health

    def overlap(self, other_ship):
        """Checks if self overlaps with other_ship

        :param other_ship: Ship, other ship
        :return: bool, True if overlap is found
        """

        overlap = False

        for coordinate in self.get_coordinate_list():
            if coordinate in other_ship.get_coordinate_list():
                overlap = True

        return overlap

    def is_sunken(self):
        """Determines whether all ship parts have been sunken

        :return: bool, True if ship health is less than 1
        """

        return self.get_ship_health() < 1

    def take_damage(self):
        """Reduces ship health by one

        :return:
        """

        self.__ship_health -= 1


class Board:

    # A matrix to emulate the board. Letters are referred to as columns,
    # numbers as rows.
    #   A B C D E F G H I J
    # 0                     0
    # 1                     1
    # 2                     2
    # 3                     3
    # 4                     4
    # 5                     5
    # 6                     6
    # 7                     7
    # 8                     8
    # 9                     9
    #   A B C D E F G H I J

    def __init__(self, number_of_rows=NUMBER_OF_ROWS,
                 board_columns=BOARD_COLUMNS):
        """Initializes a board of width len(board_columns) and height of
        number_of_rows

        :param number_of_rows: int, number of rows
        :param board_columns: list, list of row letters
        """

        self.__dict_of_columns = {}
        self.__board_columns = board_columns
        self.__number_of_rows = number_of_rows

        # constructs dictionary where keys are column letters and payloads are
        # lists with as many values as there are rows
        for column_letter in self.__board_columns:
            self.__dict_of_columns[column_letter] = []
            for row_number in range(0, self.__number_of_rows):
                self.__dict_of_columns[column_letter].append(" ")

    def get_columns(self):
        """Getter for column letter list

        :return: list, list of column letters of board
        """

        return self.__board_columns

    def get_number_of_rows(self):
        """Getter for number of rows

        :return: int, number of rows
        """

        return self.__number_of_rows

    def printout(self):
        """Prints a board

        :return:
        """

        # blank line before board
        print()

        # prints first column letter to last letter
        print(" ", end="")
        for column_letter in self.get_columns():
            print(f" {column_letter}", end="")
        print("")

        # loop for each row
        for row_number in range(0, self.get_number_of_rows()):
            # print the row number first followed by a space
            print(f"{row_number} ", end="")
            # then each value in the row followed by a space
            for column_letter in self.get_columns():
                print(f"{self.__dict_of_columns[column_letter][row_number]} ",
                      end="")
            # and finally the row number again
            print(f"{row_number}")

        # prints first column letter to last letter
        print(" ", end="")
        for column_letter in self.get_columns():
            print(f" {column_letter}", end="")
        print("")

        # blank line after board
        print()

    def mark_on_board(self, coordinate, marker):
        """Set column list coordinate to marker

        :param marker: str, marker to write on board. Preferably one character
        :param coordinate: str, format "XY", where X=column letter, Y=row num
        :return:
        """

        x_coord = coordinate[0]
        y_coord = int(coordinate[1:])

        # if the given coordinate is on the board
        if not self.bad_coordinate(coordinate):
            self.__dict_of_columns[x_coord][y_coord] = marker
        else:
            print("Invalid coordinate!")

    def get_mark(self, coordinate):
        """Getter for a mark in given coordinate

        :return: str, mark in given coordinate
        :raises: ValueError, if the given coordinate isn't on the board
        """

        if not self.bad_coordinate(coordinate):
            x_coord = coordinate[0]
            y_coord = int(coordinate[1:])
            return self.__dict_of_columns[x_coord][y_coord]
        else:
            raise ValueError()

    def mark_ship_on_board(self, ship_to_mark):
        """Prints a given ship on the board

        :param ship_to_mark: Ship, ship to be printed on board
        :return:
        """

        # capital initial of Ship type
        sunken_mark = ship_to_mark.get_ship_type()[0].upper()
        # marks each one of the sunken Ship's coordinates on the
        # board as sunken_mark
        for coordinate in ship_to_mark.get_coordinate_list():
            self.mark_on_board(coordinate, sunken_mark)

    def bad_coordinate(self, coordinate):
        """Checks if a coordinate is on the board

        :param coordinate: str, coordinate (ex. A1)
        :return: bool, True if the coordinate isn't on the board
        """

        # an empty coordinate is a bad coordinate
        if coordinate.strip() == "":
            return True

        # tests if the coordinates are within the board's range
        try:
            x = coordinate[0]
            y = int(coordinate[1:])

            if x not in self.get_columns() or \
                    y not in range(0, self.get_number_of_rows()):
                return True
            else:
                return False

        # a ValueError always means a bad coordinate. Either x or y is just not
        # the right datatype
        except ValueError:
            return True


def read_lines_from_file(file_name):
    """Reads lines from file and returns a list of them

    :param file_name: str, name of file to read
    :return: list, list of lines in file as strings
    :raises: OSError, if the file can't be read
    """

    list_of_lines = []

    try:
        # open the file
        ship_file = open(file_name, mode="r")
    except OSError:
        raise OSError("File can not be read!")

    # operate on the file
    for line in ship_file:
        # strip each file of empty spaces. Especially important considering
        # line break at the end of each line.
        line_stripped = line.strip()
        # add the stripped line to the list of lines
        list_of_lines.append(line_stripped)

    # close the file
    ship_file.close()

    return list_of_lines


def lines_to_ship_list(list_of_strings, game_board):
    """Compile a list of ships from input list of strings

    :param list_of_strings: list, list of ships in string format
    ship_type;coordinates (example "battleship;A1;A2;A3;A4")
    :param game_board: Board, board to check coordinate validity in relation to
    :return: list, list of Ships
    :raises: ValueError: if there is an error in ship coordinates or there are
    overlapping ships in the file
    """

    ship_list = []

    for ship_unit in list_of_strings:
        # first splits the string into ship type and coordinates
        ship_type, coord_string = ship_unit.split(";", maxsplit=1)
        # then splits all the coordinates into a list
        coord_list = coord_string.split(";")

        # checks if all coordinates are on the board
        for coordinate in coord_list:
            if not game_board.bad_coordinate(coordinate):
                pass
            else:
                raise ValueError("Error in ship coordinates!")

        # turns the ship type and coordinates into a ship
        ship_to_be_added = Ship(ship_type, coord_list)

        # the resulting ship is then checked against other ships already added
        # to the list
        for ship_already_in_list in ship_list:
            if ship_to_be_added.overlap(ship_already_in_list):
                raise ValueError("There are overlapping ships in the "
                                 "input file!")

        ship_list.append(ship_to_be_added)

    return ship_list


def sunken_ships_check(list_of_ships, list_of_sunken_ships, game_board):
    """Updates list_of_sunken_ships according to sunken ships on list_of_ships
    and marks newly sunken ships on the given board

    :param list_of_ships: list, list of all Ships in the game
    :param list_of_sunken_ships: list, list of Ships that have been sunken
    :param game_board: Board, the game board to print on
    :return:
    """

    # goes through all Ships in the game
    for a_ship in list_of_ships:
        # proceeds only if the Ship has sunken but hasn't already been
        # added to the list of sunken Ships
        if a_ship.is_sunken() and a_ship not in list_of_sunken_ships:
            # prints the Ship on the board
            game_board.mark_ship_on_board(a_ship)

            # informs the player
            print(f"You sank a {a_ship.get_ship_type()}!")

            # adds the sunken ship to the list of sunken ships
            list_of_sunken_ships.append(a_ship)


def main():
    # a list to add sunken ships to as they sink
    list_of_sunken_ships = []

    # initialize a board for the game
    game_board = Board()

    # read all the ship info from the file
    try:
        list_of_ship_info = read_lines_from_file(input("Enter file name: "))
    except OSError as error_message:
        print(error_message)
        return

    # turn the lines into Ship objects
    try:
        list_of_ships = lines_to_ship_list(list_of_ship_info, game_board)
    except ValueError as error_message:
        print(error_message)
        return

    # print the game board to start with
    game_board.printout()

    # flag variable for the upcoming loop
    won = False

    # loop for playing the game itself
    while not won:
        players_command = input("Enter place to shoot (q to quit): ")

        # change the player's command to uppercase to simplify handling it
        players_command = players_command.upper()

        if players_command == QUIT_COMMAND:
            print("Aborting game!")
            return

        try:
            # if the coordinate on the board hasn't yet been marked
            if game_board.get_mark(players_command) == " ":
                # initialize marker to be placed on the board in given
                # coordinate
                marker = "*"
                # if the shot hits a ship, change the marker to X and make the
                # ship take damage
                for a_ship in list_of_ships:
                    if players_command in a_ship.get_coordinate_list():
                        marker = "X"
                        a_ship.take_damage()

                    # mark appropriate marker on board
                    game_board.mark_on_board(players_command, marker)

            # if coordinate is valid but has a mark already on it, it has
            # already been shot at
            else:
                print("Location has already been shot at!")

        # the previous try statement returns a ValueError if the coordinate
        # is invalid
        except ValueError:
            print("Invalid command!")

        # updates sunken ships
        sunken_ships_check(list_of_ships, list_of_sunken_ships, game_board)
        # prints the board
        game_board.printout()

        # if as many Ships have been sunken as there are Ships in the game,
        # the game has been won
        if len(list_of_sunken_ships) == len(list_of_ships):
            won = True

    print("Congratulations! You sank all enemy ships.", end="")


if __name__ == "__main__":
    main()
