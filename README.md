Based on this GIF:
https://twitter.com/jagarikin/status/1393428373368545283

Some Pygame basics from:
http://pygametutorials.wikidot.com/tutorials-basic

OK so a simple version of this, App1, is to just recursively build all the squares. A downside is that we can only utilize one process, the main process. So we build a better version, App2, which separates calculations, which are the slow part of this application, and use multiple processes to calculate positions, sizes and rotations of all squares. It's done in a similar fashion as App1, with two changes:

1. Run a quick initial recursion with the purpose to split the binary tree into multiple parts (= number of available processes) and send each of these subtrees into the recursion.
1. Store calculations into a pre-allocated array.
1. Drawing the squares is a separate task. This will be made on the main thread when calculations are done.

## Installation

pip install -r requirements.txt

## Run

python app2.py