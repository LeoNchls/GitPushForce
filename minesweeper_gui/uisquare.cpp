/* UISquare class for a Qt minesweeper GUI
 *
 * Program author
 * Name:            Leo M
 *
 * In-depth info in header
 * */

#include "uisquare.hh"
#include "mainwindow.hh"

uiSquare::uiSquare(QWidget *parent,
                   int x, int y,
                   int top_pad, int side_pad,
                   int size,
                   const QPixmap &flag_img_,
                   const QPixmap &mine_img_):
    x_(x), y_(y),
    top_pad_(top_pad), side_pad_(side_pad), size_(size),
    state_(closed),
    button_(new QPushButton(parent)),
    label_(new QLabel(parent)),
    flag_img_ref_(flag_img_),
    mine_img_ref_(mine_img_)
{
    QBrush brush(Qt::lightGray);
    QPalette palette;
    palette.setBrush(QPalette::Button, brush);
    button_->setPalette(palette);

    // the square starts off as a blank button
    button_->setGeometry(side_pad_ + size_*x_,
                         top_pad_ + size_*y_,
                         size_, size_);

    // set geometry of label to be identical to button.
    label_->setGeometry(side_pad_ + size_*x_,
                         top_pad_ + size_*y_,
                         size_, size_);

    // until a square is opened, the label is hidden.
    label_->setVisible(false);

    // show the button
    button_->show();
}

uiSquare::~uiSquare()
{
    delete button_;
    delete label_;
}

void uiSquare::clickedAs(int click_mode,
                         bool is_mine,
                         bool has_flag,
                         int adjacent_mines)
{
    // if the square has been opened, clicking it doesn't do anything
    if ( getState() == open )
    {
        return;
    }

    switch(click_mode)
    {
    case open :
        if ( state_ == closed )
        {
            openSquare(is_mine, adjacent_mines);
        }

        break;

    case flag :
        if ( has_flag )
        {
            flagSquare();
        } else
        {
            resetSquare();
        }
        break;

    case question :
        if ( has_flag )
        {
            questionSquare();
        } else
        {
            resetSquare();
        }
        break;

    default :

        // catch-all
        return;
    }
}

void uiSquare::resetSquare()
{
    label_->setVisible(false);
    label_->setText("");
    label_->setPixmap(QPixmap());
    button_->setText("");
    button_->setIcon(QIcon());
    state_ = closed;

    QBrush brush(Qt::lightGray);
    QPalette palette;
    palette.setBrush(QPalette::Button, brush);
    button_->setPalette(palette);
}

void uiSquare::blockSquare()
{
    label_->setVisible(true);
}

const QPushButton *uiSquare::getButton()
{
    return button_;
}

int uiSquare::getState()
{
    return state_;
}

void uiSquare::openSquare(bool is_mine, int adjacent_mines)
{
    // the button gets a new colour when opened
    // but becomes unaccessible due to it's label.
    QBrush brush(Qt::white);
    QPalette palette;
    palette.setBrush(QPalette::Button, brush);
    button_->setPalette(palette);

    blockSquare();

    if ( is_mine )
    {
        button_->setText("");
        button_->setIcon(mine_img_ref_);
        button_->setIconSize(QSize(BUTTON_SIZE-5, BUTTON_SIZE-5));
    } else if ( adjacent_mines != 0 )
    {
        // prepare the number to be placed in the square
        char num_char = '0' + adjacent_mines;
        std::string num_str = "";
        num_str.push_back(num_char);
        QString num_q_str = QString::fromStdString(num_str);

        button_->setText(num_q_str);
    }

    state_ = open;
}

void uiSquare::questionSquare()
{
    button_->setIcon(QIcon());
    button_->setText("?");
    state_ = question;
}

void uiSquare::flagSquare()
{
    button_->setText("");
    button_->setIcon(flag_img_ref_);
    button_->setIconSize(QSize(BUTTON_SIZE-5, BUTTON_SIZE-5));
    state_ = flag;
}


