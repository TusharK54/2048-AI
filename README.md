# 2048 AI
The aim of this project was twofold - first, to replicate as closely as possible the original 2048 game and its mechanics, and second, to build an AI that could play the game and beat it consistently. I wrote everything in Python 3.7 and completed this project in about 2 weeks.


### The AI
<img src="/readme-resources/2048-AI-3x3-grid.gif" width="200">   <img src="/readme-resources/2048-AI-4x4-grid.gif" width="200">   <img src="/readme-resources/2048-AI-5x5-grid.gif" width="200">   <img src="/readme-resources/2048-AI-6x6-grid.gif" width="200">

##### Overview
The AI works by using a slightly modified minimax algorithm (as there is no need for a minimizer) which can be summarazied by a three step process:

1. **Generate all possible future game states** - Every possible game state *n* moves from the current game state is evaluated by computing every possible valid set of *n* moves. These game states are arranged in a tree data structure with the current game state at the root.
2. **Move towards the best future game state** - The best game state in *n* moves is found and the first move to get to that game state is performed. This is done by evaluating the best leaf in the bottom layer of the tree and walking up to find the first move on the path to that leaf.
3. **Recompute additional future game states** - The tree is updated to reflect the move that was just performed and a new layer of leaves is generated to maintain the depth of the tree for the next iteration.

Steps 2 and 3 are repeated until it the search tree can no longer be extended at which point the game is over.

##### Building the Tree
The AI is initialized by building a search tree from the given game state. Each node in the tree contains two primary attributes:

- **board** - the specific arrangement of tiles that makes up the game state represented by the node 
- **move** - the single move that is performed on the parent node's board to produce this node's board

The children of any given node *x* are all the possible nodes with boards that can be reached by performing a single valid move on the board of *x*. Equivalently, the parent *z* of any given node *x* contains the board on which applying the move given by *x* produces the board of *x*.

The search tree is generated until a certain specified *depth* is reached. The depth quantifies how many moves ahead the AI can 'see', so a higher depth corresponds to a smarter AI, but also causes slower performance. For reference, the depth of the AI in the gifs above is 4. From observations, it seems that a search tree with a depth of 4 is usually adequate to beat the game quickly on boards where a 2048 tile is possible (i.e. 4x4 boards and larger).

The image below depicts a search tree with a depth of 3 and the evaluation score of each of the leafs:

<img src="/readme-resources/2048%20Search%20Tree%20(3).jpg">

##### Evaluation Function
Once a search tree has been generated, the AI can iterate over and pick the best future game state among the bottom layer of leaves in the tree. It can then simply walk up the tree until it reaches a node whose parent is the root, and return the move attribute of this node. However, to compare game state, there needs to be some way of quantifying the strength of each board. This is done with an *evaluation function*. 

The goal of an evaluation function is to take any given game state and produce a numerical value that represents its strength. The evaluation function must take into account all the properties that contribute to a good game state, since these are the properties that will be maximized over time. There are three primary properties of each board we want to maximize:

- **score** - the current score of the game, maximized by combining larger tiles
- **largest tile** - the largest tile on the board, maximized by creating a new largest tile
- **clear tiles** - the number of open spaces on the board, maximized by combining multiple tiles

The evaluation function currently used by the AI simply multiplies the above values together:

`evaluation(board) = board.score * board.largest_tile * board.clear_tiles`

##### Updating the Tree
After the AI performs a move in the game, the search tree must be updated with the new game state at its root. The simple solution is to generate a new search tree from the new game state. However, this is an expensive operation, especially for large trees. To save time, we simply change the pointer to the root to the appropraiate child, keep only the leaves in the bottom layer of the tree that can be reached from this new root, and generate their children to maintain the same depth of the tree.
