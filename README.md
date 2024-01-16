# Project-VAFM

Project VAFM
Virtual Augmentation by Fiducial Markers

Nithish Murugavenkatesh



PSBB Millennium School OMR

Overview

Project VAFM is a real time artificial reality application that finds a specific ARUCO marker in live feed, takes a source video, warps its perspective to overlay the marker, and performs the augmentation.

Structure of the Project

The entire project is written in Python.in a OOP programming structure for enhanced reusability of the code.

Theory

Homography( Perspective Transform)

Homography is an image geometry technique where 2 planar images are made to overlay based on one image’s  perspective. 

One image is rectangular or square in nature. Rectangles and squares can form any arbitrary quadrilateral by the tweaking of its angles.

This method assumes both images share the same camera center

In the given equation, P’ is the new perspective created by P(Old Perspective) into the 3x3 matrix H


ArUCo Method (Opencv)

ArUCo stands for Augmented Reality University of Cordoba

They are Binary fiducial markers, which are detected by feature detection, mitigating camera warping, and rectifying  perspective to look like a planar square.

Each marker is identified by the unique binary pattern on the marker.


For example, the QR codes are a type of fiducial markers, though not ArUCo.


MVP - Minimum Viable Product

