import re
import glob

line = "C_files=*.[ch]"
if re.match(r'\w+=[A-Za-z0-9$]+', line):
    print("shit")


line = "exit 3 "
if re.fullmatch( r'exit ?\d?(\s+)?', line):
    line = "sys.exit()"
    print(line)