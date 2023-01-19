/* Minesweeper GUI
 *
 * desc:
 * A GUI for a minesweeper game. The player can flag, question mark, or open
 * squares on the board. When all squares with mines are flagged, the player
 * wins. The game is lost if a square with a mine is opened.
 *
 * The game can either be started using a seed given in the lineedit next to
 * the start button or a game can be reset so the previous seed will be used.
 *
 * Switching between opening, flagging, and questioning is done by clicking
 * the box on the right side of the text "Click type:"
 *
 * A timer counts the players efficiency at clearing the board. The only
 * function of the time display is to inflate the player's ego.
 *
 * The game board's size can be changed using the spin box on the upper
 * edge of the window.
 *
 * Program author
 * Name:            Leo M
 *
 * Notes about the program and it's implementation:
 * - Board squares are stored in a matrix layout using a vector of vectors
 *   with squares. The data-type is layed out in a manner where the "outer"
 *   vector represents the x-axis and the inner vector represents the y-axis
 * */

#ifndef MAINWINDOW_HH
#define MAINWINDOW_HH

#include <QMainWindow>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QSpinBox>
#include <QTimer>
#include <QLCDNumber>
#include "uisquare.hh"
#include "gameboard.hh"
#include "square.hh"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

const int BUTTON_SIZE = 40;
const int SIDE_BUFFER = 30;
const int TOP_BUFFER = 2*SIDE_BUFFER+BUTTON_SIZE;
const int DEFAULT_BOARD_SIZE = 6;
enum SQUARE_STATES { closed, open, flag, question };

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    // Detect which square was clicked and call logic handling for it
    void handleClicks();

    /* handles gameboard logic and graphic and graphic updates for square with
     * coordinates (x,y)
     * :param 1: x-coordinate of square
     * :param 2: y-coordinate of square
     */
    void handleClickLogic(int x, int y);

    /* Switches square at (x,y)'s flagged state
     * :param 1: x-coordinate of square
     * :param 2: y-coordinate of square
     * :param 3: reference to bool value of previous state
     */
    void toggleFlagged(int x, int y, bool &was_flagged);

    // Block all squares on board
    void blockBoard();

    // these images will be used by uiSquares. Therefore they are stored in
    // public.
    QPixmap flag_img_;
    QPixmap mine_img_;

private:
    Ui::MainWindow *ui;
    std::vector< std::vector <uiSquare*> > square_matrix_;

    // Mode of clicking squares. Options are:
    // 1: open square; 2: flag square; 3: question-mark square
    SQUARE_STATES click_mode_;

    // Reset the board and start a new game acknowledging the given seed
    void startGame();

    // replace old GameBoard object with new one using current_seed_
    // :param1: seed value to initialize board with
    void initializeBoard(int seed);

    // reset timer, board and first_click_ truth value
    void resetBoard();

    // set squares back to their closed state
    void resetSquares();

    // change interaction type (cycle through open-flag-question)
    void changeInteraction();

    // close application
    void quitGame();

    // check if any squares have a question mark
    // :returns: true if at least one square on the board has a "?"-mark
    bool isUncertain();

    // advance timer lcd
    void advanceTimer();

    // open graphic element squares that have were automatically opened on the
    // gameboard object
    void refreshOpenedSquares();

    // inform player about win and stop timer
    void onGameWin();

    // inform player about loss and stop timer
    void onGameLost();

    /* guarantee that the first opened square is totally blank. It or it's
     * adjacent squares don't contain mines, that is.
     * :param1: x-coordinate of square clicked
     * :param2: y-coordinate of square clicked
     */
    void guaranteeSafeOpening(int x, int y);

    // set window size and menu element positions
    void setWindowGeometry();

    // create GUI board squares
    void createBoardSquares();

    // delete GUI board squares
    void deleteBoardSquares();

    // Attributes related to game operation
    GameBoard *game_board_;
    QLineEdit *seed_input_;
    QPushButton *start_game_;
    QPushButton *reset_game_;
    QPushButton *quit_game_;
    QPushButton *choose_interaction_;
    QSpinBox *select_board_size_;
    QLabel *interaction_label_;
    QLabel *win_loss_label_;
    QLabel *select_size_label_;
    QTimer *game_timer_;
    QLCDNumber *time_display_;
    int current_seed_;
    bool first_click_;
};
#endif // MAINWINDOW_HH
