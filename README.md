# antiviral-resistance-evolution
This study investigated antiviral resistance evolution in herpes simplex virus type 1 and aimed to establish a mild hypermutator strain to accelerate adaptive processes.

Samples supposed to be included in this analysis should follow a certain labeling scheme: "genetic background", "selection", "passage" and "replicate" all in one line without space e.g. "wtACVPXXRep1". Populations samples were SNP called with LoFreq, therefore vcf files include "lofreq" in the filename e.g. "wtACVPXXRep1_lofreq.vcf.gz". Clonal samples were SNP called with BCFtools, therefore vcf files include "c" in the filename e.g. "wtGCVc1_c.vcf.gz".

Folder sturcture is assumed as followed:
```md

├── vcf_analysis.ipynp
├── reference.gb
└── "folder name"
     ├── vcf_files
     │   ├── e.g. wtACVPXXRep1_lofreq.vcf.gz
     │   └── e.g. wtACVPXXRep1_lofreq.vcf.gz.tbi
     ├── bam_files
     │   ├── e.g. wtACVPXXRep1.bam
     │   ├── e.g. wtACVPXXRep1.bam.bai
     │   ├── e.g. wtACVPXXRep1_EGFP.bam
     │   └── e.g. wtACVPXXRep1_EGFP.bam.bai
     ├── coverage
     │   ├── depth_av.csv
     │   ├── depth_EGFP.csv
     │   ├── e.g. wtACVPXXRep1_cov_av.txt            } generated with Samtools depth commmand
     │   └── e.g. wtACVPXXRep1_cov_EGFP.txt          }
     └── reads
         ├── e.g. wtACVPXXRep1_S1_L001_R1_001.fastq.gz
         └── e.g. wtACVPXXRep1_S1_L001_R2_001.fastq.gz
```
Regarding samplenames and location adjustment of scripts might be necessary


NGS pipeline depends on Trimmomatic, BWA, Samtools/BCFtools and Lofreq.
