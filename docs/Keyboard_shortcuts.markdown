# Keyboard shortcuts

Eventually the hotkeys will be editable, but this might not happen until after
1.0 -- unless you want to write that functionality, in which case please get
in touch.

## Quit the program

- Ctrl+Q: Quit the program. Currently will not ask to save unsaved data.
- Ctrl+W: Close the main window, which quits the program. Equivalent to Ctrl+Q.

## File menu: Opening and saving

- Ctrl+O - Open: Open a Scenario, Exercise, or directory
- Ctrl+Shift+S - Save all: Saves all derived data in the Scenario directory or
  its subdirectories.

## Export menu: Exporting images and data

- Ctrl+E - Export the main figure: Export the main figure in any image format
  supported by `matplotlib`.

## Image menu: Choose displayed image

- No current hotkeys

## Navigation menu: Navigate recordings and within recordings

- Up/Down arrow keys (no modifier): Go to previous/next recording.
- Left/Right arrow keys (no modifier): Move cursor to previous/next ultrasound
  frame.

## Other shortcuts:

If you are used to Praat's shortcuts for zooming, these are almost the same.
However, to avoid collisions with shortcuts for for example opening a
directory, these use Alt rather than Control as the modifier key. This will be
an editable feature in the future, probably sometime after release 1.0.

### Zooming

- Alt+I: Zoom in
- Alt+O: Zoom out
- Alt+A: Zoom to the whole recording
- Alt+N: Zoom to selection [To be implemented once interval selection is implemented]

### Panning

- Alt+Left: Pan left by quarter view 
- Alt+Right: Pan right by quarter view
- Alt+C: Center view on selection cursor

