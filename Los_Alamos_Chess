import random
from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass
from enum import Enum

# -----------------------------------
# Data Types and Initial Setup
# -----------------------------------

class Colour(Enum):
    WHITE = "White"
    BLACK = "Black"

class PieceType(Enum):
    KING = "King"
    QUEEN = "Queen"
    ROOK = "Rook"
    KNIGHT = "Knight"
    PAWN = "Pawn"

@dataclass(frozen=True)
class Piece:
    type: PieceType
    colour: Colour

Board = Dict[str, Optional[Piece]]

@dataclass(frozen=True)
class GameState:
    board: Board
    current_player: Colour
    mode: str  # "PvP" or "PvCPU"
    player_names: Dict[Colour, str]
    check: bool = False

# -----------------------------------
# Board Initialization
# -----------------------------------

def initialize_board() -> Board:
    return {f"{col}{row}": None for col in "ABCDEF" for row in range(1, 7)}

def place_pieces(board: Board) -> Board:
    new_board = board.copy()

    # White pieces
    new_board.update({
        "A1": Piece(PieceType.ROOK, Colour.WHITE),
        "B1": Piece(PieceType.KNIGHT, Colour.WHITE),
        "C1": Piece(PieceType.QUEEN, Colour.WHITE),
        "D1": Piece(PieceType.KING, Colour.WHITE),
        "E1": Piece(PieceType.KNIGHT, Colour.WHITE),
        "F1": Piece(PieceType.ROOK, Colour.WHITE),
        **{f"{col}2": Piece(PieceType.PAWN, Colour.WHITE) for col in "ABCDEF"}
    })

    # Black pieces
    new_board.update({
        "A6": Piece(PieceType.ROOK, Colour.BLACK),
        "B6": Piece(PieceType.KNIGHT, Colour.BLACK),
        "C6": Piece(PieceType.QUEEN, Colour.BLACK),
        "D6": Piece(PieceType.KING, Colour.BLACK),
        "E6": Piece(PieceType.KNIGHT, Colour.BLACK),
        "F6": Piece(PieceType.ROOK, Colour.BLACK),
        **{f"{col}5": Piece(PieceType.PAWN, Colour.BLACK) for col in "ABCDEF"}
    })

    return new_board

# -----------------------------------
# Movement Rules
# -----------------------------------

def _is_valid_pawn_move(board: Board, start: str, end: str, colour: Colour) -> bool:
    if board[end] and board[end].colour == colour:
        return False
        
    col_start, row_start = start[0], int(start[1])
    col_end, row_end = end[0], int(end[1])
    direction = 1 if colour == Colour.WHITE else -1
    
    # Standard move
    if col_start == col_end and row_end == row_start + direction:
        return board[end] is None
    # Capture move
    elif abs(ord(col_start) - ord(col_end)) == 1 and row_end == row_start + direction:
        return board[end] is not None and board[end].colour != colour
    return False

def _is_valid_knight_move(board: Board, start: str, end: str, colour: Colour) -> bool:
    if board[end] and board[end].colour == colour:
        return False
        
    x1, y1 = ord(start[0]) - ord('A'), int(start[1]) - 1
    x2, y2 = ord(end[0]) - ord('A'), int(end[1]) - 1
    dx, dy = abs(x1 - x2), abs(y1 - y2)
    return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)

def _is_valid_rook_move(board: Board, start: str, end: str, colour: Colour) -> bool:
    if board[end] and board[end].colour == colour:
        return False
        
    if start[0] != end[0] and start[1] != end[1]:
        return False
        
    squares = _get_squares_between(start, end)
    return all(board[sq] is None for sq in squares)

def _is_valid_bishop_move(board: Board, start: str, end: str, colour: Colour) -> bool:
    if board[end] and board[end].colour == colour:
        return False
        
    x1, y1 = ord(start[0]) - ord('A'), int(start[1]) - 1
    x2, y2 = ord(end[0]) - ord('A'), int(end[1]) - 1
    
    if abs(x1 - x2) != abs(y1 - y2):
        return False
        
    squares = _get_diagonal_squares(start, end)
    return all(board[sq] is None for sq in squares)

def _is_valid_queen_move(board: Board, start: str, end: str, colour: Colour) -> bool:
    if board[end] and board[end].colour == colour:
        return False
        
    if start[0] == end[0] or start[1] == end[1]:
        return _is_valid_rook_move(board, start, end, colour)
    else:
        return _is_valid_bishop_move(board, start, end, colour)

