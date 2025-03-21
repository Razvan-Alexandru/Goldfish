# Goldfish

AI Course project for a 5x5 chess game. Currently supports Human vs Human. 

# Quick start

The game is contained in `MiniChess.py`. Simply run it on the command line.
Ex: `MiniChess.py 25 13 1 H-AI e0`

```console
$ python MiniChess.py <time_limit> <max_turns> <use_alpha_beta> <play_mode> <heuristic>
```
<use_alpha_beta> 0: no, 1: yes

<play_mode> H-H, H-AI, AI-H, AI-AI, first one is white, the second is black

\<heuristic> e0, e1 or e2



Write your move in algebraic notation. For example: `e1 e2`.

```console
Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.

5   bK  bQ  bB  bN   .
4    .   .  bp  bp   .
3    .   .   .   .   .
2    .  wp  wp   .   .
1    .  wN  wB  wQ  wK

     A   B   C   D   E

Turn #1
White to move:
```

Outputs are written in `output.txt` under the same directory.
