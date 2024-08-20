# Trivia Game

## Overview

The Trivia Game project consists of both a server and a client component, designed to facilitate an interactive trivia game. The server handles user authentication, manages game state, and communicates with clients. The client provides the interface for users to interact with the game, including logging in, playing trivia questions, and viewing scores.

## Server

### Description

The server component is responsible for:

- Handling user authentication (login, registration, and logout).
- Managing trivia questions and user scores.
- Distributing questions to clients and validating answers.
- Keeping track of logged-in users and their scores.

### Setup

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd trivia-game
    ```

2. Install required packages (if any):
    ```bash
    pip install -r requirements.txt
    ```

3. Run the server:
    ```bash
    python server.py
    ```

### Configuration

- **Server IP**: 127.0.0.1
- **Server Port**: 5678

### Features

- User login and registration.
- Score tracking and high score leaderboard.
- Question fetching and answer validation.
- Web-based question loading (using `requests` library).

## Client

### Description

The client component allows users to:

- Log in or register an account.
- Play trivia questions and submit answers.
- View their current score and the high score leaderboard.
- See a list of currently logged-in users.

### Setup

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd trivia-game
    ```

2. Install required packages (if any):
    ```bash
    pip install -r requirements.txt
    ```

3. Run the client:
    ```bash
    python client.py
    ```

### Features

- Interactive menu for login, registration, and gameplay.
- Real-time communication with the server for game operations.
- Display of current scores and high scores.

## Protocol

The communication between the client and server follows a custom protocol with specific commands and message formats. Refer to `chatlib_skeleton.py` for detailed protocol definitions and message formats.

## Dependencies

- Python 3.x
- `requests` library (for fetching trivia questions from the web)
- `socket` library (for network communication)

## Usage

1. Start the server in one terminal:
    ```bash
    python server.py
    ```

2. Start one or more clients in separate terminals:
    ```bash
    python client.py
    ```

3. Follow the on-screen instructions to log in, play trivia questions, and interact with the game.
