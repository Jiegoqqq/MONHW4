import pandas as pd 
import warnings
from subprocess import PIPE, Popen
import os 
from tqdm import trange 
warnings.filterwarnings("ignore")

def site_arrange(site_data,genome_data):
    ## upstream 45 down stream 9
    site_data['start_site'] = ''
    site_data['end_site'] = ''
    site_data['sequence'] = ''
    reverse ={'A':'T',"T":"A","C":"G","G":"C"}
    # reverse_RNA = {"A":"U","T":"A","C":"G","G":"C"}
    for i in trange(len(site_data)):
        if site_data['direction'][i] =='+':
            site_data['start_site'][i] = int(site_data['genome_site'][i])-45
            site_data['end_site'][i] = int(site_data['genome_site'][i])+9
            site_data['sequence'][i] = genome_data[1][site_data['start_site'][i]-1:site_data['end_site'][i]]
        elif(site_data['direction'][i]) =='-':
            site_data['start_site'][i] = int(site_data['genome_site'][i])+45
            site_data['end_site'][i] = int(site_data['genome_site'][i])-9
            site_data['sequence'][i] = list(map(lambda x:reverse[x],genome_data[1][site_data['end_site'][i]-1:site_data['start_site'][i]][::-1]))
            site_data['sequence'][i] = ''.join(site_data['sequence'][i])
    return (site_data)

def site_arrange_modified(site_data,genome_data):
    ## upstream 41 down stream 3
    site_data['start_site'] = ''
    site_data['end_site'] = ''
    site_data['sequence'] = ''
    reverse ={'A':'T',"T":"A","C":"G","G":"C"}
    # reverse_RNA = {"A":"U","T":"A","C":"G","G":"C"}
    for i in trange(len(site_data)):
        if site_data['direction'][i] =='+':
            site_data['start_site'][i] = int(site_data['genome_site'][i])-41
            site_data['end_site'][i] = int(site_data['genome_site'][i])+3
            site_data['sequence'][i] = genome_data[1][site_data['start_site'][i]-1:site_data['end_site'][i]]
        elif(site_data['direction'][i]) =='-':
            site_data['start_site'][i] = int(site_data['genome_site'][i])+41
            site_data['end_site'][i] = int(site_data['genome_site'][i])-3
            site_data['sequence'][i] = list(map(lambda x:reverse[x],genome_data[1][site_data['end_site'][i]-1:site_data['start_site'][i]][::-1]))
            site_data['sequence'][i] = ''.join(site_data['sequence'][i])
    return (site_data)

def RNAfold(site_data,index_col,sequence_col):
    command = "RNAfold < 'tmp.fa'"
    output_list = []
    output_energy = []
    for i in trange(len(site_data)):
        with open("tmp.fa",'w') as file:
            file.write(f">{site_data[index_col][i]}\n{site_data[sequence_col][i]}")
        with Popen(command, stdout=PIPE, stderr=None, shell=True) as process:
            output = process.communicate()[0].decode("utf-8")
            output = output.split('\n')
            output_sequence_energy = output[2].split(' (')
            output_list.append(output_sequence_energy[0].split(' ')[0])
            output_energy.append(output_sequence_energy[1].strip(')'))
        try:
            os.remove(f"{site_data[index_col][i]}_ss.ps")
        except:
            pass
    return(output_list,output_energy)



if __name__ =='__main__':
    with open ('NC_000913_spikeRNA.fna','r') as genome_file:
        genome_data = genome_file.readlines()

    # site_data = pd.read_csv("S09_09_WT_log_3L.bowtie2mapping.rRNA_filtered_sorted_terminator.txt",sep='\t')    
    # result = site_arrange(site_data,genome_data)
    # result.to_csv("own_S09_09_WT.csv")        

    ### test region
    # d= {'direction':['-'],'genome_site':['9891']}
    # site_data = pd.DataFrame(d)
    # result = site_arrange(site_data,genome_data)
    # result.to_csv("test_neg.csv")

    site_data = pd.read_excel("2019_Nat Microbiol_Ju_full-length RNa profiling reveals pervasive bidirectional transcription terminators in bacteria_TSS annotation.xlsx",header =[1])
    site_data.rename(columns={"TTS_position":"genome_site","TTS_strand":"direction"},inplace=True)
    result = site_arrange(site_data, genome_data)
    reverse_RNA = {"T":"U","A":"A","G":"G","C":"C"}
    result['upstream_45_downstream_9'] = list(map(lambda x:''.join([reverse_RNA[i] for i in x]),result['sequence']))
    result_diff = result[result['upstream_45_downstream_9'] != result['RNA_sequence_around_TTS_site']]
    result[['TTS_serial_number','genome_site','direction','upstream_45_downstream_9','RNA_sequence_around_TTS_site','TTS_sequence(include_8nt_of_each_flank_sequence)','predicted_RNA_fold_structure']].to_csv("origin_add_up45down9.csv")    

    
    ###
    # doing the RNAfold for given dataframe by own data
    site_data = pd.read_csv("origin_add_up45down9.csv",index_col=[0])
    site_data.reset_index(inplace=True)
    output_list_45,output_energy_45 = RNAfold(site_data,'index','upstream_45_downstream_9')
    output_list_site,output_energy_site = RNAfold(site_data,'index','RNA_sequence_around_TTS_site')
    output_list_TTS,output_energy_TTS = RNAfold(site_data,'index','TTS_sequence(include_8nt_of_each_flank_sequence)')
    
    site_data['RNAfold(up45 down9)'] = output_list_45
    site_data['RNAfold(TTS sequence new)'] = output_list_TTS
    site_data['RNAfold(site new)'] = output_list_site
    site_data['RNAfold_energy(up45 down9)'] = output_energy_45
    site_data['RNAfold_energy(TTS sequence new)'] = output_energy_TTS
    site_data['RNAfold_energy(site new)'] = output_energy_site

    site_data.to_csv("origin_add_up45down9.csv",index=False)
    ###
    
    ###
    ## doing the RNAfold for given dataframe
    # site_data = pd.read_excel("2019_Nat Microbiol_Ju_full-length RNa profiling reveals pervasive bidirectional transcription terminators in bacteria_TSS annotation.xlsx",header =[1])
    # output_list,output_energy = RNAfold(site_data,'TTS_serial_number','RNA_sequence_around_TTS_site')

    # RNA_fold_list = ['TTS_serial_number','TTS_position','TTS_strand','RNA_sequence_around_TTS_site','TTS_sequence(include_8nt_of_each_flank_sequence)','predicted_RNA_fold_structure',' ∆G (kcal/mol)']
    # output_data = site_data[RNA_fold_list]
    # output_data['own_RNAfold(TTS_site)'] = output_list
    # output_data['own_RNAfold_energy(TTS_site)'] = output_energy
    # output_data['len(site)'] = output_data['RNA_sequence_around_TTS_site'].apply(lambda x:len(x))
    # output_data['len(predicted_RNA_fold_structure)'] = output_data['predicted_RNA_fold_structure'].apply(lambda x:len(x))
    # output_data['len(own_RNAfold(TTS_site))'] = output_data['own_RNAfold(TTS_site)'].apply(lambda x:len(x))
    # output_data.to_csv("RNA_fold_compare_TTS_site.csv",index=False)
    ###