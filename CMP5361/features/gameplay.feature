# features/gameplay.feature
Feature: Chess Game Rules
  As a chess player
  I want the game to enforce proper rules
  So that the game is fair and follows standard chess conventions

  Scenario: White pawn initial move
    Given a new chess board
    When white moves pawn from A2 to A3
    Then the move should be valid

  Scenario: Black knight capture
    Given a chess board with black knight at B6 and white pawn at C4
    When black moves knight from B6 to C4
    Then the move should be valid
    And the white pawn should be captured

  Scenario: King in check
    Given a chess board with white king at D1 and black queen at D3
    When checking if white is in check
    Then it should return true

  Scenario: Checkmate detection
    Given a chess board with:
      | position | piece  | color |
      | A1       | king   | white |
      | B2       | queen  | black |
      | C1       | rook   | black |
    When checking if white is in checkmate
    Then it should return true