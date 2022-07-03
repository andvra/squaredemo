## Introduction

I saw an [animation](https://twitter.com/jagarikin/status/1393428373368545283) and wanted to make something similar. By looking at the animation, it became clear how it works. This algorithm was then implemented using Python3.

## Math

The animation is created by iterating a pretty simple set of rules. We start with defining the points for the bottom of the first square, denoted ![img](./assets/p1.svg) and  ![img](./assets/p4.svg), and its side length  ![img](./assets/l.svg). We then calculate the top points in the square, denoted  ![img](./assets/p2.svg) and  ![img](./assets/p3.svg), by calculating the normal of the line ![img](./assets/p4p1.svg). To build the child squares, we calculate ![img](./assets/p5.svg) using the angle ![img](./assets/alpha.svg), and then recursively calculate the two child squares using ![img](./assets/p5p2.svg) and ![img](./assets/p3p5.svg) as base lines.

<img src="./assets/squares.png" width="400px">

![img](./assets/alpha.svg) is increased at each frame and loops until the application is shut down:

![img](./assets/alpharange.svg) 

## Installation

pip install -r requirements.txt

## Run

python app2.py

## Next step

1. Run a quick initial recursion with the purpose to split the binary tree into multiple parts (= number of available processes) and send each of these subtrees into the recursion.
1. Store calculations into a pre-allocated array.
1. Drawing the squares is a separate task. This will be made on the main thread when calculations are done.

Since the animation is looped, it can of course be made smoother by pre-calculating positions and rotations of all squares before rendering is started.

## Learnings

Some Pygame basics from:
http://pygametutorials.wikidot.com/tutorials-basic