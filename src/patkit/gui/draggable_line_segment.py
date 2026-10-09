"""
A line segment for interactively selecting e.g. the kymography sampling line.
"""

from collections.abc import Callable

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
        axes: Axes,
        endpoints: tuple[tuple[float, float], tuple[float, float]]
        | None = None,
        x_start: float | None = None,
        y_start: float | None = None,
        x_end: float | None = None,
        y_end: float | None = None,
        on_changed: Callable[
            [tuple[float, float], tuple[float, float]], None
        ] | None = None,
    ) -> None:
        """
        Parameters
        ----------
        axes : matplotlib.axes.Axes
            The matplotlib axes object to which the line will be added.
        endpoints : tuple[tuple[float, float], tuple[float, float]] | None
            Endpoints ((x1, y1), (x2, y2)) in data coordinates, by default
            None.
        x_start : float | None
            Initial x coordinate of the first endpoint, by default None.
        y_start : float | None
            Initial y coordinate of the first endpoint, by default None.
        x_end : float | None
            Initial x coordinate of the second endpoint, by default None.
        y_end : float | None
            Initial y coordinate of the second endpoint, by default None.
        on_changed : Callable[
            [tuple[float, float], tuple[float, float]], None
        ] | None
            Callback invoked with updated endpoints ((x1, y1), (x2, y2)) when
            the line is dragged, by default None.
        """
        if endpoints is not None:
            (x_s, y_s), (x_e, y_e) = endpoints
        else:
            x_s, y_s, x_e, y_e = x_start, y_start, x_end, y_end

        self.axes = axes
        self.canvas = self.axes.figure.canvas
        self.active_point_index: int | None = None
        self.on_changed = on_changed

        self.line = Line2D(
            xdata=[x_s, x_e],
            ydata=[y_s, y_e],
            marker='o',
            markerfacecolor=None,
            markeredgecolor='lightblue',
            color='lightblue',
            linewidth=1,
            picker=True,
            pickradius=10,
        )
        self.axes.add_line(line=self.line)

        self.cid_press = self.canvas.mpl_connect(
            s='button_press_event',
            func=self.on_press,
        )
        self.cid_release = self.canvas.mpl_connect(
            s='button_release_event',
            func=self.on_release,
        )
        self.cid_motion = self.canvas.mpl_connect(
            s='motion_notify_event',
            func=self.on_motion,
        )

    def on_press(self, event: MouseEvent) -> None:
        """
        Handle mouse button press events to detect endpoint selection.
        """
        if event.inaxes != self.axes:
            return

        xy_data = np.column_stack(
            tup=(self.line.get_xdata(), self.line.get_ydata())
        )
        xy_display = self.axes.transData.transform(values=xy_data)
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
        if event.inaxes != self.axes:
            return

        xdata = list(self.line.get_xdata())
        ydata = list(self.line.get_ydata())

        xdata[self.active_point_index] = event.xdata
        ydata[self.active_point_index] = event.ydata

        self.line.set_data(xdata, ydata)
        if self.on_changed is not None:
            p1 = (float(xdata[0]), float(ydata[0]))
            p2 = (float(xdata[1]), float(ydata[1]))
            self.on_changed(p1, p2)
        self.canvas.draw_idle()

    def on_release(self, event: MouseEvent) -> None:
        """
        Handle mouse button release events to clear active selections.
        """
        self.active_point_index = None

    def get_coordinates(
        self,
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
        return (float(xdata[0]), float(ydata[0])), (
            float(xdata[1]),
            float(ydata[1]),
        )

    def set_endpoints(
        self, endpoints: tuple[tuple[float, float], tuple[float, float]]
    ) -> None:
        """
        Set the line segment endpoints in data coordinates.

        Parameters
        ----------
        endpoints : tuple[tuple[float, float], tuple[float, float]]
            Coordinates ((x1, y1), (x2, y2)).
        """
        (x1, y1), (x2, y2) = endpoints
        self.line.set_data([x1, x2], [y1, y2])
        self.canvas.draw_idle()

    def set_visible(self, visible: bool) -> None:
        """
        Set the line visibility.

        Parameters
        ----------
        visible : bool
            Whether the line should be visible.
        """
        self.line.set_visible(visible)
        self.canvas.draw_idle()

    def get_visible(self) -> bool:
        """
        Get the line visibility state.

        Returns
        -------
        bool
            True if visible, False otherwise.
        """
        return self.line.get_visible()

    def disconnect(self) -> None:
        """
        Disconnect matplotlib event handlers and remove the line from axes.
        """
        self.canvas.mpl_disconnect(cid=self.cid_press)
        self.canvas.mpl_disconnect(cid=self.cid_release)
        self.canvas.mpl_disconnect(cid=self.cid_motion)
        self.line.remove()
        self.canvas.draw_idle()
