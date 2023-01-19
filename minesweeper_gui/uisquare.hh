/* UISquare class for a Qt minesweeper GUI
 *
 * desc:
 * A class that represents squares in a minesweeper board. They can be opened,
 * flagged, or questioned. Flags and question serve basically the same purpose
 * except they are marked differently. The program using these squares decides
 * what to do with the question marks.
 *
 * Squares with flags or question marks can't be opened before first removing
 * the mark.
 *
 * Program author
 * Name:            Leo M
 *
 * Notes about the program and it's implementation:
 * - The squares consist of a QPushButton and a QLabel. The labels are only
 *   only used to block buttons from being pushed at inappropriate times.
 *   The reason this approach was used is that disabling QPushButtons also
 *   greys them out. This could potentially be subverted using stylesheets
 *   but in the scope of this course the label approach was more appropriate
 *   |
 *   └- The labels could be removed and the only drawback would be that the
 *      buttons would change their shade when the cursor is hovering over
 *      them. Functionally the labels serve no purpose.
 * */

#ifndef UISQUARE_HH
#define UISQUARE_HH

#include <QWidget>
#include <QPushButton>
#include <QLabel>
#include <QPixmap>

class uiSquare
{
public:
    uiSquare(QWidget* parent,
             int x, int y,
             int top_pad, int side_pad,
             int size,
             const QPixmap &flag_img_,
             const QPixmap &mine_img_);

    ~uiSquare();

    /* :param1: defines what the square's new state is supposed to be
     * 0: closed; 1:open; 2: flag; 3: question (see SQUARE_STATE in MainWindow)
     * :param2: true if the square contains a mine, else false
     * :param3: true if the square is flagged, else false
     * :param4: number of adjacent mines to the square
     */
    void clickedAs(int click_mode, bool is_mine,
                   bool has_flag, int adjacent_mines);

    // open square and reset it's text and icon
    void resetSquare();

    // set label in front of square to make it unaccessible. Buttons aren't
    // just disabled to avoid greying them out
    void blockSquare();

    // get X-coordinate of square
    // :returns: x-coordinate
    int getX();

    // get Y-coordinate of square
    // :returns: y-coordinate
    int getY();

    // get constant pointer to square's button
    // :returns: constant pointer to square's button
    const QPushButton *getButton();

    // get state the square is in
    // :returns: int, according to SQUARE_STATE enum in MainWindow
    int getState();

private:
    // squares know their location and size
    int x_;
    int y_;
    int top_pad_;
    int side_pad_;
    int size_;

    // squares also know their state
    int state_;

    /* Opens a square, i.e. shows what lies within it. Also blocks it from
     * future clicks
     * :param1: true if square contains a mine, else false
     * :param2: number of adjacent mines to square
     */
    void openSquare(bool is_mine, int adjacent_mines);

    // set a question mark on the square
    void questionSquare();

    // set a flag on the square
    void flagSquare();

    // graphical elements of square
    QPushButton *button_;
    QLabel *label_;
    const QPixmap &flag_img_ref_;
    const QPixmap &mine_img_ref_;
};

#endif // UISQUARE_HH
