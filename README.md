# JetBrains Evaluation Reset
This tool helps you reset your free evaluation for Jetbrains products

## Tested Products
- PyCharm (2020.x +)
- Webstorm

## Getting Started
To use the program, you can choose one of these options:
- Run with python (version 3)
``` python
python eval_reset.py
```

- Run with .exe file\
Double click, or through the terminal:

```shell
$ eval_reset.exe
```

## Compile The Code
If you want to customize the code - you can edit the source code, and after recompile it
* To compile to .exe file you will need the "pyinstaller" packge\
You can get it with:
```shell
$ python -m pip install pyinstaller
```
* Then, just compile it!.
```shell
$ pyinstaller --onefile --icon=PATH\TO\jetbrains.ico PATH\TO\eval_reset.py 
```