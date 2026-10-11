import pydicom
import matplotlib.pyplot as plt
import numpy as np
import time


# width and height of the initial point in the flood fill
width = 256
height = 300
window_size = 10
cond_vertical_param = 10
threshold = (1000, 1110)
threshold_hemorrhage = (1070, 1110)
threshold_cond_average = 1065
window_size_cond_average = 4
hemorrhage_cleaning_parameter = 40

is_3d = True
first_image_index, last_image_index = 0, 40

directory_input = 'scans/abnormal2/'
charactar = 'FILE'
directory_output_brain = 'outputs/output'
directory_output_hemorrhage = 'outputs_hemorrhage/output_hemorrhage'

def open_dicoms(image_number):
    file_path = directory_input + charactar + '0.dcm'
    dicom_data = pydicom.dcmread(file_path)
    dicoms_pixel_array = np.empty((last_image_index - first_image_index, dicom_data.Rows, dicom_data.Columns), dtype=np.int16)
    for i in range(first_image_index, last_image_index):
        file_name = charactar + str(i) + '.dcm'
        file_path = directory_input + file_name
        dicom_data = pydicom.dcmread(file_path)
        dicoms_pixel_array[i-first_image_index] = dicom_data.pixel_array

    return dicoms_pixel_array, dicom_data


def save_dicom(dicom_data, pixel_array, number, directory):
    file_name = charactar + str(number) + '.dcm'
    dicom_data = pydicom.dcmread(directory_input + file_name)
    for i in range(len(pixel_array)):
        for j in range(len(pixel_array[0])):
            if pixel_array[i][j] < 0:
                pixel_array[i][j] = 0
    
    dicom_data.PixelData = pixel_array.tobytes()
    pydicom.dcmwrite(filename=(directory + str(number) + '.dcm'), dataset=dicom_data)
    

def cond(pixel_array, i, j, window_size, threshold):
    # TODO: if window_size moves pointer to out of image it should throw exception
    if (((pixel_array[i - window_size][j - window_size] > threshold[0] and pixel_array[i - window_size][j - window_size] < threshold[1])
    or (pixel_array[i + window_size][j + window_size] > threshold[0] and pixel_array[i + window_size][j + window_size] < threshold[1]))
    and ((pixel_array[i + window_size][j - window_size] > threshold[0] and pixel_array[i + window_size][j - window_size] < threshold[1])
    or (pixel_array[i - window_size][j + window_size] > threshold[0] and pixel_array[i - window_size][j + window_size] < threshold[1]))
    ):
        return True
    else:
        return False


def flood_fill_bfs(pixel_array):
    """
    Args:
        pixel_array (2D array): the 2D array of image including Hounsfield units WITHOUT skull stripping
    Return:
        result (2D array): the 2D array of image including Hounsfield units WITH skull stripping
    """
    unpainted = [(height, width)]
    
    result = np.full((512, 512), -2000, dtype=np.int16)
    while unpainted:
        # painting
        if pixel_array[unpainted[0][0]][unpainted[0][1]] < threshold[1]:
            result[unpainted[0][0]][unpainted[0][1]] = pixel_array[unpainted[0][0]][unpainted[0][1]]
        # add neighbours to unpainted list
        for i in range(unpainted[0][0] - 1, unpainted[0][0] + 2):
            for j in range(unpainted[0][1] - 1, unpainted[0][1] + 2):
                if result[i][j] == -2000 and pixel_array[i][j] < threshold[1] and pixel_array[i][j] > threshold[0] and (i, j) not in unpainted and cond(pixel_array, i, j, window_size, threshold):
                    unpainted.append((i, j))
        unpainted.pop(0)
        
    return result


def cond_vertical(candidate_frame, current_pixel, pixel_arrays):
    i = current_pixel[0]
    j = current_pixel[1]
    k = current_pixel[2]
    if not (pixel_arrays[i][j][k + cond_vertical_param] > threshold[0] and pixel_arrays[i][j][k + cond_vertical_param] < threshold[1] \
        and pixel_arrays[candidate_frame][j][k + cond_vertical_param] > threshold[0] and pixel_arrays[candidate_frame][j][k + cond_vertical_param] < threshold[1]):
            return False
    if not (pixel_arrays[i][j][k - cond_vertical_param] > threshold[0] and pixel_arrays[i][j][k - cond_vertical_param] < threshold[1] \
        and pixel_arrays[candidate_frame][j][k - cond_vertical_param] > threshold[0] and pixel_arrays[candidate_frame][j][k - cond_vertical_param] < threshold[1]):
            return False
    if not (pixel_arrays[i][j + cond_vertical_param][k] > threshold[0] and pixel_arrays[i][j + cond_vertical_param][k] < threshold[1] \
        and pixel_arrays[candidate_frame][j + cond_vertical_param][k] > threshold[0] and pixel_arrays[candidate_frame][j + cond_vertical_param][k] < threshold[1]):
            return False
    if not (pixel_arrays[i][j - cond_vertical_param][k] > threshold[0] and pixel_arrays[i][j - cond_vertical_param][k] < threshold[1] \
        and pixel_arrays[candidate_frame][j - cond_vertical_param][k] > threshold[0] and pixel_arrays[candidate_frame][j - cond_vertical_param][k] < threshold[1]):
            return False
    return True


