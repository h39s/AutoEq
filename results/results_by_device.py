import os
import shutil
import string


AutoEQresults = os.path.join(os.getcwd(), 'results')
device_results = {}
device_results_folder = os.path.join(os.getcwd(), 'resultsbydevice')
if os.path.exists(device_results_folder):
    shutil.rmtree(device_results_folder)
os.mkdir(device_results_folder)


def folder_iterator(rootdir):
    return [f for f in os.listdir(rootdir) if os.path.isdir(os.path.join(rootdir, f))]

for measurer in folder_iterator(AutoEQresults):
    measurer_folder = os.path.join(AutoEQresults, measurer)
    
    for target in folder_iterator(measurer_folder):
        target_folder = os.path.join(measurer_folder, target)
        if target.startswith(measurer):
            target = target[len(measurer)+1:]
        target = string.capwords(target, sep='_').replace('_', ' ')
        
        for headphone in folder_iterator(target_folder):
            headphone_folder = os.path.join(target_folder, headphone)
            
            for eqFile in os.listdir(headphone_folder):
                eqFile_path = os.path.join(headphone_folder, eqFile)
                
                if eqFile.endswith('ParametricEQ.txt'):
                    source_to_name = (eqFile_path, target+' ('+measurer.capitalize()+')')
                    if device_results.get(headphone):
                        device_results[headphone].append(source_to_name)
                    else:
                        device_results[headphone] = [source_to_name]

for headphone, eqFiles in device_results.items():
    new_folder = os.path.join(device_results_folder, headphone)
    try:
        os.mkdir(new_folder)
    except FileExistsError:
        pass
        
    for eqFile_path, newFile_name in eqFiles:
        newFile_path = os.path.join(new_folder, newFile_name)
        shutil.copyfile(eqFile_path, newFile_path)
