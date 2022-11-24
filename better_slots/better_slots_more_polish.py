"""

Projekti: Hedelmäpeli parilla pelaajaa suosivalla lisäominaisuudella.

DOKUMENTAATIO:

Pyrin tekemään kehittyneemmän käyttöliittymän, johon sisältyy grid-asettelun
käyttöä sekä graafisten elementtien skaalausta ohjelman parametrien mukaan.

Ohjelmaa tehdessäni keskityin erityisesti siihen, että hedelmäpelin "rullia"
voisi halutessaan lisätä NUMBER_OF_ROLLERS-globaalilla vakiolla. Saavutin tämän
initialize_rollers-metodin (pääikkunaluokassa) toistorakenteella, ja
huomioimalla rullien leveyden widgetien grid-asetteluissa. Myös rullien värejä
voi muuttaa ROLLER_COLOURS-listan värejä muuttamalla, ja "Voittoputkien" arvoja
voi muuttaa WINNING_COLOURS-listan arvoja muuttamalla. Vakiona ohjelmassa
olevat globaalit vakioparametrit ovat ne, jotka koin parhaiksi ohjelman
hauskuuden ja ulkonäön kannalta.

Ohjelma on luonteeltaan peli, jonka kulkua ohjataan melko tarkasti pelin
sisällä alareunalla olevalla dialogi-laatikolla.

StudentId               x
Firstname Lastname      Leo Mandara
Email                   x
"""

from tkinter import *
import random
import time

# The number of rollers in the slot machine
NUMBER_OF_ROLLERS = 5
# Needs 5 colours
ROLLER_COLOURS = ["cyan", "lime", "red", "yellow", "black"]
# a list containing the values of each colours streak. Example:
# ROLLER_COLOURS[0] streak would net the player 10 times their bet.
# Also needs 5 multipliers to work
WINNING_COLOURS = [10, 5, 3, 2, 0]
# all the dialogue in a neat dictionary so that it's not cluttering up the code
DIALOGUE = {
    "GREETING": "Welcome to the most satisfying slot machine experience! \n\n"
                "To begin, set a bet amount in marks (Mk) and then click"
                " \"ROLL\".",
    "SECOND INSTRUCTIONS": "WOW! That's a really {insert_adjective_here}"
                           " roll! \n\nI can't actually see what you rolled."
                           " Anyway, if you're not happy with it you can"
                           " change the outcome by\n pressing the buttons"
                           " underneath the rollers (essentially nudging them"
                           " with your screwdriver). Neat!\n\nYou'll"
                           " need to successfully nudge a roller three times"
                           " without it getting stuck in order to change it's"
                           " colour. \n\nIf a roller gets stuck, you can try"
                           " to bruteforce your bet back out using your"
                           " crowbar. Beware the security guard!",
    "CAUGHT TAMPERING": "VOI KEHVELI\n\n I'm sorry... I mean... oh dear. The"
                        " security guard caught you tampering \nwith the "
                        "machine and charged you a significant sum of money."
                        "\n\nJust move to another machine and try again...",
    "NICELY TAMPERED": "Nice!\n\nYou retrieved your bet from the machine"
                       ". Totally worth the risk!\n\nLet's go again!",
    "AGAIN": "You'd better strike the iron while it's hot. Make more "
             "money!",
    "NO WIN": "Can't win every time... Try again?",
    "LOST": "WOW, you lost all the money you stole off your mom's credit"
            " card AGAIN. \n\nYou lost this game but... at least now you can"
            " join the squid game...\n\nYou can still continue playing with 0"
            " bets if you want to."

}


