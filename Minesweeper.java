import java.awt.*;
import java.awt.event.*;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.border.LineBorder;

import java.util.Timer;
import java.util.TimerTask;

class BoardPiece {

	int value, posx, posy;
	JButton btn;
	Boolean isFlagged = false, isRevealed = false;
	Game G;

	BoardPiece(Game game, JButton btn) { // Each box on the board
		this.G = game; // Reference to the game object
		this.btn = btn; // Reference to Button used as the box
		this.btn.addMouseListener(new MouseAdapter() {
			@Override
			public void mousePressed(MouseEvent e) { // Mouse press is used to listen to right and left clicks
				btn.getModel().setArmed(true);
				btn.getModel().setPressed(true);
			}

			@Override
			public void mouseReleased(MouseEvent e) { // Mouse release should trigger changes
				btn.getModel().setArmed(false);
				btn.getModel().setPressed(false);
				G.startTimer();
				if (e.getButton() == MouseEvent.BUTTON3) flagPiece(); // Right click flags the box
				else if (!isFlagged && e.getButton() == MouseEvent.BUTTON1) game.revealPieces(posx, posy); // Left click reveals the pieces
			}
		});
	}

	void flagPiece() { // Flagging a box
		this.isFlagged ^= true; // Toggle isFlagged
		if (isFlagged) {
			setImageIcon("assets/bombflagged.png"); // Set icon of button to flag
			this.btn.setBackground(new Color(192, 192, 192)); // To match the icon background
			this.G.flags++;
		} else {
			setImageIcon(null); // Remove flag icon for the button
			this.btn.setBackground(new JButton().getBackground()); // Set background of button to default
			this.G.flags--;
		}
        this.G.updateFlagCount(); // Updating flag count displayed on the top
	}

	void revealPiece() { // Revealing a box
		this.isRevealed = true;
		this.disablePiece(); // Disables all the mouse listeners for the button
		this.btn.setBackground(new Color(192, 192, 192)); // Set background to match the icon background
		setBtnValue(Integer.toString(this.value)); // Show the value of the revealed piece
	}

	void setBtnValue(String value) { // Set button value based on the mines count
		if (value.equals("0")) setImageIcon(null); // If surrounding mines count is 0, remove icon from the button
		else {
			if (value.equals("-1")) {
				if (this.isFlagged) setImageIcon("assets/bombflagged.png"); // Set icon to flag if it's a mine and already flagged
				else setImageIcon("assets/bombrevealed.png"); // Set icon to mine if it's a mine and not flagged
			} else {
				if (this.isFlagged) setImageIcon("assets/bombmisflagged.png"); // Set icon to misflagged mine if it's not a mine but flagged as a mine
				else setImageIcon("assets/open" + value + ".png"); // Set icon to the number of mines around the box
			}
		}
	}

	void setImageIcon(String path) { // Sets the icon of the button to the icon with given path
		Icon icon = new ImageIcon(path);
		this.btn.setIcon(icon);
	}

	void disablePiece() { // Remove all the mouse listeners to this button
		for (MouseListener ml: this.btn.getMouseListeners()) {
			this.btn.removeMouseListener(ml);
		}
	}

}

class Game {

	JFrame frame;
	int pixelsx, pixelsy, mineCount, level, flags, time;
	BoardPiece[][] board;
	BoardPiece[] mines;
	JPanel gameScreen, welcomeScreen, gameBoard;
	JLabel flagCount, timerLabel;
	Timer timer;
	Boolean timerStarted = false;

	Game(JFrame frame) { // GAME starts here
		this.frame = frame; // Reference to the main frame
	}

	void startTimer() { // Starts the timer
		if (timerStarted) return; // Starts the timer if only it's not started yet
		timerStarted = true; // Says that timer already started
		this.timer = new Timer(); // New timer instance
		this.timer.schedule(new TimerTask() {
			@Override
			public void run() { // Runs every 1000 milliseconds
				time--;
				updateTimerLabel(); // Updates the remaining time on the top
			}
		}, 0, 1000);
	}

	void stopTimer() { // Stops the timer
		if (this.timer == null) return; // If only the timer exists, the timer is stopped
		this.timer.cancel();
	}

