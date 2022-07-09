# Bad Apple!! player

This repository contains multiple programs I have written to play Bad Apple!! other than just playing it on YouTube.

## Terminal

Plays Bad Apple!! in a terminal using Python.

Uses OpenCV to get the frame from the video, converts that frame into a smaller black & white image that would fit on the terminal, then displays it using either a '#' or a ' ' representing black and white respectively.

[Video](https://youtu.be/dZlLGa9qXyg)

## MS Paint

Plays Bad Apple!! in MS Paint using Python.

Uses Pillow to grab a PNG of each frame, renders it to Paint, then saves a screenshot. This doesn't use an MP4 as it takes multiple days to render the full video.

To render the frame, it goes through every eight rows (to lower the resolution and go faster) and separates each row into sections of color (black/white) as it renders them. Between each section it will switch colors if needed.

Due to a quirk in Paint where parts of a canvas won't update if the mouse doesn't pass over them, we also pass the mouse over every part of the canvas after each frame.

[Video](https://youtu.be/jwjmMSMnKBE) (WIP)

## Minecraft Book

Plays Bad Apple!! in a Minecraft book.

Uses Pillow to read each frame, then goes through the frame and types it into the book using the characters '#' and ' '. It then screenshots and saves it before going to the next page. It will also get new books manually as books have a page cap of 100 pages.

[Video](https://youtu.be/9gVhg2QZRA4)

## Minesweeper

Plays Bad Apple!! in Google Minesweeper.

Uses PyAutoGUI to read the board and figure out where flags are, then keeps track of the state of the board and places flags for black, and keeps the tiles empty for white.

[Video](https://youtu.be/TV_zBIrI8Bg) (WIP, will finish after MS Paint)