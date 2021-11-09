from pathlib import Path

def get_config_dict():
    config = {}
    config["data_path"] = Path(r"/media/pedro/Data/PhD/UoE/Data/ADNI") / "raw_data"
    resolution_mm = 2
    config["reference_atlas_location"] = Path(f'/usr/local/fsl/data/standard/MNI152_T1_{resolution_mm}mm_brain.nii.gz')