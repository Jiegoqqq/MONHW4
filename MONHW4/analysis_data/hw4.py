import pandas as pd 
import warnings
from subprocess import PIPE, Popen
import os 
from tqdm import trange 

def RNAfold(site_data,index_col,sequence_col):
    command = "RNAfold < 'tmp.fa'"  #之後command要處理的指令
    output_list = []
    output_energy = []
    current_working_directory = os.getcwd()
    os.chdir('/home/jiego/1122MON/MONHW4/own_S09_RNAfold')
    for i in trange(len(site_data)): #trange用來迭代處理每一行
        with open("tmp.fa",'w') as file:
            file.write(f">own_S09_{site_data[index_col][i]}\n{site_data[sequence_col][i]}")
        with Popen(command, stdout=PIPE, stderr=None, shell=True) as process:
            output = process.communicate()[0].decode("utf-8")
            output = output.split('\n')
            output_sequence_energy = output[2].split(' (')
            output_list.append(output_sequence_energy[0].split(' ')[0])
            output_energy.append(output_sequence_energy[1].strip(')'))
    os.chdir(current_working_directory)
    return(output_list,output_energy)



if __name__ =='__main__':

    
    ###
    # doing the RNAfold for given dataframe by own data
    site_data = pd.read_csv("own_S09_09_WT.csv",index_col=[0])
    site_data.reset_index(inplace=True)#重設index那行
    output_list,output_energy = RNAfold(site_data,'index','sequence')

    
    site_data['RNAfold'] = output_list
    site_data['RNAfold_energy'] = output_energy


    site_data.to_csv("own_S09_09_WT_RNAfold.csv",index=False)
    ###
    