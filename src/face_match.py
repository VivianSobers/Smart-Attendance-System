import cv2
import numpy as np
def image_to_matrix(image_path, size=(64, 64)):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, size)

    return np.array(img, dtype=np.float64)

def matrix_to_vector(matrix):
    return matrix.reshape(-1, 1)

def normalize_vector(vector):
    norm = np.linalg.norm(vector)
    return vector / norm if norm != 0 else vector

def projection_similarity(ref_vec, live_vec):
    ref_unit = ref_vec / np.linalg.norm(ref_vec)
    projection = np.dot(ref_unit.T, live_vec)
    confidence = abs(projection[0][0]) * 100
    return min(confidence, 100)