/* a Qt minesweeper GUI
 *
 * Program author
 * Name:            Leo M
 *
 * In-depth info in header
 * */

#include "mainwindow.hh"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , flag_img_(":/flag.png")
    , mine_img_(":/mine.png")
    , ui(new Ui::MainWindow)
    , click_mode_(open)
    , game_board_(new GameBoard(DEFAULT_BOARD_SIZE))
    , current_seed_(0)
    , first_click_(true)
{
    ui->setupUi(this);

    // scale flag and mine images
    flag_img_ = flag_img_.scaled(BUTTON_SIZE, BUTTON_SIZE);
    mine_img_ = mine_img_.scaled(BUTTON_SIZE, BUTTON_SIZE);

    // initialize menu related elements
    seed_input_         = new QLineEdit(this);
    start_game_         = new QPushButton("Start", this);
    reset_game_         = new QPushButton("Reset", this);
    quit_game_          = new QPushButton("Quit", this);
    choose_interaction_ = new QPushButton(" ", this);
    select_board_size_  = new QSpinBox(this);
    interaction_label_  = new QLabel("Click type:", this);
    win_loss_label_     = new QLabel(" ", this);
    select_size_label_  = new QLabel("Board size:", this);
    game_timer_         = new QTimer(this);
    time_display_       = new QLCDNumber(this);

    // colour timer because it's unreadable otherwise
    time_display_->setSegmentStyle(QLCDNumber::Flat);
    QPalette palette = time_display_->palette();
    palette.setColor(palette.WindowText, Qt::blue);
    time_display_->setPalette(palette);

    // set maximum and minimum board sizes
    select_board_size_->setMaximum(50);
    select_board_size_->setMinimum(1);
    select_board_size_->setValue(DEFAULT_BOARD_SIZE);

    // Initialize logic board
    game_board_->init(0);

    // set menu element geometry
    setWindowGeometry();

    // create squares
    createBoardSquares();

    // connect menu related elements
    connect(start_game_, &QPushButton::clicked,
            this, &MainWindow::startGame);
    connect(reset_game_, &QPushButton::clicked,
            this, &MainWindow::resetBoard);
    connect(quit_game_, &QPushButton::clicked,
            this, &MainWindow::quitGame);
    connect(choose_interaction_, &QPushButton::clicked,
            this, &MainWindow::changeInteraction);
    connect(game_timer_, &QTimer::timeout,
            this, &MainWindow::advanceTimer);
    connect(select_board_size_, &QSpinBox::valueChanged,
            this, &MainWindow::resetBoard);
}

MainWindow::~MainWindow()
{
    deleteBoardSquares();

    delete game_board_;
    delete ui;
}

void MainWindow::handleClicks()
{
    for ( int x = 0; x < game_board_->getSize(); ++x )
    {
        for ( int y = 0; y < game_board_->getSize(); ++y )
        {
            if ( square_matrix_.at(x).at(y)->getButton() == sender() )
            {
                handleClickLogic(x, y);

                // only one button can be pressed at a time
                return;
            }
        }
    }
}

void MainWindow::handleClickLogic(int x, int y)
{
    // the board is determined when the first square is opened
    if ( first_click_ and click_mode_ == open )
    {
        guaranteeSafeOpening(x, y);
    }

    // required parameters for determining square actions
    bool is_mine = game_board_->getSquare(x, y).hasMine();
    bool has_flag = game_board_->getSquare(x, y).hasFlag();
    int adjacent_mines = game_board_->getSquare(x, y).getAdjacent();

    switch (click_mode_)
    {
    case open :
        if ( not has_flag )
        {
            game_board_->openSquare(x, y);

            // the game timer starts when the first square is opened
            if ( not game_timer_->isActive() )
            {
                game_timer_->start(1000);
            }

            if ( is_mine )
            {
                onGameLost();

                break;
            }

            // if the user clicked an empty square, update all other squares.
            if ( adjacent_mines == 0 )
            {
                refreshOpenedSquares();
            }
        }
        break;

    case flag :
        // the first click must be an opening
        if ( !first_click_ )
        {
            toggleFlagged(x, y, has_flag);
        }
        break;

    case question :
        // the first click must be an opening
        if ( !first_click_ )
        {
            // on the game-engine level, questions are the same as flags
            toggleFlagged(x, y, has_flag);
        }
        break;

    default :
        // catch-all
        return;
    }

    // handle uiSquare modifications
    square_matrix_.at(x).at(y)->clickedAs(click_mode_,
                                         is_mine,
                                         has_flag,
                                         adjacent_mines);

    // all squares must be flagged but not be "?"-flagged in order to win
    if ( game_board_->isGameOver() and not isUncertain() )
    {
        onGameWin();
    }

    return;
}

