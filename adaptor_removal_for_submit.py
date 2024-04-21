'''
first, manually check all RemainContamination files are raised for adpator comntaminations,
then put all RC file into a folder,
Last, run this script to remove them
'''

import os,sys,subprocess
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord


def parse_RC_file(file):
    seq_adaptor = {}
    res = subprocess.run(['sed', '-n','/Trim:/,/^$/p', file], capture_output=True, text=True)
    result = res.stdout.split('\n')[2:]

    for line in result:
        if line != '':
            split = line.split('\t')
            seq_adaptor[split[0]] = [eval(i) for i in split[2].split('..')]

    return seq_adaptor


def remove_adaptor(dic,fasta,outfasta):
    with open(fasta, 'r') as f:
        records = list(SeqIO.parse(f, 'fasta'))

    filted_records = []
    count = 0
    for record in records:
        if record.id not in dic:
            filted_records.append(record)
        else:
            count += 1
            start,end = min(dic[record.id])-1,max(dic[record.id])

            seq1 = record.seq[0:start]
            seq2 = record.seq[end:]

            if len(seq1) == 0 and len(seq2) != 0:
                filted_records.append(SeqRecord(seq2, id=f'{record.id.split("_adaptor_")[0]}_rm_adaptor', description=""))
            elif len(seq2) == 0 and len(seq1) != 0:
                filted_records.append(SeqRecord(seq1, id=f'{record.id.split("_adaptor_")[0]}_rm_adaptor', description=""))
            elif len(seq1) != 0 and len(seq2) != 0:
                if len(seq1) > 200:
                    filted_records.append(SeqRecord(seq1, id=f'{record.id.split("_adaptor_")[0]}_rm_adaptor_1', description=""))
                if len(seq2) >= 200:
                    filted_records.append(SeqRecord(seq2, id=f'{record.id.split("_adaptor_")[0]}_rm_adaptor_2', description=""))

    if count != len(list(dic.keys())):
        print('Some seqs are not found in the fasta file')

    SeqIO.write(filted_records, outfasta, 'fasta')


def main():
    pwd = os.getcwd()

    RC_files = os.listdir(sys.argv[1])
    RC_parse = {}
    os.chdir(sys.argv[1])

    for file in RC_files:
        split = file.rstrip('.txt').split('_')
        bin_name = f'{split[-4]}_{split[-3]}_{split[-2]}_{split[-1]}.fasta'
        RC_parse[bin_name] = parse_RC_file(file)

    os.chdir(pwd)

    try:
        os.mkdir(sys.argv[3])
    except FileExistsError:
        os.system(f'rm -r {sys.argv[3]}')
        os.mkdir(sys.argv[3])

    abs = os.path.abspath(sys.argv[3])

    fasta_lis = os.listdir(sys.argv[2])
    os.chdir(sys.argv[2])

    for fasta in fasta_lis:
        if fasta in RC_parse:
            remove_adaptor(RC_parse[fasta], fasta, f'{abs}/{fasta}')

    os.chdir(pwd)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 script.py RC_folder fasta_folder output_folder')
        sys.exit(1)
    main()
