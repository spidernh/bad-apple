# Microsoft Paint (Vector)

Plays Bad Apple! in Microsoft Paint using Python

Uses OpenCV to read each frame from a frame sequence, converts to grayscale, thresholds, then finds the contours. It then draws the contours, uses a form of the winding number to detect the direction the points on the contour are moving, to know which side of the contour it needs to fill on. It then fills the needed contours and saves a screenshot.

[Video](https://youtu.be/rCpWId-SxW4) (WIP)