## SNP Analysis Project

### Project overview

> Evaluate SNPs from a chosen gene through gathering data from several databases, then create plots using data extracted from trimmed file. 

### Part 1: Data cleaning (snpsnip.py)

`clinvar_download_mapt.tsv` —>`snpsnip.py`—> `cv2tb.csv` (UCSC Table Browser) —>`snpsnip.py`—> `trimmedvcf.tsv`  

Base Python was used to create a helper script to extract columns of data chosen by user inputs. Options include extracting dbSNP rs accession numbers, ClinVar VCV accession IDs, or creating a trimmed VCF from files downloaded from UCSC Table Browser or dbSNP. 

### Part 2: Data analysis

Using results generated from a VEP tab-separated file, pandas, numpy, and matplotlib packages were used at several parts to extract, prepare, and plot data. This file was created using a Jupyter notebook (.ipynb), so each coding cell could be run independently. 

### Project pipeline:

I used the ClinVar database to find (reviewed) SNPs for the MAPT gene. Based on the search criteria, 402 entries were found, and downloaded to a TSV file. I used the snpsnip.py helper script to extract rs IDs to a separate file (260 total), which I then pasted into UCSC Table Browser to also get position and mutation data for each SNP (670 lines). I used snpsnip.py again to create a trimmed VCF file (669 lines, -header) from the Table Browser result to plug in to Ensembl VEP. I decided to use VEP to find more information about the pathogenicity of each SNP, and find amino acid changes associated with each SNP. This step of the analysis was done by converting the VEP output to a pandas data frame, and plotted through matplotlib in order to visualize the data. 

#### Builds + Parameters

ClinVar search: [link](https://www.ncbi.nlm.nih.gov/clinvar/search/?gene=mapt&assembly=GRCh38)

Genome build used (ClinVar, UCSC Table Browser, Ensembl VEP):
GRCh38/hg38

dbSNP track (UCSC Table Browser):
155