void MainWindow::toggleFlagged(int x, int y, bool &was_flagged)
{
    if ( was_flagged )
    {
        Square replacement_square = game_board_->getSquare(x, y);
        replacement_square.removeFlag();

        game_board_->setSquare(replacement_square, x, y);
    } else
    {
        Square replacement_square = game_board_->getSquare(x, y);
        replacement_square.addFlag();

        game_board_->setSquare(replacement_square, x, y);
    }

    // flagged-status has changed
    was_flagged = not was_flagged;
}

void MainWindow::blockBoard()
{
    for ( int x = 0; x < game_board_->getSize(); ++x )
    {
        for ( int y = 0; y < game_board_->getSize(); ++y )
        {
            square_matrix_.at(x).at(y)->blockSquare();
        }
    }
}

void MainWindow::advanceTimer()
{
    time_display_->display(time_display_->intValue() + 1);
}

void MainWindow::refreshOpenedSquares()
{
    for ( int  x = 0; x < game_board_->getSize(); ++x )
    {
        for ( int y = 0; y < game_board_->getSize(); ++y )
        {
            // If a logic square is open, opens the ui square
            if ( game_board_->getSquare(x, y).isOpen() and
                 square_matrix_.at(x).at(y)->getState() == closed )
            {
                int adjacent = game_board_->getSquare(x, y).getAdjacent();
                square_matrix_.at(x).at(y)->clickedAs(open, false,
                                                     false, adjacent);
            }
        }
    }
}

void MainWindow::onGameWin()
{
    blockBoard();
    win_loss_label_->setText("You won!");
    game_timer_->stop();

    // open all squares (squares with mines dismissed by flags)
    for ( int x = 0; x < game_board_->getSize(); ++x )
    {
        for ( int y = 0; y < game_board_->getSize(); ++y )
        {
            int adjacent_mines =
                    game_board_->getSquare(x, y).getAdjacent();

            square_matrix_.at(x).at(y)->clickedAs(open,
                                                  false,
                                                  false,
                                                  adjacent_mines);
        }
    }
}

void MainWindow::onGameLost()
{
    // explode remaining mines
    {
        for ( int  x = 0; x < game_board_->getSize(); ++x )
        {
            for ( int y = 0; y < game_board_->getSize(); ++y )
            {
                if ( game_board_->getSquare(x, y).hasMine() and
                     square_matrix_.at(x).at(y)->getState() == closed )
                {
                    square_matrix_.at(x).at(y)->clickedAs(open, true,
                                                         false, 0);
                }
            }
        }
    }

    blockBoard();
    win_loss_label_->setText("BOOM!");
    game_timer_->stop();
}

void MainWindow::guaranteeSafeOpening(int x, int y)
{
    // flag for next loop
    int adjacent_mines = game_board_->getSquare(x, y).getAdjacent();
    bool is_mine = game_board_->getSquare(x, y).hasMine();
    bool suitable = ( (adjacent_mines == 0) and (not is_mine) );

    // start looking for boards from current_seed_
    int seed = current_seed_;

    while ( not suitable )
    {
        // Cycle seeds until the clicked square is empty. Unfortunately this is
        // a magic number. A random number generator wasn't used for this,
        // because the gameboard has to correlate with the seed to some degree.
        seed += 1000023;

        // re-initialize board
        initializeBoard(seed);

        // update flag variable 'suitable'
        adjacent_mines = game_board_->getSquare(x, y).getAdjacent();
        is_mine = game_board_->getSquare(x, y).hasMine();
        suitable = ( (adjacent_mines == 0) and (not is_mine) );
    }

    // the first click has happened at this point
    first_click_ = false;
}

