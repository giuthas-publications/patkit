import numpy as np
from scipy.ndimage import map_coordinates


def extract_kymogram(
    video_array: np.ndarray,
    start_point: tuple[float, float],
    end_point: tuple[float, float],
    num_samples: int | None = None
) -> np.ndarray:
    """
    Sample pixel values along a line across all time frames of a video array.

    Generates coordinates for an oblique line defined by two endpoints and
    extracts the interpolated pixel values for every time step in the 3D array.

    Parameters
    ----------
    video_array : np.ndarray
        A 3D numpy array representing a sequence of grayscale images with
        dimensions in the order of (time, x, y).
    start_point : tuple[float, float]
        The (x, y) coordinates of the starting point of the line.
    end_point : tuple[float, float]
        The (x, y) coordinates of the ending point of the line.
    num_samples : int | None
        The number of points to sample along the line. If None, it defaults to
        the Euclidean distance between the two points to sample roughly every
        pixel.

    Returns
    -------
    np.ndarray
        A 2D numpy array of shape (time, num_samples) containing the
        interpolated pixel values across time.

    Examples
    --------
    >>> import numpy as np
    >>> video = np.random.rand(100, 50, 50)
    >>> kymograph = sample_line_across_time(
    ...     video_array=video,
    ...     start_point=(10.0, 10.0),
    ...     end_point=(40.0, 40.0)
    ... )
    >>> kymograph.shape
    (100, 43)
    """
    t_max, x_max, y_max = video_array.shape
    x_start, y_start = start_point
    x_end, y_end = end_point

    if num_samples is None:
        num_samples = int(np.hypot(x_end - x_start, y_end - y_start))

    x_coords = np.linspace(start=x_start, stop=x_end, num=num_samples)
    y_coords = np.linspace(start=y_start, stop=y_end, num=num_samples)
    t_coords = np.arange(stop=t_max)

    t_grid = t_coords[:, np.newaxis] * np.ones(shape=(1, num_samples))
    x_grid = x_coords[np.newaxis, :] * np.ones(shape=(t_max, 1))
    y_grid = y_coords[np.newaxis, :] * np.ones(shape=(t_max, 1))

    coordinates = np.stack(arrays=(t_grid, x_grid, y_grid), axis=0)

    sampled = map_coordinates(
        input=video_array,
        coordinates=coordinates,
        order=1,
        mode='nearest'
    )

    return sampled
