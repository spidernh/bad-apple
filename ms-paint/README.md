# MS Paint

Plays Bad Apple!! in MS Paint using Python.

Uses Pillow to grab a PNG of each frame, renders it to Paint, then saves a screenshot. This doesn't use an MP4 as it takes multiple days to render the full video.

To render the frame, it goes through every eight rows (to lower the resolution and go faster) and separates each row into sections of color (black/white) as it renders them. Between each section it will switch colors if needed.

Due to a quirk in Paint where parts of a canvas won't update if the mouse doesn't pass over them, we also pass the mouse over every part of the canvas after each frame.

[Video]([https://youtu.be/XBVU8bV-pdY)