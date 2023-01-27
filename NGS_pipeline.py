import os 

print("loading samplenames ...")

home_path="" #enter the path to your home directory

raw_path=home_path+"raw_data/"          #all those folders need to be located within your home directory
trimmed_path=home_path+"trimmed_reads/"
reference_path=home_path+"reference/"
vcf_path=home_path+"vcf_files/"
bam_path=home_path+"bam_files/"

os.system("ls "+raw_path+" > "+home_path+"temp.txt") #getting samplenames
file=open(home_path+"temp.txt","r")

samplelist=[]
samplename=""
samplelist2=[]
reads=""

depth_EGFP=[]
depth_av=[]

trimmoutput=""
trimmomatic_options="ILLUMINACLIP:/path/to/TruSeq3-PE.fa:2:30:10:2:keepBothReads LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36"

for line in file:                                               #loading samplenames into samplename list
    samplename=line[:line.find("_R")]
    if samplename not in samplelist:
        samplelist.append(samplename)

file.close()
os.system("rm "+home_path+"temp.txt")

print("trimming samplenames ...")

for name in samplelist:                                         
    samplename=name[:name.find("_")]                             #trimming samplenames
    if samplename not in samplelist2:
        samplelist2.append(samplename)

    reads=raw_path+name+"_R1_001.fastq.gz "+raw_path+name+"_R2_001.fastq.gz "
    trimmoutput=trimmed_path+samplename+"_forward_paired.fq.gz "+trimmed_path+samplename+"_forward_unpaired.fq.gz "+trimmed_path+samplename+"_reverse_paired.fq.gz "+trimmed_path+samplename+"_reverse_unpaired.fq.gz "
    os.system("java -jar $EBROOTTRIMMOMATIC/trimmomatic-0.39.jar PE "+reads+trimmoutput+trimmomatic_options)

    
    
print("mapping and variant calling ...")    

for name in samplelist2:       #mapping trimmed paired reads to reference, reference is already indexed
    os.system("bwa mem -t 10 "+reference_path+"HSV-1_F-BAC.fa "+trimmed_path+name+"_forward_paired.fq.gz "+trimmed_path+name+"_reverse_paired.fq.gz > "+bam_path+name+".sam")  
    os.system("samtools view -Sb "+bam_path+name+".sam | samtools sort - > "+bam_path+name+".bam")
    os.system("rm "+bam_path+name+".sam")
    os.system("samtools index "+bam_path+name+".bam")

    os.system("bwa mem -t 10 "+reference_path+"EGFP.fa "+trimmed_path+name+"_forward_paired.fq.gz "+trimmed_path+name+"_reverse_paired.fq.gz > "+bam_path+name+"_EGFP.sam")  
    os.system("samtools view -Sb "+bam_path+name+"_EGFP.sam | samtools sort - > "+bam_path+name+"_EGFP.bam")
    os.system("rm "+bam_path+name+"_EGFP.sam")
    os.system("samtools index "+bam_path+name+"_EGFP.bam")
                               #variant call
    os.system("lofreq call-parallel --pp-threads 10 -f "+reference_path+"HSV-1_F-BAC.fa -o "+vcf_path+name+"_lofreq.vcf "+bam_path+name+".bam")  
    os.system("bgzip "+vcf_path+name+"_lofreq.vcf")
    os.system("tabix "+vcf_path+name+"_lofreq.vcf.gz")

    os.system("bcftools mpileup -f "+reference_path+"HSV-1_F-BAC.fa "+bam_path+name+".bam | bcftools call -cv -Ov --ploidy 1 -o "+vcf_path+name+"_c.vcf")
    os.system("bgzip "+vcf_path+name+"_c.vcf")
    os.system("tabix "+vcf_path+name+"_c.vcf.gz")
    
    os.system("samtools depth -r EGFP "+bam_path+name+"_EGFP.bam > "+home_path+"coverage/"+name+"_cov_EGFP.txt")
    os.system("samtools depth -r HSV-1_F-BAC "+bam_path+name+".bam > "+home_path+"coverage/"+name+"_cov_av.txt")
    file_EGFP=open(home_path+"coverage/"+name+"_cov_EGFP.txt","r")
    file_av=open(home_path+"coverage/"+name+"_cov_av.txt","r")

    coverage_EGFP=[]
    coverage_av=[]
    for EGFP in file_EGFP:
        coverage_EGFP.append(EGFP.split())
        
    for av in file_av:
        coverage_av.append(av.split())
        
    cov_E=0.0
    cov_av=0.0
    
    for EGFP in coverage_EGFP:
        cov_E=cov_E+float(EGFP[2])

    for av in coverage_av:
        cov_av=cov_av+float(av[2])
        
    if len(coverage_EGFP)>0:    
        cov_E=cov_E/len(coverage_EGFP)
    else:
        cov_E=0
        
    if len(coverage_av)>0:    
        cov_av=cov_av/len(coverage_av)
    else:
        cov_av=0    
    
        
        
    depth_EGFP.append([name,cov_E])
    depth_av.append([name,cov_av])
    file_EGFP.close()
    file_av.close()
    
out_EGFP="name;EGFP depth\n"
out_av="name;average depth\n"
for EGFP in depth_EGFP:
    out_EGFP=out_EGFP+EGFP[0]+";"+str(EGFP[1])+"\n"

for av in depth_av:
    out_av=out_av+av[0]+";"+str(av[1])+"\n"
    
outfile_EGFP=open(home_path+"coverage/depth_EGFP.csv","w")
outfile_EGFP.write(out_EGFP)
outfile_av=open(home_path+"coverage/depth_av.csv","w")
outfile_av.write(out_av)
outfile_EGFP.close()
outfile_av.close()
    
print("done!")
    
    
    
    
