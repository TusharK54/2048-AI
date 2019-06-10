# 2048 AI
The aim of this project was twofold - first, to replicate as closely as possible the original 2048 game and its mechanics, and second, to build an AI that could play the game and beat it consistently. Everything was written in Python 3.7. The project was completed in about 2 weeks.


### The AI
<img src="/readme-resources/2048-AI-3x3-grid.gif" width="200">   <img src="/readme-resources/2048-AI-4x4-grid.gif" width="200">   <img src="/readme-resources/2048-AI-5x5-grid.gif" width="200">   <img src="/readme-resources/2048-AI-6x6-grid.gif" width="200">

##### Overview
The AI works by using a slightly modified minimax algorithm. It first evaluates every game state it can be in *n* moves from now by computing every possible valid set of *n* moves. It then chooses the best game state and performs the first respective move on the path to that game state. From this new game state, it repeats the entire process until it runs out of moves at which point the game is over.

##### Building the Tree
The AI is initialized by building a move tree from the current game state. Each node in the tree contains three important attributes:

1. **board** - the game state represented by the node 
2. **move** - the move that when applied to the game state of the parent node produces the game state of this node 
3. **score** - an evaluation score quantifiying how good the game state is 

The children of any given node *x* are all the nodes containing boards that can be reached by performing a single valid move on the board of *x*. Equivalently, the parent *z* of any given node *x* contains the board on which applying the move given by *x* produces the board of *x*.

The move tree is generated until a certain specified *depth* is reached. The depth quantifies how many moves ahead the AI can 'see', so a higher depth corresponds to a smarter AI, but also causes slower performance. The depth of the AIs in the gifs above is 4.

##### Evaluation Function
To pick the next move, the AI iterates over all the leaves in the move tree and picks the one with the highest score attribute. It then walks up the tree until it reaches the node whose parent is the root, and returns the move attribute of this node. The score attribute of each node is calculated when it is initialized by an evaulation function. The goal of this evaluation function is to assign a value that quantifies the strength of each game state. Thus, our evaluation function must take into account all the properties of a good game state since the AI will try to maximize this value, thus maximizing all the properties used in generating the evaluation score. There are three properties of the board we always want to maximize:

1. **score** - the current score of the game, maximized by combining larger tiles
2. **largest tile** - the largest tile on the board, maximized by creating a new largest tile
3. **clear tiles** - the number of open spaces on the board, maximized by combining multiple tiles

Thus, the evaluation function we use is simply `evaluation(board) = board.score * board.largest_tile * board.clear_tiles`

##### Updating the Tree
