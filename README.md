<<<<<<< HEAD
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
=======
# 2048 AI
### Introduction
The aim of this project was twofold - first, to replicate as closely as possible the original 2048 game and its mechanics, and second, to build an AI that could play the game and beat it on its own consistently. I wrote everything in Python 3.7 and completed this project in about 2 weeks.

### The Game
##### Gameplay (from Wikipedia)
2048 is played on a (typically 4x4) grid, with numbered tiles that slide when a player moves them using the four arrow keys. Every turn, a new tile will randomly spawn in an empty spot on the board with a value of either 2 or 4. Tiles slide as far as possible in the chosen direction until they are stopped by either another tile or the edge of the grid. If two tiles of the same number collide while moving, they will merge into a tile with the total value of the two tiles that collided. The resulting tile cannot merge with another tile again in the same move. The user's score starts at zero, and is increased whenever two tiles combine, by the value of the new tile. When the player can no longer make a move, the game is over.

### The AI
<img src="/readme-resources/2048-AI-3x3-grid.gif" width="200">   <img src="/readme-resources/2048-AI-4x4-grid.gif" width="200">   <img src="/readme-resources/2048-AI-5x5-grid.gif" width="200">   <img src="/readme-resources/2048-AI-6x6-grid.gif" width="200">

##### Overview
The AI works by using a slightly modified minimax algorithm (as there is no need for a minimizer) which can be summarazied by a three step process:

1. **Generate all possible future game states** - Every possible game state *n* moves from the current game state is evaluated by computing every possible valid set of *n* moves. These game states are arranged in a tree data structure with the current game state at the root.
2. **Move towards the best future game state** - The best game state in *n* moves is found and the first move to get to that game state is performed. This is done by evaluating the best leaf in the bottom layer of the tree and walking up to find the first move on the path to that leaf.
3. **Recompute additional future game states** - The tree is updated to reflect the move that was just performed and a new layer of leaves is generated to maintain the depth of the tree for the next iteration.

Steps 2 and 3 are repeated until the search tree can no longer be extended at which point the game is over.

##### Building the Tree
The AI is initialized by building a search tree from the given game state. Each node in the tree contains two primary attributes:

- **board** - the specific arrangement of tiles that makes up the game state represented by the node 
- **move** - the single move that is performed on the parent node's board to produce this node's board

The children of any given node *x* are all the possible nodes with boards that can be reached by performing a single valid move on the board of *x*. Equivalently, the parent *z* of any given node *x* contains the board on which applying the move given by *x* produces the board of *x*.

The search tree is generated until a certain specified *depth* is reached. The depth quantifies how many moves ahead the AI can 'see', so a higher depth corresponds to a smarter AI, but also causes slower performance. For reference, the depth of the AI in the gifs above is 4. From observations, it seems that a search tree with a depth of 4 is usually adequate to beat the game quickly on boards where a 2048 tile is possible (i.e. 4x4 boards and larger).

Note that a new tile will randomly spawn in an empty spot on the board after every move. Normally, this would be a significant source of error since the search tree would not accuratly reflect future game states, and this problem would compound exponentially for each additional layer. To address this problem, each node in the search tree inherits the random state of its parent so it can generate its children deterministically and spawn new tiles in the same positions they would spawn in during the game. This way, we can ensure that nodes in the search tree are completley accurate representations of future game states.

The image below depicts a search tree with a depth of 3 and the evaluation score of each of the leafs:

<img src="/readme-resources/2048%20Search%20Tree%20(3).jpg">

##### Evaluation Function
Once a search tree has been generated, the AI can iterate over and pick the best future game state among the bottom layer of leaves in the tree. It can then simply walk up the tree until it reaches a node whose parent is the root, and return the move attribute of this node. However, to compare game states, there needs to be some way of quantifying the strength of each board. This is done with an *evaluation function*. 

The goal of an evaluation function is to take any given game state and produce a numerical value that represents its strength. The evaluation function must take into account all the properties that contribute to a good game state, since these are the properties that will be maximized over time. There are three primary properties of each board we want to maximize:

- **score** - the current score of the game, maximized by combining larger tiles
- **largest tile** - the largest tile on the board, maximized by creating a new largest tile
- **empty tiles** - the number of open spaces on the board, maximized by combining multiple tiles

The evaluation function currently used by the AI simply multiplies the above values together:

`evaluation(board) = board.score * board.largest_tile * board.empty_tiles`

##### Updating the Tree
After the AI performs a move in the game, the search tree must be updated to have the new game state at its root and new layer of leafs generated. The simplest way to do this is to build a new search tree from the new game state. However, this is an expensive operation, especially for large trees. To save time, we first change the pointer of the root from the old game state to the new game state. Then, we find which nodes in the bottom layer of leafs correspond to this *branch* of the search tree, and eliminate the others. Finally, we generate the children of these leafs to maintain the depth of the tree. After some testing, I found that this small optimization speeds up the entire operation by about 25%.

### Future Improvements
While the AI is fully capable of beating the game, there is still much room for improvement. Below are some areas that can be further optimized to enhance the performance of the AI:

##### Evaluation Function
The evaluation function is the driving force of the decision making process of the AI. It is how the AI distinguishes between bad moves, good moves, and great moves. Thus, the AI is really only as good as its evaluation function. The current evaluation function suffices because it forces the AI to maximize certain properties of the board, specifically the score, largest tile, and number of empty tiles. However, we can add weights to these properties to give them different priorities with which the AI maximizes them. We can also add more properties that we want to maximize, or even minimize. For example, we might want to minimize the number of duplicate tiles, which could possibly cause the AI to combine tiles faster and more efficiently. 

Now a really good evaluation function would not just take into account the value of the tiles on the board, but also their position. This could be implemented by multiplying each tile with a distinct weight specified by some *position matrix* that is the same size as the board. For example, a position matrix with a weight of 10 on the edge tiles and a weight of 5 elsewehere would favor keeping the largest tiles on the edges and out of the center - a great 2048 strategy. Another good 2048 strategy is keeping similarly valued tiles close to each other so they are easier to combine once they have the same value. This might be implemented by multiplying all adjacent tiles together, which would favor keeping the largest tiles next to each other.

There really are no limits to the creativity involved in writing an evaluation function. And while an AI with a simple evaluation function can still achieve a very high score, enhancing it is definitely one of the most surefire and fun ways to improve the AI. 

##### Search Tree Pruning
The primary limiting factor preventing the AI from playing a perfect game every game is the depth of its search tree. As of right now, I've found a depth of 4 to be ideal in terms of both speed and performance. A shorter search tree will run much faster but achieve much lower scores, while a longer one will play much better but take much longer to process. The reason for this is because each additional layer is about 4 times larger than the previous layer. Thus the tree grows exponentially, with each layer at a depth of *n* containing roughly 4<sup>*n*</sup> nodes. If we could add layers to the tree without significantly increasing the size of each layer, we would be able to create a better AI that can 'see' more moves ahead without compromising on speed. This is where pruning comes in. 

//TODO: TALK ABOUT PRUNING
>>>>>>> 2b2b311a19d7be516814da5a898598d88e04c292
