# Maze Solvers
![](https://travis-ci.com/ntflix/Maze-Solvers.svg?token=nVTpGDRNowJWRQdBiYw2&branch=master)

A program to generate and solve mazes.

## Running – Two Steps:

On a UNIX/Linux system, `cd` to the `Maze Solvers` directory (root of this project) and run
```sh
export PYTHONPATH=`pwd`
```
to set a temporary variable in your shell, which will tell Python where to look for the program's modules. Then, simply:
```sh
python3 modules/ui_processing_link_layer/ui_processing_link_layer.py
```

## Loading a Maze

When running this, you're presented with a 'Load a Maze' window. For now, just hit `Load Maze…`, and select the `simply_connected_maze.db` file. The program will load this preset maze and then you can:
* see the maze view drawn
* press `Solve`, and then the `Play` button (watch your terminal for solver progress!)

## Dependencies

This project requires PyQt6 to be installed. You can install this very easily through Pip with:
```
python3 -m pip install PyQt6
```
PyQt6, however, requires Qt6 to install. You can get this through the Qt Online Installer [here](https://www.qt.io/download-open-source). Make sure to select __Qt 6__ and not _Qt 5_.

Happy mazeing!