def flood_fill_bfs_3d(pixel_arrays):
    """
    Args:
        pixel_arrays (3D array): the 3D array of image including Hounsfield units WITHOUT skull stripping
    Return:
        result (3D array): the 3D array of image including Hounsfield units WITH skull stripping
    """
    counter = 0
    depth = int(len(pixel_arrays) / 2 + 1)
    unpainted = [(depth ,height, width)]
    for i in range(len(pixel_arrays)):
        print(pixel_arrays[i][height][width])
    result = np.full((len(pixel_arrays), 512, 512), 0, dtype=np.int16)

    while unpainted:
        # painting
        result[unpainted[0][0]][unpainted[0][1]][unpainted[0][2]] = pixel_arrays[unpainted[0][0]][unpainted[0][1]][unpainted[0][2]]
        for i in range(unpainted[0][0] - 1, unpainted[0][0] + 2):
            if (i < 0 or i > last_image_index - first_image_index - 1 or not cond_vertical(i, unpainted[0], pixel_arrays)): # first condition is for short circuit
                continue
            for j in range(unpainted[0][1] - 1, unpainted[0][1] + 2):
                for k in range(unpainted[0][2] - 1, unpainted[0][2] + 2):
                    if i < 0:
                        print(i)
                    counter += 1
                    if result[i][j][k] == 0 and pixel_arrays[i][j][k] < threshold[1] and pixel_arrays[i][j][k] > threshold[0] and (i, j, k) not in unpainted and cond(pixel_arrays[i], j, k, window_size, threshold):
                        unpainted.append((i, j, k))

        unpainted.pop(0)
    for i in range(len(pixel_arrays)):
        print(result[i][height][width])
    print(counter)
    return result


def cond_average_hemorrhage(pixel_array, i, j, window_size, threshold):
    try:
        summation = pixel_array[i - window_size][j] + pixel_array[i + window_size][j] + pixel_array[i][j - window_size] + pixel_array[i][j + window_size] + pixel_array[i - window_size][j - window_size] + pixel_array[i + window_size][j + window_size] + pixel_array[i + window_size][j - window_size] + pixel_array[i - window_size][j + window_size]
    except:
        return False
    if summation // 8 > threshold:
        return True
    else:
        return False


def detect_hemorrhage(brain_area):
    hemorrhage_area = np.full((len(brain_area), 512, 512), 0, dtype=np.int16)
    for i in range(len(brain_area)):
        for j in range(len(brain_area[0])):
            for k in range(len(brain_area[0][0])):
                if (brain_area[i][j][k] > threshold_hemorrhage[0] and cond(brain_area[i], j, k, window_size, threshold_hemorrhage)) or cond_average_hemorrhage(brain_area[i], j, k, window_size_cond_average, threshold_cond_average): # hemorrhage detection
                    hemorrhage_area[i][j][k] = brain_area[i][j][k]

    return hemorrhage_area


def cond_average_hemorrhage_3d(pixel_arrays, frame, row, column, window_size, threshold):
    try:
        summation = 0
        for i in range(frame - 1, frame + 1 + 1):
            for j in range(row - window_size, row + window_size + 1):
                for k in range(column - window_size, column + window_size + 1):
                    summation += pixel_arrays[i][j][k]
    except:
        return False
    if summation // ((window_size * 2 + 1) ** 2 * 3) < threshold / 4:
        return True
    else:
        return False


def hemorrhage_cleaning(hemorrhage_area, distance):
    for i in range(len(hemorrhage_area)):
        for j in range(len(hemorrhage_area[0])):
            for k in range(len(hemorrhage_area[0][0])):
                if hemorrhage_area[i][j][k] != 0:
                    try:
                        if cond_average_hemorrhage_3d(hemorrhage_area, i, j, k, window_size_cond_average, threshold_cond_average) or (hemorrhage_area[i][j][k + distance] + hemorrhage_area[i][j][k - distance] + hemorrhage_area[i][j + distance][k] + hemorrhage_area[i][j - distance][k] == 0 and hemorrhage_area[i - 1][j][k] + hemorrhage_area[i + 1][j][k] == 0):
                            hemorrhage_area[i][j][k] = 0
                    except:
                        pass
    return hemorrhage_area



def show_dicom(dicom_data, pixel_array):
    # Access metadata (header information)
    print("Patient ID:", dicom_data.PatientID)
    print("Study Description:", dicom_data.StudyDescription)
    print("Image Shape:", dicom_data.pixel_array.shape)
    
    plt.imshow(pixel_array, cmap=plt.cm.gray)
    plt.title("DICOM Image")
    plt.show()


if __name__ == '__main__':
    start_time = time.time()
    dicoms_pixel_array, dicom_data = open_dicoms(28)
    if is_3d:
        brain_area = flood_fill_bfs_3d(dicoms_pixel_array)
        hemorrhage_area = detect_hemorrhage(brain_area)
        hemorrhage_area = hemorrhage_cleaning(hemorrhage_area, hemorrhage_cleaning_parameter)
        hemorrhage_area = hemorrhage_cleaning(hemorrhage_area, hemorrhage_cleaning_parameter // 2)
        hemorrhage_area = hemorrhage_cleaning(hemorrhage_area, hemorrhage_cleaning_parameter // 4)
        print('finish processing. wait for saving!')
        for i in range(first_image_index, last_image_index):
            save_dicom(dicom_data, brain_area[i-first_image_index], i, directory_output_brain)
            save_dicom(dicom_data, hemorrhage_area[i-first_image_index], i, directory_output_hemorrhage)
            print('file ' + str(i) + ' saved')
    else:
        for i in range(first_image_index, last_image_index):
            brain_layer = flood_fill_bfs(dicoms_pixel_array[i - first_image_index])
            save_dicom(dicom_data, brain_layer, i, directory_output_brain)
            print('file ' + str(i) + ' saved')
            # show_dicom(dicom_data, pixel_array)
    end_time = time.time()
    print('execution time (in sec) : ' + str(int(end_time) - int(start_time)))