void MainWindow::setWindowGeometry()
{
    int board_size = game_board_->getSize();

    // place menu related elements and set window geometry
    int y_above_board = SIDE_BUFFER;
    int y_below_board = TOP_BUFFER + board_size*BUTTON_SIZE + SIDE_BUFFER;

    seed_input_->setGeometry(           SIDE_BUFFER,
                                        y_above_board,
                                        3*BUTTON_SIZE,
                                        BUTTON_SIZE);

    start_game_->setGeometry(           SIDE_BUFFER + 3*BUTTON_SIZE,
                                        y_above_board,
                                        2*BUTTON_SIZE,
                                        BUTTON_SIZE);

    reset_game_->setGeometry(           SIDE_BUFFER + 5*BUTTON_SIZE,
                                        y_above_board,
                                        2*BUTTON_SIZE,
                                        BUTTON_SIZE);

    interaction_label_->setGeometry(    SIDE_BUFFER + 3*BUTTON_SIZE,
                                        y_below_board,
                                        3*BUTTON_SIZE,
                                        BUTTON_SIZE);

    choose_interaction_->setGeometry(   SIDE_BUFFER + 6*BUTTON_SIZE,
                                        y_below_board,
                                        BUTTON_SIZE,
                                        BUTTON_SIZE);

    select_board_size_->setGeometry(    SIDE_BUFFER + 11*BUTTON_SIZE,
                                        y_above_board,
                                        2*BUTTON_SIZE,
                                        BUTTON_SIZE);

    quit_game_->setGeometry(            SIDE_BUFFER + 14*BUTTON_SIZE,
                                        y_above_board,
                                        2*BUTTON_SIZE,
                                        BUTTON_SIZE);

    time_display_->setGeometry(         SIDE_BUFFER,
                                        y_below_board,
                                        2*BUTTON_SIZE,
                                        BUTTON_SIZE);

    win_loss_label_->setGeometry(       SIDE_BUFFER + 8*BUTTON_SIZE,
                                        y_below_board,
                                        2*BUTTON_SIZE,
                                        BUTTON_SIZE);

    select_size_label_->setGeometry(    SIDE_BUFFER + 8*BUTTON_SIZE,
                                        y_above_board,
                                        2*BUTTON_SIZE,
                                        BUTTON_SIZE);

    // determine window scaling
    int window_width = 2*SIDE_BUFFER+16*BUTTON_SIZE;
    int window_height = TOP_BUFFER+3*SIDE_BUFFER+board_size*BUTTON_SIZE;

    // window width depends on board size
    if ( board_size > 16 )
    {
        window_width = 2*SIDE_BUFFER+board_size*BUTTON_SIZE;
    }

    this->setGeometry(100,100,window_width,window_height);
}

void MainWindow::createBoardSquares()
{
    int board_size = game_board_->getSize();

    for ( int x = 0; x < board_size; ++x )
    {
        std::vector< uiSquare* > new_column = {};

        for ( int y = 0; y < board_size; ++y )
        {
            uiSquare *new_square = new uiSquare(this, x, y,
                                                TOP_BUFFER, SIDE_BUFFER,
                                                BUTTON_SIZE,
                                                flag_img_,
                                                mine_img_);
            new_column.push_back(new_square);

            connect(new_square->getButton(), &QPushButton::clicked,
                    this, &MainWindow::handleClicks);
        }

        square_matrix_.push_back(new_column);
    }
}

void MainWindow::deleteBoardSquares()
{
    for ( int x = 0; x < game_board_->getSize(); ++x )
    {
        for ( int y = 0; y < game_board_->getSize(); ++y )
        {
            delete square_matrix_.at(x).at(y);
        }
    }

    square_matrix_ = {};
}

void MainWindow::startGame()
{
    // starting the game is basically the same as resetting the board
    // with the exception of also setting a new seed value

    QString seed_qstring = seed_input_->text();
    int seed = seed_qstring.toInt();
    current_seed_ = seed;

    resetBoard();
}

void MainWindow::initializeBoard(int seed)
{
    // delete old board and replace it with a new board
    delete game_board_;
    game_board_ = new GameBoard(select_board_size_->value());
    game_board_->init(seed);
}

void MainWindow::resetBoard()
{
    // delete old squares
    deleteBoardSquares();

    win_loss_label_->setText(" ");

    // when the board is reset, it also needs to be re-initialized
    initializeBoard(current_seed_);

    // create new squares
    createBoardSquares();
    setWindowGeometry();

    // the timer is reset when the game is reset
    game_timer_->stop();
    time_display_->display(0);

    first_click_ = true;
}

void MainWindow::resetSquares()
{
    for ( int x = 0; x < game_board_->getSize(); ++x )
    {
        for ( int y = 0; y < game_board_->getSize(); ++y )
        {
            square_matrix_.at(x).at(y)->resetSquare();
        }
    }
}

void MainWindow::changeInteraction()
{
    click_mode_ = SQUARE_STATES( (click_mode_ + 1) % 4 );
    // squares can't be closed again
    if ( click_mode_ == closed )
        click_mode_ = open;

    if ( click_mode_ == open or click_mode_ == question)
    {
        std::vector< std::string > mark_types = {" ", " ", "P", "?"};
        std::string mark = mark_types.at(click_mode_);
        QString qmark = QString::fromStdString(mark);

        choose_interaction_->setIcon(QIcon());
        choose_interaction_->setText(qmark);
    } else
    {
        choose_interaction_->setText("");
        choose_interaction_->setIcon(flag_img_);
        choose_interaction_->setIconSize(QSize(BUTTON_SIZE-5, BUTTON_SIZE-5));
    }

}

void MainWindow::quitGame()
{
    this->close();
}

bool MainWindow::isUncertain()
{
    for ( int x = 0; x < game_board_->getSize(); ++x )
    {
        for ( int y = 0; y < game_board_->getSize(); ++y )
        {
            if ( square_matrix_.at(x).at(y)->getButton()->text() == "?" )
            {
                return true;
            }
        }
    }

    return  false;
}
