# Start game command

A player can take tokens

## Player stock increase when player takes tokens
```
Title : add tokens to player's stock
Given a player with tokens
    0 red, 0 blue, 0 black, 0 white, 0 green, 0 yellow
When player takes these tokens : 
    1 red, 1 blue, 1 black
Then
    player has these tokens
    1 red, 1 blue, 1 black, 0 white, 0 green, 0 yellow

Title : cumulate tokens
Given a player with tokens
    1 red, 1 blue, 0 black, 1 white, 0 green, 0 yellow
When player takes these tokens : 
    1 red, 1 blue, 1 black
Then
    player has these tokens
    2 red, 2 blue, 1 black, 1 white, 0 green, 0 yellow
```

## Stock decrease when player takes tokens
```
Title : decrease stock
Given
    a player
    a stock with tokens
        4 red, 4 blue, 4 black, 4 white, 4 green, 5 yellow
When player takes these tokens : 
    1 red, 1 blue, 1 black
Then
    the stock has these remaining tokens 
        3 red, 3 blue, 3 black, 4 white, 4 green, 5 yellow
```

## Tell when wrong player takes tokens
```
Title : tell when wrong player takes tokens
Given
    a player A
    a player B
    current player is player A
When
    player B takes tokens
Then
    tell that's player B is not current player 
```
