# ADCT

This originally started off as a C++ implementation of K-Means clustering, but I decided to extend it myself since I saw it as a good excercise. This is not the most optimized coding, but it displays what I am able to do.

(A) (D)ata (C)lustering (T)ool. This is a python package that is able to execute K-Means clustering and Mean-Shift Clustering. It has no limit on the number of dimensions the data to be clustered is. (Obviously, the more dimenions you the, the less performance you get) Additionally, this script is able to visualize and maintain records of clusterings done.

To install, simply use:
```
pip install ADCT
```

In this repo, there exists 2 folders: <b>Console</b> and </b>Data</b>.
* Console contains the same scripts, but slightly alterred, that utilize the objects ADCT provides to demonstrate how it can be used/implemented
* Data holds the files that Console's scripts uses to save and load data.
  * saved.txt holds the saved data
  * 2D holds plots the Console script can generate

To run the Console sciprt, enter the console folder and run:
```
python Driver.py
```

If you want to load your own custom data, have your data written in similar format:
```
Dim1,Dim2
100,99
66,77
99,76
33,44
54,45
65,67
-50,-40
-20,20
-25,-25
```

Make sure to not have any lines ending in commas.