	void showWelcomeScreen() { // Welcome screen to take the level of game from user
		this.frame.setSize(400, 600); // Frame dimensions
		this.frame.setLocationRelativeTo(null); // Center the frame
		this.frame.getContentPane().removeAll(); // Remove previous components (Used when restarting the game)
		this.frame.repaint(); // Repaint the frame

		this.welcomeScreen = new JPanel(new GridBagLayout());
		this.welcomeScreen.setBackground(new Color(192, 192, 192));

		GridBagConstraints c = new GridBagConstraints();
		c.weightx = 1; c.weighty = 1; c.gridheight = 1;
		c.fill = GridBagConstraints.BOTH;

		JPanel header = new JPanel();
		header.setOpaque(false);

		JLabel heading = new JLabel("Minesweeper"); // Set the heading
		heading.setFont(heading.getFont().deriveFont(30.0F));
		heading.setBorder(new EmptyBorder(30, 0, 0, 0));
		header.add(heading);

		c.gridx = 0; c.gridy = 0;
		this.welcomeScreen.add(header, c);

		JPanel body = new JPanel(new GridBagLayout());
		body.setOpaque(false);
		GridBagConstraints x = new GridBagConstraints();
		x.weightx = 1; x.weighty = 1;
		x.fill = GridBagConstraints.NONE;
		JButton btn1 = new JButton("<html><center><span style='font-size: 1.3em'>Beginner</span><br />(7x9 with 10 mines)</center></html>");
		btn1.setBorder(new EmptyBorder(10, 10, 10, 10));
		btn1.setFocusPainted(false);
		btn1.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				startGame(1); // Start game with level 1
			}
		});
		x.gridy = 0;
		body.add(btn1, x);
		JButton btn2 = new JButton("<html><center><span style='font-size: 1.3em'>Intermediate</span><br />(13x18 with 35 mines)</center></html>");
		btn2.setBorder(new EmptyBorder(10, 10, 10, 10));
		btn2.setFocusPainted(false);
		btn2.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				startGame(2); // Start game with level 2
			}
		});
		x.gridy = 1;
		body.add(btn2, x);
		JButton btn3 = new JButton("<html><center><span style='font-size: 1.3em'>Advanced</span><br />(22x25 with 91 mines)</center></html>");
		btn3.setBorder(new EmptyBorder(10, 10, 10, 10));
		btn3.setFocusPainted(false);
		btn3.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				startGame(3); // Start game with level 3
			}
		});
		x.gridy = 2; body.add(btn3, x);

		c.gridx = 0; c.gridy = 1;
		this.welcomeScreen.add(body, c);

		JPanel footer = new JPanel(new BorderLayout());
		footer.setOpaque(false);

		JLabel kk = new JLabel("Minesweeper Game in JAVA", SwingConstants.RIGHT);
		kk.setFont(kk.getFont().deriveFont(12.0F));
		kk.setBorder(new EmptyBorder(0, 0, 2, 10));
		footer.add(kk, BorderLayout.SOUTH);

		c.gridx = 0; c.gridy = 2;
		this.welcomeScreen.add(footer, c);

		this.frame.getContentPane().add(this.welcomeScreen); // Add the welcomscreen panel to the frame
		this.frame.validate();
	}

	void startGame(int level) { // Start game with given level
		this.level = level;
		this.timerStarted = false; // Set timer to "not started yet"
		switch (level) {
			case 1:
				this.time = 60; // 1 Minute for beginners
				showGameScreen(7, 9, 10);
				break;
			case 2:
				this.time = 180; // 3 Minutes for intermediate
				showGameScreen(13, 18, 35);
				break;
			case 3:
				this.time = 600; // 10 Minutes for advanced
				showGameScreen(22, 25, 91);
				break;
			default:
				throw new Error("Invalid level selected!");
		}
	}

	void initBoard(int pixelsx, int pixelsy, int mines) { // Initiate the boxes with given dimensions and random mines

		this.pixelsx = pixelsx; this.pixelsy = pixelsy;
		this.mineCount = mines; this.flags = 0; // Set minecount of the game to track remaining mines to be flagged
		this.board = new BoardPiece[pixelsx][pixelsy]; // Declare board size
		this.mines = new BoardPiece[mines]; // Array to store mines locations

		for (int i = 0; i < pixelsx; i++) {
			for (int j = 0; j < pixelsy; j++) {
				JButton btn = new JButton();
				btn.setPreferredSize(new Dimension(30, 30));
				btn.setFocusPainted(false);
				btn.setBorder(new LineBorder(Color.BLACK));
				this.board[i][j] = new BoardPiece(this, btn); // Place all the boxes on the board
				this.board[i][j].posx = i;
				this.board[i][j].posy = j;
			}
		}

		int tmpx, tmpy;
		for (int x = 0; x<mines; x++) {
			int posx, posy;
			do {
				posx = (int)(Math.random() * pixelsx - 1);
				posy = (int)(Math.random() * pixelsy - 1);
			} while (this.board[posx][posy].value != 0); // Generate random x,y values until they don't match previous mines
			this.mines[x] = this.board[posx][posy]; // Save the box reference to mines list
			this.board[posx][posy].value = -1; // Set the box as mined
			for (int m = -1; m < 2; m++) {
				for (int n = -1; n < 2; n++) {
					tmpx = posx + m; tmpy = posy + n;
					if (
						tmpx < 0 || tmpx >= pixelsx ||
						tmpy < 0 || tmpy >= pixelsy ||
						this.board[tmpx][tmpy].value == -1
					) continue;
					this.board[tmpx][tmpy].value++; // Increment the count in the surrounding boxes of the mines
				}
			}
		}

	}

	void showGameScreen(int pixelsx, int pixelsy, int mines) {
		this.frame.getContentPane().removeAll();
		this.frame.repaint();

		initBoard(pixelsx, pixelsy, mines); // Initiate the game board

		this.gameScreen = new JPanel(new GridBagLayout());
		GridBagConstraints c = new GridBagConstraints();
		c.weightx = 1;
		c.weighty = 1;
		c.fill = GridBagConstraints.BOTH;

		JPanel head = new JPanel(new GridBagLayout());
		JButton restartBtn = new JButton("Restart");
        restartBtn.setFocusPainted(false);
		restartBtn.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				stopTimer(); // Stop the timer when restarted
				showWelcomeScreen(); // Send the user back to homescreen
			}
		});
		c.gridx = 1; c.gridy = 0; head.add(restartBtn, c);

		this.flagCount = new JLabel(); // Count for remaining mines to be flagged
		flagCount.setFont(new Font(null, Font.BOLD, 16));
		flagCount.setHorizontalAlignment(JLabel.CENTER);
		updateFlagCount();
		c.gridx = 0; c.gridy = 0; head.add(flagCount, c);

		this.timerLabel = new JLabel(); // Reverse timer
		timerLabel.setFont(new Font(null, Font.BOLD, 16));
		timerLabel.setHorizontalAlignment(JLabel.CENTER);
		updateTimerLabel();
		c.gridx = 2; c.gridy = 0; head.add(this.timerLabel, c);

		c.gridx = 0; c.gridy = 0; this.gameScreen.add(head, c);
		this.gameBoard = new JPanel(new GridBagLayout());
		this.gameBoard.setBackground(Color.DARK_GRAY);

		GridBagConstraints x = new GridBagConstraints();
		x.weightx = 1; x.weighty = 1; x.fill = GridBagConstraints.NONE;

		for (int i = 0; i<pixelsx; i++) {
			for (int j = 0; j<pixelsy; j++) {
				x.gridx = i; x.gridy = j;
				JButton btn = this.board[i][j].btn;
				this.gameBoard.add(btn, x); // Adding the all the boxes to the game screen
			}
		}
		c.gridx = 0; c.gridy = 1;
		this.gameBoard.setBorder(new EmptyBorder(5, 5, 5, 5));
		this.gameScreen.add(this.gameBoard, c);

		this.frame.getContentPane().add(this.gameScreen);
		this.frame.pack(); this.frame.setLocationRelativeTo(null);
		this.frame.validate();
	}

	void revealPieces(int posx, int posy) { // Reveals the pieces
		expandRevealedPieces(posx, posy); // Reveals the surrounding pieces
		if (this.board[posx][posy].value == -1) { // GAMEOVER
			gameOver(); // Stops the timer and disables all the boxes and reveals the unflagged mines
			this.board[posx][posy].btn.setBackground(new Color(255, 0, 0));
			this.board[posx][posy].setImageIcon("assets/bombdeath.png"); // Set triggered mine to different icon
		}
	}

	void gameOver() { // Called when game is over
		stopTimer();
		for (BoardPiece bp: this.mines) bp.revealPiece(); // Uncover all mines
		for (BoardPiece[] l: this.board) {
			for (BoardPiece x: l) {
				if (x.isFlagged) x.revealPiece();
				x.disablePiece(); // Disable all the buttons
			}
		}
	}

	void expandRevealedPieces(int posx, int posy) { // Revealing surrounding pieces of the clicked box
		this.board[posx][posy].revealPiece(); // Reveale the box that was clicked
		int tmpx, tmpy;
		if (this.board[posx][posy].value == 0) { // If clicked box has no mines in the surroundings
			for (int i = -1; i < 2; i++) {
				for (int j = -1; j < 2; j++) {
					tmpx = posx + i; tmpy = posy + j;
					if ( // Skip if
						tmpx<0 || tmpx >= this.pixelsx || // Out of range (in X)
						tmpy<0 || tmpy >= this.pixelsy || // Out of range (in Y)
						this.board[tmpx][tmpy].isRevealed || // If already revealed
                        this.board[tmpx][tmpy].isFlagged || // If flagged
						this.board[tmpx][tmpy].value == -1 // If it's a mine
					) continue;
					revealPieces(tmpx, tmpy); // Recursively reveal pieces
				}
			}
		}
	}

	void updateFlagCount() { // Update the unflagged mines count
		this.flagCount.setText(String.format("%02d", (this.mineCount - this.flags)));
	}

	void updateTimerLabel() { // Update the timer
		if (this.time == 0) gameOver(); // If time is up, it's gameover
		int minutes = (int) this.time / 60;
		int seconds = this.time % 60;
		this.timerLabel.setText(String.format("%02d:%02d", minutes, seconds));
	}

}

public class Minesweeper {

	public static void main(String args[]) {
		JFrame frame = new JFrame("Minesweeper (Java GUI Application)"); // Title of the application
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setResizable(false); // Set window to be not resizable
		Game game = new Game(frame); // Initiate game class

		game.showWelcomeScreen(); // Show welcome screen with level options

		frame.setVisible(true);
	}

}