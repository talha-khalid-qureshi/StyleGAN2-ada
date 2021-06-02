python dataset_tool.py --source=processed_input_folder --dest=final_data/input_folder.zip
python train.py --outdir=data_training_folder --data=final_data/input_folder.zip --gpu=1 --aug=ada

