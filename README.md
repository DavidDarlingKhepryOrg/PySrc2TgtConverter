# PySrc2TgtConverter
Convert text files in the specified source path into the specified target path, transforming their column delimiters and quoting characters in the process.

## Parameters

* **--src_path:** type=str, default='~/Desktop/TSVs/', help='source file path'
* **--src_file_extension:** type=str, default='.tsv', help='source file extension'
* **--src_col_delimiter:** type=str, default='\t', help='source column delimiter'
* **--src_col_quotechar:** type=str, default='"', help='source quoting character'

* **--tgt_path:** type=str, default='~/Desktop/CSVs/', help='target file path'
* **--tgt_file_extension:** type=str, default='.csv', help='target file extension'
* **--tgt_col_delimiter:** type=str, default=',', help='target column delimiter'
* **--tgt_col_quotechar:** type=str, default='"', help='targer quoting character'

* **--break_after_first_file:** type=bool, default=False, help='break after processing first file'
* **--progress_msg_template:** type=str, default='{:s}: {:,.0f} rows in {:.2f} secs at {:,.0f} rows/sec', help='progress message template'
* **--row_flush_interval:** type=int, default=100000, help='flush pending rows to file interval'
