# test_chess.py
import unittest
from Los_Alamos_Chess import * 
from Los_Alamos_Chess import _is_valid_pawn_move
from Los_Alamos_Chess import _is_valid_knight_move
from Los_Alamos_Chess import _is_valid_rook_move
from Los_Alamos_Chess import _is_valid_king_move

class TestChessGame(unittest.TestCase):
    def setUp(self):
        """Initialize a fresh board for each test"""
        self.board = place_pieces(initialize_board())
        self.white = Colour.WHITE
        self.black = Colour.BLACK

    def test_pawn_movement(self):
        """Test valid and invalid pawn moves"""
        # White pawn forward move
        self.assertTrue(_is_valid_pawn_move(self.board, "A2", "A3", self.white))
        # White pawn invalid backward move
        self.assertFalse(_is_valid_pawn_move(self.board, "A2", "A1", self.white))
        # White pawn capture
        self.board["B3"] = Piece(PieceType.PAWN, self.black)
        self.assertTrue(_is_valid_pawn_move(self.board, "A2", "B3", self.white))
        # Black pawn forward move
        self.assertTrue(_is_valid_pawn_move(self.board, "A5", "A4", self.black))

    def test_knight_movement(self):
        """Test knight L-shaped moves"""
        # Valid knight moves
        self.assertTrue(_is_valid_knight_move(self.board, "B1", "A3", self.white))
        self.assertTrue(_is_valid_knight_move(self.board, "B1", "C3", self.white))
        # Invalid knight moves
        self.assertFalse(_is_valid_knight_move(self.board, "B1", "B2", self.white))
        self.assertFalse(_is_valid_knight_move(self.board, "B1", "D2", self.white))

    def test_rook_movement(self):
        """Test rook straight-line movement"""
        # Clear path for rook
        self.board["A3"] = None
        self.assertTrue(_is_valid_rook_move(self.board, "A1", "A4", self.white))
        # Blocked path
        self.assertFalse(_is_valid_rook_move(self.board, "A1", "A6", self.white))
        # Horizontal move
        self.board["B1"] = None
        self.assertTrue(_is_valid_rook_move(self.board, "A1", "D1", self.white))

    def test_king_movement(self):
        """Test king one-square moves"""
        # Valid king moves
        self.board["D2"] = Piece(PieceType.KING, self.white)
        self.assertTrue(_is_valid_king_move(self.board, "D2", "D3", self.white))
        self.assertTrue(_is_valid_king_move(self.board, "D2", "E3", self.white))
        # Invalid king moves
        self.assertFalse(_is_valid_king_move(self.board, "D2", "D4", self.white))
        self.assertFalse(_is_valid_king_move(self.board, "D2", "F4", self.white))

    def test_check_detection(self):
        """Test check detection logic"""
        # Clear some pieces for testing
        self.board["D2"] = None
        self.board["D1"] = Piece(PieceType.KING, self.white)
        self.board["D3"] = Piece(PieceType.QUEEN, self.black)
        self.assertTrue(is_in_check(self.board, self.white))
        # Move king out of check
        new_board = update_board(self.board, ("D1", "E1"))
        self.assertFalse(is_in_check(new_board, self.white))

    def test_checkmate_detection(self):
        """Test checkmate scenarios"""
        # Create a checkmate scenario
        test_board = {f"{col}{row}": None for col in "ABCDEF" for row in range(1, 7)}
        test_board["A1"] = Piece(PieceType.KING, self.white)
        test_board["B2"] = Piece(PieceType.QUEEN, self.black)
        test_board["C1"] = Piece(PieceType.ROOK, self.black)
        self.assertTrue(is_checkmate(test_board, self.white))

    def test_stalemate_detection(self):
        """Test stalemate scenarios"""
        # Create a stalemate scenario
        test_board = {f"{col}{row}": None for col in "ABCDEF" for row in range(1, 7)}
        test_board["A1"] = Piece(PieceType.KING, self.white)
        test_board["B3"] = Piece(PieceType.QUEEN, self.black)
        test_board["C2"] = Piece(PieceType.KING, self.black)
        self.assertTrue(is_stalemate(test_board, self.white))

if __name__ == "__main__":
    unittest.main()