def _is_valid_king_move(board: Board, start: str, end: str, colour: Colour) -> bool:
    if board[end] and board[end].colour == colour:
        return False
        
    x1, y1 = ord(start[0]) - ord('A'), int(start[1]) - 1
    x2, y2 = ord(end[0]) - ord('A'), int(end[1]) - 1
    dx, dy = abs(x1 - x2), abs(y1 - y2)
    return dx <= 1 and dy <= 1

def _get_squares_between(start: str, end: str) -> List[str]:
    squares = []
    
    if start[0] == end[0]:  # Vertical move
        row_start = int(start[1])
        row_end = int(end[1])
        step = 1 if row_end > row_start else -1
        for row in range(row_start + step, row_end, step):
            squares.append(f"{start[0]}{row}")
    elif start[1] == end[1]:  # Horizontal move
        col_start = ord(start[0])
        col_end = ord(end[0])
        step = 1 if col_end > col_start else -1
        for col in range(col_start + step, col_end, step):
            squares.append(f"{chr(col)}{start[1]}")
    
    return squares

def _get_diagonal_squares(start: str, end: str) -> List[str]:
    squares = []
    x1, y1 = ord(start[0]) - ord('A'), int(start[1]) - 1
    x2, y2 = ord(end[0]) - ord('A'), int(end[1]) - 1
    
    x_step = 1 if x2 > x1 else -1
    y_step = 1 if y2 > y1 else -1
    
    x, y = x1 + x_step, y1 + y_step
    while x != x2 and y != y2:
        squares.append(f"{chr(ord('A') + x)}{y + 1}")
        x += x_step
        y += y_step
    
    return squares

def is_valid_move(board: Board, move: Tuple[str, str], colour: Colour) -> bool:
    start, end = move
    piece = board.get(start)
    
    if not piece or piece.colour != colour:
        return False
        
    if piece.type == PieceType.PAWN:
        return _is_valid_pawn_move(board, start, end, colour)
    elif piece.type == PieceType.KNIGHT:
        return _is_valid_knight_move(board, start, end, colour)
    elif piece.type == PieceType.ROOK:
        return _is_valid_rook_move(board, start, end, colour)
    elif piece.type == PieceType.QUEEN:
        return _is_valid_queen_move(board, start, end, colour)
    elif piece.type == PieceType.KING:
        return _is_valid_king_move(board, start, end, colour)
    return False

# -----------------------------------
# Game Logic
# -----------------------------------

def update_board(board: Board, move: Tuple[str, str]) -> Board:
    start, end = move
    return {**board, end: board[start], start: None}

def get_all_valid_moves(board: Board, colour: Colour) -> List[Tuple[str, str]]:
    valid_moves = []
    for start in board:
        piece = board[start]
        if piece and piece.colour == colour:
            for end in board:
                if is_valid_move(board, (start, end), colour):
                    valid_moves.append((start, end))
    return valid_moves

def is_in_check(board: Board, colour: Colour) -> bool:
    king_pos = next(sq for sq, piece in board.items()
                   if piece and piece.type == PieceType.KING and piece.colour == colour)
    
    opponent = Colour.BLACK if colour == Colour.WHITE else Colour.WHITE
    for square, piece in board.items():
        if piece and piece.colour == opponent:
            if is_valid_move(board, (square, king_pos), opponent):
                return True
    return False

def is_checkmate(board: Board, colour: Colour) -> bool:
    if not is_in_check(board, colour):
        return False
    
    # Check if any move can get the king out of check
    for start in board:
        piece = board[start]
        if piece and piece.colour == colour:
            for end in board:
                if is_valid_move(board, (start, end), colour):
                    temp_board = update_board(board, (start, end))
                    if not is_in_check(temp_board, colour):
                        return False
    return True

def is_stalemate(board: Board, colour: Colour) -> bool:
    if is_in_check(board, colour):
        return False
    
    # Check if any legal move exists
    for start in board:
        piece = board[start]
        if piece and piece.colour == colour:
            for end in board:
                if is_valid_move(board, (start, end), colour):
                    temp_board = update_board(board, (start, end))
                    if not is_in_check(temp_board, colour):
                        return False
    return True

