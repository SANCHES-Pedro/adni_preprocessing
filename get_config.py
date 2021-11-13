from pathlib import Path

def get_config_dict():
    config = {}
    #config["data_path"] = Path(r"/media/pedro/Data/PhD/UoE/Data/ADNI") / "raw_data"
    config["data_path"] = Path(r"/home/s2086085/idcom_data/Brain/ADNI1_raw/") 
    config["re_process"] = False
    
    resolution_mm = 2
    #config["reference_atlas_location"] = Path(f'/usr/local/fsl/data/standard/MNI152_T1_{resolution_mm}mm_brain.nii.gz')
    config["reference_atlas_location"] = Path(f'/home/s2086085/RDS/fsl/data/standard/MNI152_T1_{resolution_mm}mm_brain.nii.gz')
    config["axial_size"] = 90
    config["save_2d"] = True
    return config
    