class Roller:
    """
    This class models a roller in a slot machine. It can be rotated, read,
    and get stuck, in which case it can no longer be rotated.

    "Nudging" the roller is also possible, being an "unofficial" (illegal) way
    to turn the roller.
    """

    def __init__(self):
        self.__roller_panels = []
        self.__stuck = False
        self.__nudged_up = 0
        self.__nudged_down = 0

        # for each of the roller's colours make a panel with that colour
        for panel_number in range(0, 5):

            # finds a random int that's not in roller_panels yet
            next_panel = random.randint(0, 4)
            while next_panel in self.__roller_panels:
                next_panel = random.randint(0, 4)

            # appends the found int to roller_panels
            self.__roller_panels.append(next_panel)

    def nudge(self, direction="DOWN"):
        """For nudging the roller down. Kind of like roll_down, but needs to
        successfully execute three times to work

        :param direction: str, which way to nudge the roller. "DOWN" OR "UP"
        :return:
        """

        # does nothing if the roller is stuck
        if self.is_stuck():
            return

        # random number to determine whether the roller will get stuck
        stuck_rng = random.randint(0, 100)

        # if the random int is less than or equal to 10, the roller gets stuck
        if stuck_rng <= 10:
            self.__stuck = True
            return

        # adds a nudge to the applicable counter and then tries to roll the
        # roller. If the roller is rolled, the nudge counter is set to 0 so
        # that more nudges can be executed
        if direction == "DOWN":
            self.__nudged_down += 1

            if self.__nudged_down > 2:
                self.roll(direction="DOWN")
                self.__nudged_down = 0

        elif direction == "UP":
            self.__nudged_up += 1

            if self.__nudged_up > 2:
                self.roll(direction="UP")
                self.__nudged_up = 0

    def roll(self, direction="DOWN"):
        """Roll the roller up one tick

        :param direction: str, UP or DOWN depending on which way to spin the
        roller. "DOWN" OR "UP"
        :return:
        """

        # if the roller is stuck, returns without doing anything
        if self.is_stuck():
            return

        # makes a list that the new roller position will be stored in
        new_panels = []

        # appends the applicable panels to the new_panels list. Basically
        # shifts all elements in the list one step and loops from last index
        # to first
        if direction == "DOWN":
            for panel in range(0, len(ROLLER_COLOURS)):
                new_panels.append(self.__roller_panels[
                                      abs((panel - 1) % len(ROLLER_COLOURS))])
        elif direction == "UP":
            for panel in range(0, len(ROLLER_COLOURS)):
                new_panels.append(self.__roller_panels[
                                      (panel + 1) % len(ROLLER_COLOURS)])

        self.__roller_panels = new_panels

    def get_panels_state(self):
        """Getter for the position of the roller panels

        :return: list, list of ints that represent each panel on the roller
        from 0 (highest) to 4 (lowest)
        """

        return self.__roller_panels

    def is_stuck(self):
        """Getter for roller's stuck state

        :return: bool, True if roller is stuck
        """

        return self.__stuck


