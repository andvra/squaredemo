## Introduction

This repo is inspired by the [following Gif](https://twitter.com/jagarikin/status/1393428373368545283):

![img](./assets/animation.gif)

## Math

The animation is created using these steps:

1. Defining the points for the bottom of the first square, denoted ![img](./assets/p1.svg) and  ![img](./assets/p4.svg), and its side length  ![img](./assets/l.svg)
1. Calculate the top points in the square, denoted  ![img](./assets/p2.svg) and ![img](./assets/p3.svg), using the normal of the line ![img](./assets/p4p1.svg)
1. Calculate ![img](./assets/p5.svg), using the angle ![img](./assets/alpha.svg) and side length ![img](./assets/lcosa.svg)
1. Repeat from step 2, using ![img](./assets/p5p2.svg) and ![img](./assets/p3p5.svg) as base lines, until a minimum side length or maximum recursion depth is reached

<img src="./assets/squares.png" width="400px">

![img](./assets/alpha.svg) is increased at each frame and loops until the application is shut down:

![img](./assets/alpharange.svg) 


## Requirements

python >= 3.7

## Installation

pip install -r requirements.txt

## Run

python app2.py

## Next steps

1. Run a quick initial recursion with the purpose to split the binary tree into multiple parts (= number of available processes) and send each of these subtrees into the recursion.
1. Store calculations into a pre-allocated array.
1. Drawing the squares is a separate task. This will be made on the main thread when calculations are done.

Since the animation is looped, it can of course be made smoother by pre-calculating positions and rotations of all squares before rendering is started.
