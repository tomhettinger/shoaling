shoaling
========

## Introduction

`shoaling` A graphical simulation for shoaling fish and their reactions to the environment (walls, fish, predators). Fish move in shoals by moving towards similar fish within a radius of vision, moving away from fish that are too close, and moving the same direction as fish close by.

Click to see demo:
[![yt screenshot](https://raw.githubusercontent.com/tomhettinger/shoaling/master/video/yt_screenshot.png)](http://youtu.be/IZJPUrxL9H0)


## Installation

```sh
$ python setup.py install
```

## Running the application

```sh
$ shoaling
```

## Controls

Forces can be adjusted in real time by using:

`q`/`a` - Fish attraction force +/-

`w`/`s` - Fish anti-crowding force +/-

`e`/`d` - Fish alignment force +/-

`r`/`f` - Wall boundary force +/-

`t`/`g` - Fear of predators force +/-