def get_random_move(board: Board, colour: Colour) -> Optional[Tuple[str, str]]:
    valid_moves = get_all_valid_moves(board, colour)
    return random.choice(valid_moves) if valid_moves else None

def prompt_move(player: str, board: Board) -> Optional[Tuple[str, str]]:
    try:
        user_input = input(f"{player}, enter move (e.g., 'B2 to B3'): ").upper().strip()
        start, end = user_input.split(" TO ")
        if start in board and end in board:
            return (start, end)
    except ValueError:
        pass
    return None

def get_player_move(state: GameState) -> Tuple[str, str]:
    player_name = state.player_names[state.current_player]
    while True:
        move = prompt_move(player_name, state.board)
        if move and is_valid_move(state.board, move, state.current_player):
            # Verify the move doesn't leave the king in check
            temp_board = update_board(state.board, move)
            if not is_in_check(temp_board, state.current_player):
                return move
            print("Invalid move - would leave your king in check!")
        print("Invalid move. Try again.")

# -----------------------------------
# Game Flow
# -----------------------------------

def print_board(board: Board):
    print("\n  A B C D E F")
    for row in range(6, 0, -1):
        print(row, end=" ")
        for col in "ABCDEF":
            piece = board[f"{col}{row}"]
            symbol = "."
            if piece:
                symbol = {
                    (PieceType.KING, Colour.WHITE): "♔",
                    (PieceType.QUEEN, Colour.WHITE): "♕",
                    (PieceType.ROOK, Colour.WHITE): "♖",
                    (PieceType.KNIGHT, Colour.WHITE): "♘",
                    (PieceType.PAWN, Colour.WHITE): "♙",
                    (PieceType.KING, Colour.BLACK): "♚",
                    (PieceType.QUEEN, Colour.BLACK): "♛",
                    (PieceType.ROOK, Colour.BLACK): "♜",
                    (PieceType.KNIGHT, Colour.BLACK): "♞",
                    (PieceType.PAWN, Colour.BLACK): "♟",
                }.get((piece.type, piece.colour), "?")
            print(symbol, end=" ")
        print()

def play_turn(state: GameState) -> Optional[GameState]:
    print_board(state.board)
    player_name = state.player_names[state.current_player]
    print(f"\n{player_name}'s turn ({state.current_player.value})")
    
    if state.check:
        print(f"{player_name} is in check!")
    
    move = (
        get_player_move(state)
        if state.current_player == Colour.WHITE or state.mode == "PvP"
        else get_random_move(state.board, state.current_player)
    )
    
    if not move:
        if is_stalemate(state.board, state.current_player):
            print("Stalemate! Game ended in a draw.")
            return None
        else:
            print("No valid moves available.")
            return state
    
    new_board = update_board(state.board, move)
    print(f"Move made: {move[0]} to {move[1]}")
    
    opponent = Colour.BLACK if state.current_player == Colour.WHITE else Colour.WHITE
    opponent_in_check = is_in_check(new_board, opponent)
    
    if is_checkmate(new_board, opponent):
        print(f"Checkmate! {player_name} wins!")
        return None
    
    return GameState(
        new_board,
        opponent,
        state.mode,
        state.player_names,
        check=opponent_in_check
    )

def main():
    print("Welcome to Los Alamos Chess!")
    print("---------------------------")
    
    # Game mode selection
    mode = input("Choose mode:\n1. Player vs Player\n2. Player vs CPU\n> ").strip()
    while mode not in ("1", "2"):
        mode = input("Invalid choice. Enter 1 or 2: ").strip()
    mode = "PvP" if mode == "1" else "PvCPU"
    
    # Player names
    player_names = {
        Colour.WHITE: input("Enter White player's name: ").strip() or "White",
        Colour.BLACK: input("Enter Black player's name: ").strip() or "Black" if mode == "PvP" else "CPU"
    }
    
    # Initialize game
    state = GameState(
        board=place_pieces(initialize_board()),
        current_player=Colour.WHITE,
        mode=mode,
        player_names=player_names
    )
    
    # Main game loop
    while state:
        state = play_turn(state)
    
    # Game over
    print("\nGame over! Would you like to play again?")
    if input("Play again? (y/n): ").lower().startswith("y"):
        main()
    else:
        print("Thanks for playing!")

if __name__ == "__main__":
    main()