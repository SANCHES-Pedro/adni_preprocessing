import numpy as np
from pathlib import Path
from glob import glob
import os
from matplotlib import pyplot as plt
import json
import csv
import time
import datetime
import SimpleITK as sitk
from typing import List

def get_unique_image_file(subject_protocol_folder : List[Path]):
    # the inversion [::-1] is done so the most preprocessed data is used
    found_image_ids = np.array([image_file.parents[0].name for image_file in subject_protocol_folder])
    inverse_found_image_ids = found_image_ids[::-1]
    ids, idx =  np.unique(inverse_found_image_ids,return_index = True)
    unique_image_ids_paths = np.array(subject_protocol_folder)[::-1][idx]
    
    assert len(unique_image_ids_paths) <= len(subject_protocol_folder)
    assert len(unique_image_ids_paths) > 0
    
    return unique_image_ids_paths


def intensity_normalization(volume : np.array, clip_ratio : float = 99.5):
    # Normalize the pixel values of volumes to (-1, 1)
    assert np.min(volume) == 0.0
    volume_max = np.percentile(volume, clip_ratio)
    volume = np.clip(volume/volume_max, 0, 1) * 2 - 1
    
    return volume

def run_fsl_processing(image_path,preprocessed_image_path):
    os.system(f'fslreorient2std {image_path} {preprocessed_image_path}')
    os.system(f'robustfov -i {preprocessed_image_path} -r {preprocessed_image_path}')
    os.system(f'bet {preprocessed_image_path} {preprocessed_image_path} -R')
    os.system(f'flirt -in {preprocessed_image_path} -ref {ref} -out {preprocessed_image_path}')
    # "fast" saves output file as {file_name}_restore.nii.gz
    os.system(f'fast --nopve -B -o {preprocessed_image_path} {preprocessed_image_path}')

def main():
    data_path = Path(r"/media/pedro/Data/PhD/UoE/Data/ADNI")
    
    preprocessed_data_path = data_path / "preprocessed_data"
    raw_data_path = data_path / "raw_data"

    resolution_mm = 2
    ref=f'/usr/local/fsl/data/standard/MNI152_T1_{resolution_mm}mm_brain.nii.gz' 


    subject_folder_list = list(raw_data_path.glob('*'))
    subjects_list = [subject_folder.name for subject_folder in subject_folder_list]
    nb_subjects = len(subjects_list)
    subjects_protocol_folder = [sorted(subject_folder.glob("**/*.nii")) for subject_folder in subject_folder_list]
    images_path_list = ([images_path for subject_protocol_folder in subjects_protocol_folder for images_path in get_unique_image_file(subject_protocol_folder)])
    nb_images = len(images_path_list)

    image_path = images_path_list[2]

    preprocessed_image_path = Path(str(image_path).replace("raw_data","preprocessed_data").replace(".nii",".nii.gz"))
    preprocessed_image_path.parent.mkdir(parents = True,exist_ok=True)

    start=time.time()
    run_fsl_processing(image_path,preprocessed_image_path)
    print(f'{datetime.timedelta(seconds=time.time()-start)}')





if __name__ == "__main__":
    main()