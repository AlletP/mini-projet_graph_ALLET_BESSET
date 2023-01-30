import multiprocessing as mp
import time
from multiprocessing import Manager, Process
import os
import model.social_reg_ALLET_BESSET as sr
from pathlib import Path


def slave(config,rank, res_dict,verbose=True):
    start = time.time()
    print(f"Process {rank} started at {time.strftime('%d %b %Y %H:%M:%S', time.gmtime(start))}")
    rmses, maes = sr.soc_reg(config, rank, verbose)
    res_dict[rank] = (rmses[0], maes[0])
    print("ici")
    print(res_dict)
    end = time.time()
    print(f"Process {rank} stopped at {time.strftime('%d %b %Y %H:%M:%S', time.gmtime(end))}")
    print(f"Execution time for process {rank} : {end-start} seconds")


def para(config,verbose):
    current_file_path = os.path.abspath(__file__)
    current_file_directory = os.path.dirname(current_file_path)
    res_dir = config.result_path
    # change cwd to the current file directory
    os.chdir(current_file_directory)

    manager = Manager()
    res_dict = manager.dict()
    proc = []

    nb_folds = config.k_fold_num
    nb_proc = nb_folds

    start = time.time()
    for rank in range(nb_proc):
        p = Process(target=slave, args=(config,rank, res_dict,verbose))
        proc.append(p)
        p.start()
        
    print("Début des calculs en parallèle")
    for p in proc:
        p.join()

    rmse_sum = 0
    mae_sum = 0

    for i in range(nb_proc):
        rmse_sum += res_dict[i][0]
        mae_sum += res_dict[i][1]

    rmse_avg = rmse_sum / nb_proc
    mae_avg = mae_sum / nb_proc

    end = time.time()
    print(f"The average of RMSES is {rmse_avg}")
    print(f"The average of MAES is {mae_avg}")
    print(f"Total execution time : {end-start} seconds")
    res_str = [f"The average of RMSES is {rmse_avg}\n",f"The average of MAES is {mae_avg}\n",f"Total execution time : {end-start} seconds\n"]
    
    #sauvegarde des résultats dans des fichiers textes
    Path(res_dir).mkdir(parents=True, exist_ok=True)
    if(not (os.path.exists(res_dir+"/res.txt"))):
        f=open(res_dir+'res.txt',"x")
        f.writelines(res_str)
        f.close()
    else:
        f=open(res_dir+'res.txt',"w")
        f.writelines(res_str)
        f.close()
