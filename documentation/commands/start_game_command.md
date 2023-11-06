# Start game command

A game should start 

## Rules : Prepare some game elements at start (DONE)
```
Title : Should draw cards
Given
    any players
When
    a game start
Then
    5 gold tokens are in reserve
    4 cards level 1 are revealed
    4 cards level 2 are revealed
    4 cards level 3 are revealed
```

## Rules : Some elements depends on number of player (TODO)  
```
Title : Specific preparation for two players (DONE)
Given
    2 players
When
    a game start
Then
    2 players are ready to play
    4 tokens are in the stock
    3 nobles are in the board

Title : Specific preparation for three players (DONE)
Given
    3 players
When
    a game start
Then
    3 players are ready to play
    5 tokens are in the stock
    4 nobles are in the board

Title : Specific preparation for four players (TODO)
Given
    4 players
When
    a game start
Then
    4 players are ready to play
    7 tokens are in the stock
    4 nobles are in the board
```

