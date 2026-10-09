"""
A line segment for interactively selecting e.g. the kymography sampling line.
"""

import numpy as np
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from matplotlib.lines import Line2D


class DraggableLineSegment:
    """
    An interactive matplotlib line allowing users to drag both endpoints.

    Binds mouse events of a matplotlib Axes to allow the user to move the start
    and end points of a line segment.
    """

    def __init__(
        self,
        ax: Axes,
        x_start: float,
        y_start: float,
        x_end: float,
        y_end: float
    ) -> None:
        """
        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The matplotlib axes object to which the line will be added.
        x_start : float
            Initial x coordinate of the first endpoint.
        y_start : float
            Initial y coordinate of the first endpoint.
        x_end : float
            Initial x coordinate of the second endpoint.
        y_end : float
            Initial y coordinate of the second endpoint.
        """
        self.ax = ax
        self.canvas = self.ax.figure.canvas
        self.active_point_index: int | None = None

        self.line = Line2D(
            xdata=[x_start, x_end],
            ydata=[y_start, y_end],
            marker='o',
            color='red',
            linewidth=2,
            picker=True,
            pickradius=10
        )
        self.ax.add_line(line=self.line)

        self.cid_press = self.canvas.mpl_connect(
            s='button_press_event',
            func=self.on_press
        )
        self.cid_release = self.canvas.mpl_connect(
            s='button_release_event',
            func=self.on_release
        )
        self.cid_motion = self.canvas.mpl_connect(
            s='motion_notify_event',
            func=self.on_motion
        )

    def on_press(self, event: MouseEvent) -> None:
        """
        Handle mouse button press events to detect endpoint selection.
        """
        if event.inaxes != self.ax:
            return

        xy_data = np.column_stack(
            tup=(self.line.get_xdata(), self.line.get_ydata())
        )
        xy_display = self.ax.transData.transform(values=xy_data)
        event_xy = np.array(object=[event.x, event.y])

        distances = np.linalg.norm(x=xy_display - event_xy, axis=1)

        if np.min(a=distances) < 15.0:
            self.active_point_index = int(np.argmin(a=distances))

    def on_motion(self, event: MouseEvent) -> None:
        """
        Handle mouse motion events to drag the selected endpoint.
        """
        if self.active_point_index is None:
            return
        if event.inaxes != self.ax:
            return

        xdata = list(self.line.get_xdata())
        ydata = list(self.line.get_ydata())

        xdata[self.active_point_index] = event.xdata
        ydata[self.active_point_index] = event.ydata

        self.line.set_data(x=xdata, y=ydata)
        self.canvas.draw_idle()

    def on_release(self, event: MouseEvent) -> None:
        """
        Handle mouse button release events to clear active selections.
        """
        self.active_point_index = None

    def get_coordinates(
        self
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        """
        Retrieve the current coordinates of the line endpoints.

        Returns
        -------
        tuple[tuple[float, float], tuple[float, float]]
            A tuple containing ((x_start, y_start), (x_end, y_end)).
        """
        xdata = self.line.get_xdata()
        ydata = self.line.get_ydata()
        return (xdata[0], ydata[0]), (xdata[1], ydata[1])

    def disconnect(self) -> None:
        """
        Disconnect matplotlib event handlers and remove the line from axes.
        """
        self.canvas.mpl_disconnect(cid=self.cid_press)
        self.canvas.mpl_disconnect(cid=self.cid_release)
        self.canvas.mpl_disconnect(cid=self.cid_motion)
        self.line.remove()
        self.canvas.draw_idle()
