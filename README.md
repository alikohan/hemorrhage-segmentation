# Hemorrhage Segmentation

## Overview

This project was developed in 2024 at Arioobarzan Lab to detect and segment intracranial hemorrhages in CT scan images using an interpretable segmentation algorithm.

The dataset used during development was obtained from Shahid Rajaee Hospital, Shiraz, Iran. Because the dataset contains private medical data and cannot be publicly distributed, it is not included in this repository. However, the code can be applied to your own DICOM files in either 2D or 3D mode.

## Motivation and Objectives

The primary objective was to develop an interpretable and reliable expert system to help identify patients who may require urgent surgical intervention. The proposed system was intended to support clinical decision-making by estimating hemorrhage volume and identifying its location (i.e., intraparenchymal, intraventricular, Subarachnoid, Subdural, Epidural).

To support this objective, the project focused on detecting and segmenting hemorrhage regions in CT scans using a flood fill algorithm. The method supports both 2D and 3D CT images, with 3D processing generally producing better segmentation results.

Note: The system was developed as a research prototype and has not been established as a clinically validated tool for determining surgical urgency.

## Methodology

The segmentation algorithm uses flood fill to identify hemorrhage regions in CT scan images. During development, particular attention was given to handling variations and inconsistencies in the input data.

Two major challenges emerged:

Robustness: The algorithm was sensitive to variations in image quality, anatomical structures, and dataset consistency.

Computational cost: Processing CT volumes, particularly in 3D, was computationally expensive.

To overcome the first problem, I tried to incorporate different methodologies into the code, especially, because the data was highly noisy and inconsistent, I had to design the algorithm to be as robust as possible. A novel, simple method that I used to improve robustness is described in the following. To address the second issue, I planned to rewrite the code in C, using different vectorization and optimization methods to increase execution speed.

However, after introducing Detectron2 and testing it on brain hemorrhage CT scans, we realized that it outperformed our method in most cases in terms of both robustness and computational efficiency. Consequently, the project was paused at this stage.

## Results

The following figures show the results of applying the method to CT scan images to segment hemorrhage areas:

<p align="center"><img width="700" alt="AbnormalPatientStripping" src="https://github.com/user-attachments/assets/d37edc1f-9245-4fe8-9f48-d248fdf96adb" /></p>
<p align="center">(1)</p>

<p align="center"><img width="700" alt="AbnormalPatientStripping2" src="https://github.com/user-attachments/assets/f5c86d61-8217-4dbd-ae78-16b57b7aab41" /></p>
<p align="center">(2)</p>

<p align="center"><img width="700" alt="AbnormalPatientStripping3" src="https://github.com/user-attachments/assets/20773a29-ed18-4cc6-a183-ac1fad9534ba" /></p>
<p align="center">(3)</p>

<p align="center"><img width="700" alt="NormalPatientStripping2" src="https://github.com/user-attachments/assets/7eef148a-8d58-48e3-b13a-6c24196895bd" /></p>
<p align="center">(4)</p>

<p align="center"><img width="700" alt="NormalPatientStripping" src="https://github.com/user-attachments/assets/1026cfd4-1122-4818-89c9-38082c50177c" /></p>
<p align="center">(5)</p>

This figure compares the performance of the 2D and 3D algorithms on complex CT scans:

<p align="center"><img width="700" alt="performance of 2d vs 3d" src="https://github.com/user-attachments/assets/22d07198-bb80-4552-b8a1-23913ce98805" /></p>
<p align="center">comparison of the performance of 2d and 3d algorithms</p>

This figure illustrates an example of a case in which the flood fill algorithm fails:

<p align="center"><img width="700" alt="FloodFill_weakness" src="https://github.com/user-attachments/assets/58e56f5f-f986-4963-8123-f60dee17e7ad" /> /></p>
<p align="center">flood fill weakness</p>

To mitigate this problem, I proposed an algorithm to make the segmentation method more robust in such cases:

<p align="center"><img width="700" alt="formula" src="https://github.com/user-attachments/assets/700765a2-71f3-455f-950f-bcaed5a0009c" /></p>
<p align="center">the novel formula I used</p>

The result of using this algorithm:

<p align="center"><img width="700" alt="FloodFill_fixError" src="https://github.com/user-attachments/assets/9eb4cb53-b3d1-44ae-9094-96d74b960aab" /></p>
<p align="center">the result of applying the formula</p>









