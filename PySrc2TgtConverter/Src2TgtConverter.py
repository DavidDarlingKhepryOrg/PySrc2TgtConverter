# -*- coding: utf-8 -*-

# ========================================================================
#
# Copyright © 2016 Khepry Quixote
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ========================================================================


import argparse
import csv
import io
import os
import sys
import time


args = None # global arguments array


# mainline routine, by default:
#     src_extension is '.tsv'
#     tgt_extension is '.csv'        
#     source is tab-delimited and quoted as needed
#     target is comma-delimited and quoted as needed

def main(src_path,
         tgt_path,
         src_file_extension=None,
         tgt_file_extension=None,
         src_col_delimiter=None,
         tgt_col_delimiter=None,
         src_col_quotechar=None,
         tgt_col_quotechar=None,
         break_after_first_file=None,
         rows_flush_interval=None,
         progress_msg_template=None):
    
    if src_file_extension is None:
        src_file_extension = args.src_file_extension
    if tgt_file_extension is None:
        tgt_file_extension = args.tgt_file_extension
    if src_col_delimiter is None:
        src_col_delimiter = args.src_col_delimiter
    if tgt_col_delimiter is None:
        tgt_col_delimiter = args.tgt_col_delimiter
    if src_col_quotechar is None:
        src_col_quotechar = args.src_col_quotechar
    if tgt_col_quotechar is None:
        tgt_col_quotechar = args.tgt_col_quotechar
    if break_after_first_file is None:
        break_after_first_file = args.break_after_first_file
    if rows_flush_interval is None:
        rows_flush_interval = args.rows_flush_interval
    if progress_msg_template is None:
        progress_msg_template = args.progress_msg_template
    
    if src_path.startswith('~'):
        src_path = os.path.expanduser(src_path)
        
    if not os.path.exists(src_path):
        os.makedirs(src_path)
        
    if not os.path.exists(src_path):
        print('--src_path not found: %s' % src_path)
        sys.exit(404)

    if tgt_path.startswith('~'):
        tgt_path = os.path.expanduser(tgt_path)
        
    if not os.path.exists(tgt_path):
        os.makedirs(tgt_path)
        
    if not os.path.exists(tgt_path):
        print('--tgt_path not found: %s' % tgt_path)
        sys.exit(404)
    
    for root, _dirs, files in os.walk(src_path):
        for file in files:
            if file.lower().endswith(src_file_extension.lower()):
                tgt_file_name = os.path.join(tgt_path,
                                    os.path.splitext(file)[0] + tgt_file_extension)
                src_file_name = os.path.join(root, file)
                src2tgt_file(src_file_name,
                             tgt_file_name,
                             src_col_delimiter,
                             tgt_col_delimiter,
                             src_col_quotechar,
                             tgt_col_quotechar)
                if break_after_first_file:
                    break


# source to target file converter routine, by default:
#     source is tab-delimited and quoted as needed
#     target is comma-delimited and quoted as needed

def src2tgt_file(src_file_name,
                 tgt_file_name,
                 src_col_delimiter=None,
                 tgt_col_delimiter=None,
                 src_col_quotechar=None,
                 tgt_col_quotechar=None,
                 rows_flush_interval=None,
                 progress_msg_template=None):
    
    if src_col_delimiter is None:
        src_col_delimiter = args.src_col_delimiter
    if tgt_col_delimiter is None:
        tgt_col_delimiter = args.tgt_col_delimiter
    if src_col_quotechar is None:
        src_col_quotechar = args.src_col_quotechar
    if tgt_col_quotechar is None:
        tgt_col_quotechar = args.tgt_col_quotechar
    if rows_flush_interval is None:
        rows_flush_interval = args.rows_flush_interval
    if progress_msg_template is None:
        progress_msg_template = args.progress_msg_template
    
    print('')
    print('=============================')
    print('SRC file: %s' % src_file_name)
    print('-----------------------------')
    with io.open(tgt_file_name, 'w', newline='') as tgt_file:
        
        csv_writer = csv.writer(tgt_file,
                                delimiter=tgt_col_delimiter,
                                quotechar=tgt_col_quotechar,
                                quoting=csv.QUOTE_MINIMAL)
        
        with io.open(src_file_name, 'r', newline='') as src_file:
            csv_reader = csv.reader(src_file,
                                    delimiter=src_col_delimiter,
                                    quotechar=src_col_quotechar,
                                    quoting=csv.QUOTE_MINIMAL)
        
            rows = 0
            start_time = time.time()
            
            for row in csv_reader:
                rows += 1
                csv_writer.writerow(row)
                if rows % rows_flush_interval == 0:
                    tgt_file.flush()
                    elapsed_time = time.time() - start_time
                    print(progress_msg_template.format(src_file_name,
                                                       rows,
                                                       elapsed_time,
                                                       rows / elapsed_time if elapsed_time > 0 else rows))
        
        tgt_file.flush()
        elapsed_time = time.time() - start_time
        print(progress_msg_template.format(src_file_name,
                                           rows,
                                           elapsed_time,
                                           rows / elapsed_time if elapsed_time > 0 else rows))


def parse_cmdline_args(sys_argv):

    # handle incoming parameters,
    # pushing their values into the
    # args dictionary for later usage
    
    arg_parser = argparse.ArgumentParser(description='Convert text files in the source path into the target path')
    
    arg_parser.add_argument('--src_path',
                            type=str,
                            default='~/Desktop/TSVs/',
                            help='source file path')
    arg_parser.add_argument('--src_file_extension',
                            type=str,
                            default='.tsv',
                            help='source file extension')
    arg_parser.add_argument('--src_col_delimiter',
                            type=str, default='\t',
                            help='source column delimiter')
    arg_parser.add_argument('--src_col_quotechar',
                            type=str,
                            default='"',
                            help='source quoting character')
    
    arg_parser.add_argument('--tgt_path',
                            type=str,
                            default='~/Desktop/CSVs/',
                            help='target file path')
    arg_parser.add_argument('--tgt_file_extension',
                            type=str,
                            default='.csv',
                            help='target file extension')
    arg_parser.add_argument('--tgt_col_delimiter',
                            type=str,
                            default=',',
                            help='target column delimiter')
    arg_parser.add_argument('--tgt_col_quotechar',
                            type=str,
                            default='"',
                            help='target quoting character')
    
    arg_parser.add_argument('--break_after_first_file',
                            type=bool,
                            default=False,
                            help='break after processing first file')
    arg_parser.add_argument('--progress_msg_template',
                            type=str,
                            default='{:s}: {:,.0f} rows in {:.2f} secs at {:,.0f} rows/sec',
                            help='process message template')
    arg_parser.add_argument('--rows_flush_interval',
                            type=int,
                            default=100000,
                            help='flush rows to files interval')
    
    args = arg_parser.parse_args(sys_argv)
    
    return args


# invoke mainline routine
# with specified arguments
  
if __name__ == "__main__":
    
    args = parse_cmdline_args(sys.argv[1:])
    
    main(args.src_path,
         args.tgt_path,
         args.src_file_extension,
         args.tgt_file_extension,
         args.src_col_delimiter,
         args.tgt_col_delimiter,
         args.src_col_quotechar,
         args.tgt_col_quotechar,
         args.break_after_first_file,
         args.rows_flush_interval,
         args.progress_msg_template)
    
    print(os.linesep + 'Processing finished!')
