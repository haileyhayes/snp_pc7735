#! /usr/bin/env python3
#
# ================================================================================ #
# Filename:snpsnip.py
# Author: Hailey Hayes
# Date Created: 2026/11/12 21:25
# Version: 1
# ================================================================================ #
# Usage:
# Input SNP files of different types, and recieve output of either..
# -> a list of rs accession numbers
# -> a list of ClinVar VCV accession IDs
# -> a trimmed VCF file (e.g. for use with EMBL's VEP)
# ================================================================================ #

import sys
import gzip
import re


if len(sys.argv)<3: # sys.argv usage check
    print('\t[!] Invalid input!')
    print('\tUsage: snpsnip.py <input_file> <output_file>')
else:
    infile: str=sys.argv[1]
    outfile: str=sys.argv[2]


if sys.argv[1].endswith('.gz'): # allow for opening gzip files too
    infileOpen=gzip.open(infile,'rt')
else:
    infileOpen=open(infile,'r')

outfileOpen=open(outfile,'w') # open outfile

# welcome message
print(('O---o \n'
       ' O-o  \t SNP Snip!\n'
       '  O   \n'
       ' o-O  \t  A helper script to trim your SNP file \n'
       'o---O \t - - - - - - - - - 8< - - - - - - - - - - \n'
       'O---o \t Requirements: \n'
       ' O-o  \t   8< Use tab-separated file \n'
       '  o   \t   8< Know the original file source\n'
       ' O-o  \n'
       'O---o'))

while True:
    # user prompt
    print(('><><><><><><><><><><><><><><><><><><><><><><><><><><\n'
           'Output options:\n'
           '\t [rs] ................ get dbSNP rs accession\n'
           '\t [VCV] ............ get ClinVar VCV accession\n'
           '\t [VCF]  .............. get trimmed VCF format\n'
           '\t [?]  ................................. Help\n'
           '\t [Q]  ................................. Quit\n'
           ))

    user_prompt: str=input('Choose an option...').upper()

    if user_prompt=="?": # help block
        print(('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n'
               'Help:\n'
               '[rs]: dbSNP Reference Sequence (rs):\n'
               '\t -> Output contains:\n'
               '\t    rs accession number\n\n'
               '[VCV]: ClinVar VCV:\n'
               '\t -> Output contains:\n'
               '\t    VCV accession number\n\n'
               '[VCF]: Trimmed VCF format:\n'
               '\t -> Output contains:\n'
               '\t    chrom | pos (1-based) | ref | alt*\n\n'
               '\t\t\t*includes all alts'
               ))
        continue

    if user_prompt not in ["RS","VCV","VCF","?","Q"]: # error message
        print(('****************************************************\n'
               'Invalid input!\n'
               '\tPlease select one of the following options:'
               ))
        continue

    if user_prompt=="Q": # quit program message
        print(('Exiting SNP Snip now\n'
               '- - - - - 8< - - - - - - - - Goodbye! - - - - - - -'
               ))
        break

    if user_prompt in ["RS","VCV","VCF"]:

        rs=[]
        vcv=[] # empty lists for appending

        # output: dbSNP RS accession number in outfile
        if user_prompt=="RS":
            for Line in infileOpen:
                rssnp: list=re.findall(r"\brs\d+\b", Line)
                rs.append(rssnp)
                rsclean=[x for x in rs if x]
            rsstring='\n'.join(''.join(str(obj) for obj in x) for x in rsclean)
            outfileOpen.write(rsstring)
            print('\tFile written to...', outfile)

        # output: ClinVar VCV accession number in outfile
        if user_prompt=="VCV":
            for Line in infileOpen:
                vcvid: list=re.findall(r"\bVCV\d+\b", Line)
                vcv.append(vcvid)
                vcvclean=[x for x in vcv if x]
            vcvstring='\n'.join('\t'.join(str(obj) for obj in x) for x in vcvclean)
            outfileOpen.write(vcvstring)
            print('\tFile written to...', outfile)

        # output: trimmed VCF in outfile
            # e.g. ready for use in VEP
        if user_prompt=="VCF":
            print(('><><><><><><><><><><><><><><><><><><><><><><><><><><\n'
                    'What is the original file source?\n'
                    '[1]: dbSNP | [2]: UCSC Table Browser\n'
                    )) # allow user to select the file origin, so parsing works as expected

            file_origin: str=input('Choose an option...')
            if file_origin not in ["1","2"]:
                print("[!] Invalid input!\n Please select one of the following options:")
                continue
            # dbSNP origin file
            if file_origin=="1": # selects columns based on positions in dbSNP file output
                print('Original file source: dbSNP')
                for Item in infileOpen:
                    if Item[0].startswith("#"):
                        continue
                    else:
                        Item=Item.strip('\n').split('\t')
                        chr=Item[0]
                        pos=Item[1]
                        snp_id=('rs'+Item[4])
                        var_raw=Item[2]
                        if len(var_raw)>=2:
                            var_regex=re.split(r"[>,]", var_raw.strip()) # get rid of > in between refs and alts
                            ref=var_regex[0]
                            alt=','.join(var_regex[1:]).replace('-','') # remove indel 
                        
                    outlist=' '.join([chr,pos,snp_id,ref,alt])+'\n'
                    outfileOpen.write(outlist)
                print('\tFile written to...', outfile)
                break

            # UCSC Table Browser origin
            if file_origin=="2": # selects columns based on UCSC Table Browser positions
                print('Original file source: UCSC Table Browser')
                for Item in infileOpen:
                    if Item[0].startswith("#"):
                        continue
                    else:
                        Item=Item.strip('\n').split('\t')
                        chr_raw=Item[0].strip()
                        chrom_chr=chr_raw.split("_")[0]
                        chrom=chrom_chr.replace('chr','')
                        pos=Item[2] # use ChromEnd, becaue VCF is 1-based
                        snp_id=Item[3]
                        ref=Item[4]
                        alt=Item[6].rstrip(',')
                        
                    outlist=' '.join([chrom,pos,snp_id,ref,alt])+'\n'
                    outfileOpen.write(outlist)
                print('\tFile written to...', outfile)
                break

    infileOpen.close()
    outfileOpen.close()
    break
