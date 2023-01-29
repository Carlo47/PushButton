## Debounced Pushbutton ##
Implements a class for debouncing a pushbutton. 

Other implementations distinguish the events **button pressed** and **button released**. In practice, however, **button clicked**, **button clicked twice in quick succession** and **button held long** seem to me to be the most common use cases.

With my solution the user only has to program the methods **onClick()**, **onDoubleClick()** and **onLongClick()** and install them as callbacks of the class DebouncedButton.

### Design decisions:
1. The bouncing of the switch lasts no more than 50 ms (a really bad push button)
2. A double-click event is triggered when the second click is made within 250 ms.
3. A click lasts less than 300 ms otherwise a long-click event is triggered.  