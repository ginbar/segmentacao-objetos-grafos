from math import pow
from itertools import product, islice, permutations, combinations
from caracteristicas.superpixel import SuperPixel
from skimage.color import rgb2xyz
import numpy as np 



def extract_chromaticity_moments(image, labels, bkg_mask=None, n_moments=5):
    """
    Extrair momentos de cromaticidade.    
    """

    img_xyz = rgb2xyz(image)
    superpixels = split_superpx(img_xyz, labels) if bkg_mask is None else get_object_superpxs(img_xyz, labels, bkg_mask)
    
    xy_spaces = [rgb_to_xy(pixels) for (_, pixels) in superpixels]
    matrixes = [create_matrixes(xy) for xy in xy_spaces]
    indices = moments_indexes(n_moments)
    moments = np.array([[moments_per_index(matriz, m, l) for m, l in indices] for matriz in matrixes])
        
    return np.array([(label, np.append(mts[:, 0], mts[:, 1])) for (label, _), mts in zip(superpixels, moments)], dtype=object)



def get_object_superpxs(image, labels, bkg_mask, percent=0.4):
    labels = enumerate(np.unique(labels))
    
    px_obj_por_spx = [(label, image[np.logical_and(labels == label, bkg_mask != 0)]) for (_, label) in labels]        
    
    labels = enumerate(np.unique(labels))
    
    superpxs = [(label, image[labels == label]) for (_, label) in labels]
    
    return [spx_obj for (spx, spx_obj) in zip(superpxs, px_obj_por_spx) if (len(spx_obj[1]) / len(spx[1])) > percent]    



def get_no_mask_chromaticity(image, labels, n_moments=5):
    """
    Extrair momentos de cromaticidade.    
    """

    superpixels = split_superpx(rgb2xyz(image), labels)

    xy_space = [rgb_to_xy(pixels) for (_, pixels) in superpixels]
    
    matrizes = [create_matrixes(xy) for xy in xy_space]

    indices = moments_indexes(n_moments)
    
    moments = np.array([[moments_per_index(matriz, m, l) for m, l in indices] for matriz in matrizes])
    
    return np.array([np.append(mts[:, 0], mts[:, 1]) for (label, _), mts in zip(superpixels, moments)]) 

# comentar tempo de processamento 
# usar a mascara de segmentacao


def split_superpx(image, labels):
    labels = enumerate(np.unique(labels))    
    return [(label, image[labels == label]) for (_, label) in labels]



def rgb_to_xy(rgb_values):
    return np.array([xyz_to_xy(rgb) for rgb in rgb_values])    



def xyz_to_xy(xyz):
    X, Y, Z = xyz
    sum_ = X + Y + Z
    if sum_ == 0:
        return (0, 0)
    else:
        return (int((X / sum_) * 100), int((Y / sum_) * 100))



def create_matrixes(xy_values):
    T = np.array([[0 for _ in range(101)] for _ in range(101)], dtype=int)
    for x, y in xy_values:
        T[x, y] += 1
    return T



def moments_per_index(matrix, m, l):
    sum_t, sum_d = 0, 0
    for x in range(100):
        for y in range(100):
            value = matrix[x][y]
            if value > 0:    
                sum_t += pow(x, m) * pow(y, l) * 1
            sum_d += pow(x, m) * pow(y, l) * value
    return sum_t, sum_d



def moments_indexes(n):
    values = range(n // 2 + 1)
    combinations = product(values, repeat=2)
    valid_values = [(x,y) for x, y in combinations if x == 0 or y == 0]    
    return list(islice(valid_values, n))



def porcent_spxs(numerator, denominator):
    len_num, len_den = len(numerator[1]), len(denominator[1]) 
    return 0 if len_den == 0 else numerator / denominator