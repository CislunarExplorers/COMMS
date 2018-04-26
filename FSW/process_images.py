"""
vision.py

Includes code for the following tasks:
    1) Given images which show the Earth and Moon, compute pixel locations of these bodies in the images.
    2) Convert pixel locations to body frame unit vectors, pointing from the body frame origin to the Moon/Earth
    3) Return unit vectors as requested

Should be able to perform these tasks on a sample of pre-collected data, or in real-time on the Raspberry Pi





QUESTION: How to do multiple-body detection?
Use ephemerides to calculate approximate expected size of bodies at all points during the mission
 - use these as guesses for the Hough transform (will greatly increase speed)
 - would this work with RANSAC as well?

"""

import numpy as np
import h5py
import cv2
import glob


class CameraParameters(object):
    """
    Class for storing information on camera parameters.
    """

    def __init__(self, focal_length, pixel_size, image_height, image_width):
        self.focal_length = focal_length
        self.pixel_size = pixel_size
        self.image_height = image_height
        self.image_width = image_width

class CameraData(object):
    """
    Class for processing a set of images from a single camera and obtaining radius and centroid information.

    Inputs: Camera parameters object, name of a directory of images.
    Writes an HDF5 file containing the radius and centroid of the Earth, Moon, and Sun at each time step.
    (also needs to receive and store time information somehow)
    Stores values in pixels (2D, in image frame), as well as in meters (3D, in camera frame)
    Uses camera parameters together with distance-from-camera formula to compute camera frame positions.

    """

    def __init__(self, folder_name, camera_params, cv_algorithm):
        # TODO finishing implementing
        self.images = []
        files_list = glob.glob('%s/*.png' % folder_name)
        if len(files_list) == 0:
            raise Exception, 'Invalid image directory name.'
        for filename in files_list:
            cv2.imread(filename, cv2.IMREAD_COLOR)
        self.camera_params = camera_params
        self.write_camera_data()

    def write_camera_data(self):
        """
        Write camera data to an HDF5 file

        :return:
        """
        # TODO Implement this
        pass

    # Need method to read HDF5?
    # Still unclear on how classes tie into saved HDF5 dataset files
    @staticmethod
    def read_camera_data(filename):
        # TODO Implement this
        pass

#
# class VisionACS(object):
#
#     # Make an object for each camera?
#
#     def __init__(self, ):
#         # Read HDF5 file containing satellite information
#         # (Camera location vectors, etc)
#         pass
#         # save body frame position and rotation matricx as attributes
#
#     def request_unit_vector(self, target):
#         """
#         TODO: How should this work? Real-time vs. preprocessed cases
#
#         :param target: Earth or Moon
#         :return: Unit vector to the requested celestial body
#         """
#         pass
#
#     def vector_from_pixels(self, pixel_position):
#         """
#
#         :param pixel_position: a 2x1 numpy array containing an image frame position in pixels.
#         :return: a 3x1 numpy array containing a vector to the same position in the camera frame
#         """
#         pass
#
#         # Pixel position gives x and y in pixels
#         # Compute z distance from camera to target using size equation
#
#         # Then, convert x and y in pixels to x and y in meters in camera frame
#         # Depends on focal length and other camera parameters
#
#     def camera_frame_to_body_frame(self, vec):
#         """
#         Given a vector in the camera frame, return the corresponding vector in the body frame.
#
#         :param vec:
#         :return:
#         """
#         pass
#
#         # Rotate from camera frame to body frame
#         # Then, add camera position vector to camera-to-target vector