class RootWindow:
    def __init__(self):
        # create a seed out of time for random operations
        random.seed(time.time(), version=2)

        self.__root_window = Tk()

        # Padding for the actual widgets. Only visual.
        for _ in range(0, 5 * NUMBER_OF_ROLLERS + 16):
            self.__square = Label(height=1,
                                  width=2)
            self.__square.grid(column=_,
                               row=0)
        for _ in range(0, 23):
            self.__square = Label(width=3,
                                  height=1)
            self.__square.grid(column=0,
                               row=_)

        # dialogue window at the bottom of the screen
        self.__dialogue_window = Label(text=DIALOGUE["GREETING"],
                                       anchor=CENTER)
        self.__dialogue_window.grid(row=16,
                                    column=2,
                                    rowspan=9,
                                    columnspan=5 * NUMBER_OF_ROLLERS + 11,
                                    sticky=NW+SE)

        # prize column at ride side of screen
        self.prize_column()

        # roller related attributes
        self.__rollers = []
        self.initialize_rollers()

        # bet related attributes
        self.__bet_label = Label(text="Bet: ",
                                 border=2)
        self.__bet_entry = Entry()
        self.__bet_feedback = Label(text="",
                                    fg="red")
        self.__bet_label.grid(row=2,
                              column=4 * NUMBER_OF_ROLLERS + 2,
                              columnspan=2)
        self.__bet_entry.grid(row=2,
                              column=4 * NUMBER_OF_ROLLERS + 4,
                              columnspan=6)
        self.__bet_feedback.grid(row=3,
                                 column=4 * NUMBER_OF_ROLLERS + 4,
                                 columnspan=6)

        # user money related attributes
        self.__user_money = 100
        self.__user_money_field = Label(text=f"Money: {self.__user_money}Mk",
                                        bg="black",
                                        fg="lime")
        self.__user_money_field.grid(row=2,
                                     column=4 * NUMBER_OF_ROLLERS + 11,
                                     columnspan=10,
                                     sticky=W,
                                     ipadx=5)

        # game operation related attributes
        self.__payout_amount = 0
        self.__roll_button = Button(text="ROLL",
                                    border=2,
                                    relief=RAISED,
                                    command=self.game_frame)
        self.__take_button = Button(text="CASH OUT",
                                    border=2,
                                    relief=RAISED,
                                    state=DISABLED,
                                    command=self.cash_out)
        self.__crowbar_button = Button(text="Crowbar",
                                       state=DISABLED,
                                       command=self.break_machine)
        self.__roll_button.grid(row=4,
                                column=4 * NUMBER_OF_ROLLERS + 2,
                                columnspan=8,
                                sticky=NW+SE)
        self.__take_button.grid(row=6,
                                column=4 * NUMBER_OF_ROLLERS + 2,
                                columnspan=8,
                                sticky=NW+SE)
        self.__crowbar_button.grid(row=12,
                                   column=4 * NUMBER_OF_ROLLERS + 2,
                                   rowspan=3,
                                   columnspan=8,
                                   sticky=NW+SE)

        # quit button
        self.__quit_button = Button(text="Quit",
                                    command=self.quit_command,
                                    bg="grey80")
        self.__quit_button.grid(row=14,
                                column=5 * NUMBER_OF_ROLLERS + 13)

        self.__root_window.mainloop()

    def prize_column(self):
        """Puts the winning streaks on the side of the window for the player
        to see. These are static, so I won't worry about making them
        accessible.

        :return:
        """

        # column titles
        self.__streak_column_title = Label(text="Winning streak:",
                                           relief=RIDGE,
                                           border=4)
        self.__prize_column_title = Label(text="Prize:",
                                          relief=RIDGE,
                                          border=4)
        self.__streak_column_title.grid(row=4,
                                        column=NUMBER_OF_ROLLERS * 4 + 11,
                                        columnspan=NUMBER_OF_ROLLERS,
                                        sticky=NW+SE)
        self.__prize_column_title.grid(row=4,
                                       column=NUMBER_OF_ROLLERS * 5 + 11,
                                       columnspan=3,
                                       sticky=NW+SE)

        # a counter for which row the next round of winning colours will be on
        current_row = 5

        for winning_colour in range(0, 5):
            for roller in range(0, NUMBER_OF_ROLLERS):
                self.__win_square = Label(bg=ROLLER_COLOURS[winning_colour],
                                          relief=RAISED,
                                          border=2)
                self.__win_square.grid(row=current_row,
                                       column=NUMBER_OF_ROLLERS * 4+11+roller,
                                       sticky=NW+SE)

            self.__win_text = Label(text=f"{WINNING_COLOURS[winning_colour]}x "
                                         f"Bet",
                                    relief=RIDGE,
                                    border=2)
            self.__win_text.grid(row=current_row,
                                 column=NUMBER_OF_ROLLERS * 5 + 11,
                                 columnspan=3,
                                 sticky=NW+SE)
            current_row += 1

    def initialize_rollers(self):
        """Initializes list of element "rollers"

        :return:
        """

        # initialize the "rollers" of the slot machine and add them to a list
        # for easy access when we need to alter them.
        self.__rollers = []
        for roller_number in range(0, NUMBER_OF_ROLLERS):
            new_roller = self.create_roller(column=(4 * roller_number + 2),
                                            roller_number=roller_number)
            self.__rollers.append(new_roller)
            if 0 <= roller_number < NUMBER_OF_ROLLERS - 1:
                # this goes in between the rollers. It is not initialized in
                # __init__ because it fits in this method better
                self.__in_between = Label(text="=")
                self.__in_between.grid(row=6,
                                       column=(4 * roller_number + 5),
                                       sticky=W+E)

    def create_roller(self, column, roller_number):
        """Makes a new roller visual element including nudge tool

        :param column: int, location column of the roller
        :param roller_number: int, index of the roller in self.__rollers
        :return: list, list with first element being a Roller object and others
        being Tk widgets
        """

        def nudge_up():
            """Local function for updating the roller up. Needs this because
            button commands can't have parameters

            :return:
            """
            self.nudge_roller(roller_number, "UP")

        def nudge_down():
            """Local function for updating the roller down. Needs this because
            button commands can't have parameters

            :return:
            """
            self.nudge_roller(roller_number, "DOWN")

        # make a Roller object for the interface roller object
        roller_object = Roller()

        def create_roller_element(panel_number, border_size, relief_style):
            """Creates a roller panel element

            :param panel_number: int, number of the panel in the Roller
            object
            :param border_size: int, size of the panel border
            :param relief_style: relief style, style of Tk relief
            :return: Tk Label. One panel of the roller
            """

            return Label(bg=ROLLER_COLOURS[
                roller_object.get_panels_state()[panel_number]],
                border=border_size,
                relief=relief_style)

        # initialize all elements related to a single roller.
        roller_element_0 = create_roller_element(0, 2, RIDGE)
        roller_element_1 = create_roller_element(1, 2, RIDGE)
        roller_element_2 = create_roller_element(2, 5, RAISED)
        roller_element_3 = create_roller_element(3, 2, RIDGE)
        roller_element_4 = create_roller_element(4, 2, RIDGE)

        # creates the buttons below each roller
        stuck_text = Label(text="", border=2)
        screwdriver_button_0 = Button(text="^",
                                      command=nudge_up,
                                      background="grey",
                                      state="disabled")
        screwdriver_text = Label(text="Screwdriver")
        screwdriver_button_1 = Button(text="V",
                                      command=nudge_down,
                                      background="grey",
                                      state="disabled")

        # position all elements related to the roller
        roller_element_0.grid(row=2,
                              column=column,
                              rowspan=1,
                              columnspan=3,
                              sticky=NW+SE)
        roller_element_1.grid(row=3,
                              column=column,
                              rowspan=2,
                              columnspan=3,
                              sticky=NW+SE)
        roller_element_2.grid(row=5,
                              column=column,
                              rowspan=3,
                              columnspan=3,
                              sticky=NW+SE)
        roller_element_3.grid(row=8,
                              column=column,
                              rowspan=2,
                              columnspan=3,
                              sticky=NW+SE)
        roller_element_4.grid(row=10,
                              column=column,
                              rowspan=1,
                              columnspan=3,
                              sticky=NW+SE)
        stuck_text.grid(row=11,
                        column=column,
                        rowspan=1,
                        columnspan=3,
                        sticky=W+E)
        screwdriver_button_0.grid(row=12,
                                  column=column,
                                  rowspan=1,
                                  columnspan=3,
                                  sticky=W+E)
        screwdriver_text.grid(row=13,
                              column=column,
                              rowspan=1,
                              columnspan=3,
                              sticky=W+E)
        screwdriver_button_1.grid(row=14,
                                  column=column,
                                  rowspan=1,
                                  columnspan=3,
                                  sticky=W+E)

        # returns all of the elements of the roller for easy access to them
        # later in the program
        return [roller_object, roller_element_0, roller_element_1,
                roller_element_2, roller_element_3, roller_element_4,
                stuck_text, screwdriver_button_0, screwdriver_text,
                screwdriver_button_1]

    def roll_roller(self, roller_number, direction="DOWN"):
        """Rolls the roller one turn in given direction

        :return:
        """

        self.__rollers[roller_number][0].roll(direction)
        self.update_roller(roller_number)

    def roll_all_rollers(self):
        """Makes all rollers spin a random number of times between 7 and 14

        note to self: this method uses the update_idletasks method in Tk. From
        what I understand it makes sure the roller panel graphics (empty text
        widgets) are updated when the program changes their values by it's self

        :return:
        """

        number_of_rollers = len(self.__rollers)
        sleep_time = 0.0033

        # spins all rollers at least 14 times, plus some random times for
        # granularity
        for number_of_rolls in range(0, 14):
            for roller in range(0, number_of_rollers):
                self.roll_roller(roller)
                time.sleep(sleep_time)
                self.__root_window.update_idletasks()

                granular_rolls = random.randint(0, 1)
                for number_of_granular_rolls in range(1, granular_rolls):
                    self.roll_roller(roller)
                    time.sleep(sleep_time)
                    self.__root_window.update_idletasks()

        # also unlocks the screwdriver buttons
        for roller in range(0, number_of_rollers):
            self.__rollers[roller][7].configure(state=NORMAL)
            self.__rollers[roller][9].configure(state=NORMAL)

    def nudge_roller(self, roller_number, direction):
        """Connects the Roller method "nudge" to self.__rollers

        :param roller_number: int, index of roller in self.__rollers
        :param direction: str, direction of nudge. "UP" or "DOWN"
        :return:
        """

        self.__rollers[roller_number][0].nudge(direction)

        if self.__rollers[roller_number][0].is_stuck():
            self.__rollers[roller_number][7].configure(state="disabled",
                                                       text="###",
                                                       background="grey")
            self.__rollers[roller_number][9].configure(state="disabled",
                                                       text="###",
                                                       background="grey")
            # if a roller gets stuck, the crowbar option is unlocked
            self.__crowbar_button.configure(state=NORMAL)

        self.update_roller(roller_number)

    def update_roller(self, roller_number):
        """Updates the roller's graphical elements according to what is in the
        roller's Roller object (index 0)

        :param roller_number: int, index of roller in self.__rollers
        :return:
        """

        # for each panel in the roller, change it's colour to the colour of the
        # panel in the new state of the roller
        for panel in range(0, 5):
            self.__rollers[roller_number][panel + 1].configure(
                background=ROLLER_COLOURS[self.__rollers[roller_number]
                                          [0].get_panels_state()[panel]])

        if self.__rollers[roller_number][0].is_stuck():
            self.__rollers[roller_number][6].configure(
                text="STUCK!", foreground="red")

        # also update the worth of the current streak since the streak changed
        self.__payout_amount = self.determine_streak_worth()

    def check_bet(self):
        """Checks if the bet is valid. Also gives feedback based on truth state

        :return: bool, True if the bet is an int and the user can afford it
        """

        # checks if the bet can be turned into an integer
        try:
            int(self.__bet_entry.get())
        except ValueError:
            self.__bet_feedback.configure(text="Must be int!")
            return False

        # checks if the user can afford the bet
        if int(self.__bet_entry.get()) > self.__user_money:
            self.__bet_feedback.configure(text="Can't afford bet!")
            return False

        # can't steal money from the machine yet ;)
        if int(self.__bet_entry.get()) < 0:
            self.__bet_feedback.configure(text="Bet can't be negative!")
            return False

        # if the method gets to this point, the bet is valid
        self.__bet_feedback.configure(text="")
        return True

    def charge_user(self):
        """Checks if the bet is valid and charges the user according to the bet

        :return:
        :raises: ValueError, if the bet is invalid
        """

        # checks if the bet is valid to start with. If it's not, raises a
        # ValueError
        if not self.check_bet():
            raise ValueError

        # puts the bet amount in a variable, removes it from money and updates
        # money display widget
        bet_amount = int(self.__bet_entry.get())
        self.__user_money -= bet_amount
        self.__user_money_field.configure(text=f"Money: {self.__user_money}Mk")

        # disables bet setting and rolling
        self.__bet_entry.configure(state=DISABLED)
        self.__roll_button.configure(state=DISABLED)

    def determine_streak_worth(self):
        """Determines how much the current streak of colours in the middle row
        is worth considering the bet

        :return: int, worth of streak
        """

        # make a list of all the middle panel values to make handling them
        # easier
        list_of_middle_panels = []
        for roller in range(0, len(self.__rollers)):
            middle_panel = self.__rollers[roller][0].get_panels_state()[2]
            list_of_middle_panels.append(middle_panel)

        # if all panels aren't the same, the streak is worthless
        for middle_panel in list_of_middle_panels:
            if middle_panel != list_of_middle_panels[0]:
                return 0

        # all the panels are the same. Returns the worth of the streak
        bet_entered = int(self.__bet_entry.get())
        return WINNING_COLOURS[list_of_middle_panels[0]] * bet_entered

    def cash_out(self):
        """Adds payout amount to users balance, then sets payout to 0 and
        disables the button

        :return:
        """

        # a bool to determine whether the player actually won anything.
        # used to determine what sort of dialogue is printed at the end.
        nothing_was_won = (self.__payout_amount == 0)

        # add the payout to users balance
        self.__user_money += int(self.__payout_amount)
        self.__user_money_field.configure(text=f"Money: {self.__user_money}Mk")
        self.__user_money_field.update_idletasks()

        # resets payouts
        self.__payout_amount = 0
        self.__take_button.configure(state=DISABLED)

        # at this point the loop is basically done regarding this path.
        # With that, all buttons and rollers should be reset for the next round
        self.initialize_rollers()
        self.__bet_entry.configure(state=NORMAL)
        self.__roll_button.configure(state=NORMAL)
        self.__crowbar_button.configure(state=DISABLED)

        # if the machine wasn't broken, gives some different dialogue
        if nothing_was_won:
            self.__dialogue_window.configure(text=DIALOGUE["NO WIN"])
        else:
            self.__dialogue_window.configure(text=DIALOGUE["AGAIN"])

        # if the user runs out of money, informs the user that they lost
        if self.__user_money == 0:
            self.__dialogue_window.configure(text=DIALOGUE["LOST"])

    def break_machine(self):
        """Gets the player's bet out of the machine at the cost of a slight
        chance of getting caught and losing some money

        :return:
        """

        success_chance = random.randint(0, 100)
        penalty = self.__user_money // 2

        if success_chance < 40:
            self.__user_money -= penalty
            self.__user_money_field.configure(text=f"Money: "
                                                   f"{self.__user_money}Mk")
            self.__payout_amount = 0
            self.cash_out()
            self.__dialogue_window.configure(text=DIALOGUE["CAUGHT TAMPERING"])
            self.__root_window.update_idletasks()

            # if the user also ends up broke, waits a few seconds and displays
            # losing dialogue
            if self.__user_money == 0:
                time.sleep(5)
                self.__dialogue_window.configure(text=DIALOGUE["LOST"])

        else:
            self.__payout_amount = int(self.__bet_entry.get())
            self.cash_out()
            self.__dialogue_window.configure(text=DIALOGUE["NICELY TAMPERED"])

    def game_frame(self):
        """The frame of the game. Calls other functions to make the game work

        :return:
        """

        # charges the user first
        try:
            self.charge_user()
        except ValueError:
            return

        # starts the rollers
        self.roll_all_rollers()

        # enables the cash out option
        self.__take_button.configure(state=NORMAL)

        # updates dialogue
        self.__dialogue_window.configure(text=DIALOGUE["SECOND INSTRUCTIONS"])

    def quit_command(self):
        """Quits the mainloop

        :return:
        """

        self.__root_window.destroy()


def main():
    root_window = RootWindow()


if __name__ == "__main__":
    main()
