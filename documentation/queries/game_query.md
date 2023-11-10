# Game query

User want to see game state

## Rules - Display game not started
```
Title : Display game not started (Done)

Given
    a game is not started
When
    user query game state
Then
    suggest to user to start a game 
```

## Rules - Display cards
```
Title : Display cards (TODO)

Given
    a game is started
        with level 1 cards : A, B, C, D
        with level 2 cards : E, F, G, H
        with level 3 cards : I, J, K, L
When
    player query game state
Then
    game state is :
        with level 1 cards : A, B, C, D
        with level 2 cards : E, F, G, H
        with level 3 cards : I, J, K, L        
```

## Rules - Display player's hand
```
Title : Display player's hand (TODO)

Given
    a game is started
    and player A has cards :
        - card A
        - card B
When
    player A query game state
Then
    game state is :
        player A with cards :
            - card A
            - card B
```

## Rules - Hide opponent's hand
```
Title : Hide opponent's hand (TODO)

Given
    a game is started
    and player A is current player
    and player B has cards :
        - card A
        - card B
When
    player A query game state
Then
    game state is :
        player B with cards :
            - hidden card
            - hidden card
```

## Rules - Display game tokens
```
Title : Display game tokens (TODO)

Given
    a game is started
    and stock has :
        3 red tokens
        2 black tokens
        2 white tokens
        4 blue tokens
        1 green token
        0 yellow token
When
    player A query game state
Then
    game state is :
        stock  :
            3 red tokens
            2 black tokens
            2 white tokens
            4 blue tokens
            1 green token
            0 yellow token
```

## Rules - Display player tokens
```
Title : Display player tokens (TODO)

Given
    a game is started
    and a player A has stock :
        1 red tokens
        1 black tokens
        2 white tokens
        2 blue tokens
        1 green token
        1 yellow token
    and a player B has stock :
        2 red tokens
        1 black tokens
        1 white tokens
        0 blue tokens
        2 green token
        1 yellow token
When
    player A query game state
Then
    game state is :
        player A with stock :
            1 red tokens
            1 black tokens
            2 white tokens
            2 blue tokens
            1 green token
            1 yellow token
        and player B with stock :
            2 red tokens
            1 black tokens
            1 white tokens
            0 blue tokens
            2 green token
            1 yellow token
```
