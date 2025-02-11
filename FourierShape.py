import numpy as np
import matplotlib.pyplot as plt


def full_to_short(full):
    return full[::2]


def short_to_full(short):
    """
    Based on: https://stackoverflow.com/a/5347492
    """
    full = np.zeros(2 * len(short), dtype=short.dtype)
    full[0::2] = short
    return full


class FourierShape(object):
    """
    A class to generate a shape based on a set of Fourier descriptors.
    """

    def __init__(self, n_descriptors, descriptor_amp=None, descriptor_phase=None):
        """
        :param n_descriptors: The number of fourier descriptors used to create the shape.
            Increasing this number adds complexity to the shape.
        :param descriptor_amp: amplitude of each fourier descriptor. If not stated, it is randomly determined.
        :param descriptor_phase: phase of each fourier descriptor. If not stated, all phases are set to 0.
        """
        self.n_descriptors = n_descriptors

        if descriptor_phase is None:
            descriptor_phase = np.zeros(n_descriptors)
        elif len(descriptor_phase) != n_descriptors:
            raise ValueError('length of descriptor_phase does not match the number of descriptors')
        self.descriptor_phase = short_to_full(descriptor_phase)

        if descriptor_amp is None:
            descriptor_amp = np.random.uniform(-1, 1, n_descriptors)
        elif len(descriptor_amp) != n_descriptors:
            raise ValueError('length of descriptor_amp does not match the number of descriptors')
        self.descriptor_amp = short_to_full(descriptor_amp)

        self.points = None

    def cumbend(self, t):
        """
        Calculates the next theta angle for the timepoint t.
        """
        freqs = np.arange(len(self.descriptor_amp))
        phases = np.pi * self.descriptor_phase / 180
        theta = -t + np.sum(self.descriptor_amp * np.cos(freqs * t - phases))
        return theta

    def cumbend_to_points(self, n_points=1000):
        """
        Finds equally spaced points of the shape's perimeter, based on the process described by __.
        :param n_points: number of points to find.
        """
        self.points = np.empty((n_points, 2))
        cur_point = np.array([0, 0])
        time_points = np.linspace(0, 2 * np.pi, n_points)

        for i, t in enumerate(time_points):
            self.points[i] = cur_point
            bend_angle = self.cumbend(t)
            following_point = cur_point + [np.cos(bend_angle), np.sin(bend_angle)]
            cur_point = following_point


    def plot_shape(self, color=None, edge_color=None):
        plt.fill_between(*self.points.T, color=color, edgecolor=None)
        if edge_color:
            # using the edgecolor argument in fill_between created an artifact of an horizontal line in the image
            plt.plot(*self.points.T, color=edge_color)
        plt.axis('off')
        plt.gca().set_aspect('equal')

# check = FourierShape(7,[0,0,0,0,0,0,0])
# check.cumbend_to_points()
# check.plot_shape()
# plt.show()

