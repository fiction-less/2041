#! /usr/bin/env python3

import os, re, sys
import pprint
glob = []
ignoreDollar = []
backticks = []

soloSubs = ["ls", "date", "id", "pwd"]
subs = ["ls", "mkdir", "chmod", "touch", "rm"]
testStrOp = {"!=":"!=", "=":"=="}
testMathOp = {"-eq":"==", "-ne":"!=", "!=": "!=", "-gt":">", "-ge":">=", "-le":"<=", "-lt":"<"}
testPerms = {"-r":"os.R_OK", "-w":"os.W_OK", "-x":"os.X_OK"}
testFile = {"-d":"isdir", "-f":"isfile"}
testOther = {"-z": "== \"\"", "-n": "!= \"\""}
eraseLine = ["do", "done", "then", "fi"]

shellFile = sys.argv[1]
checkImport=[False]


    ##################################################
    #       TRANSPILATION HELPER FUNCTIONS
    ##################################################
def tryShebang(line):
    """ changes the hash bang """
    if line == "#!/bin/dash":
        checkImport[0] = True
        return line.replace("#!/bin/dash", "#!/usr/bin/python3 -u")
    return line


def checkImports(shellFile):
    """pre scans every line to check for imports and imports it"""
    sett = set()
    with open(shellFile) as shell:
        for line in shell:
            # get rif of commnets, find the last #
            index = line.rfind("#")
            if not re.match( r'^#', line):
                if not "\"" in line[index:] and not "\'" in line[index:] and not index == -1:
                    if not re.match(r' *$# *', line):
                        line = line[:index]

            if "*" in line or "?" in line or  "[" in line or "]" in line:
                if not re.match(r' *\w+ \[ [^\[\]]+ \]', line):
                    sett.add("import glob")
            if re.fullmatch( r'(\s+)?exit ?\d?(\s+)?', line) or re.search( r'\$\d+', line) or "$@" in line or "$#" in line:
                sett.add("import sys")

            ifORwhile = "(?:if|elif|while)"
            if "cd" in line or re.match( rf' *{ifORwhile} test \-[dfrwx] *(.*)', line):
                sett.add("import os")
            temp = soloSubs + subs

            for i in temp:
                if re.match( rf'^{i}', line):
                    sett.add("import subprocess")
                    break
            if "`" in line:
                sett.add("import subprocess")

    if len(sett) > 0:
        temp = list(sett)
        temp.sort()
        print("")
        for i in temp:
            print(i)


def tryBackTick(line):
    """subprocesses most backticks"""
    # if ` its in unccomented line then subprocess it.
    # if its a = scenario and not an echo

    if "`" in line:
        # if its a = scenario and not an echo
        if m := re.search(r"([^=`]+)=(`.+)", line):
            values = m.group(2).split()
            values = [ x.replace("`", "" ) for x in values]
            line = f"{m.group(1)} = subprocess.run({values}, text=True, stdout=subprocess.PIPE).stdout.rstrip(\'\\n\')"
        elif m := re.search(r"( *)echo .*(`[^`]+`)", line):
            values = m.group(2).split()
            values = [ x.replace("`", "" ) for x in values]
            print(f"{m.group(1)}{m.group(2)} = subprocess.run({values}, text=True, stdout=subprocess.PIPE).stdout.rstrip(\'\\n\')")
            line = line.replace(f"{m.group(2)}", f"${m.group(2)}")
            line = line.replace("`", "")
            # if its imberred in like an echo, then we make a seprate one
            # and choose a username?

        # if theres a $ sign in there, just get rid of it
        line = re.sub(r"\'\$([^\']+)\'", r"\1", line)
        line = f"{line}"

    return line.rstrip()



def tryEcho(line):
    """prints out echos, globs command args"""

    # 1. store double quotes, single quotes and all words split by either unnested quotes
    # 2. change any globs and change any command args
    # 3. formate the string into a print, including -n options

    listWords = []
    nFlag = False
    if re.fullmatch( r' *echo .*', line):

        words = re.sub( r' *echo *', "", line)
        if "echo -n" in line:
            words = re.sub( r'-n ', "", words)
            nFlag = True
        indent = re.search( r'( *)echo', line)
        quotation = ""

        singleQuote = []
        doubleQuote = []
        listWords = [] # this is the sentences split up

        # splits words up into either isngle quotes, or double quotes.
        if "\'"  in line and "\""  in line:

            single = line.find("\'")
            double = line.find("\"")
            # single comes first
            if single < double:
                singleQuote = re.findall(r"\'([^\']*)\'", words)
                [ignoreDollar.append(x) for x in listWords]
                quotation = "\'"
                doubleQuote = re.findall(r"\"([^\"]*)(?:\"|\')", words)
            else:
                doubleQuote = re.findall(r"\"([^\"]*)(?:\"|\')", words)
                temp = line
                for i in doubleQuote:
                    temp = temp.replace(i, "")
                singleQuote = re.findall(r"\'([^\']*)\'", temp)
                quotation="\""

        elif "\'"  in line:
            # finds all the words that are quotes. THIS ONE DOESNT EXPAND $
            singleQuote = re.findall(r"\'([^\"\']*)\'", words)
            [ignoreDollar.append(x) for x in listWords]
            quotation = "\'"
        elif "\""  in line:
            # this one will exand $
            doubleQuote = re.findall(r"\"([^\"\']*)(?:\"|\')", words)
            quotation="\""
        else:
            # default double quote
            quotation = "\""

        # create listwords, splitting up quotes and
        # not splitting up quotes within quotes
        count = 0
        prevCount = 0
        inQuotedSentence = False

        for i in words:
            if not inQuotedSentence:
                if i == "\"" or i == "\'":
                    quote = i
                    inQuotedSentence = True
                    listWords.append(words[prevCount:count])
                    prevCount = count + 1
            elif i == quote:
                    inQuotedSentence = False
                    listWords.append(words[prevCount:count])
                    prevCount = count + 1

            if int(count) == (len(words) - 1):
                listWords.append(words[prevCount:])
            count +=1

        listWords = [x for x in listWords if x.strip() != ""]


        def addGlob(count, end, word, glob, idx, format):

            if count == 1 and end == 1:
                # if its just a glob with nothing else
                listWords[idx] = re.sub( f"\{word}", f"{glob}",  listWords[idx])
                format = "solo"
            elif count == 1 and end != 1:
                # if its ag the beginning
                listWords[idx] = re.sub( f"\{word}", f"{glob} + \"",  listWords[idx])
                format = "beginning"
            elif count == end:
                # if its at the lend

                listWords[idx] = re.sub( f"\{word}", f"\" + {glob})",  listWords[idx])
                format = "end"
            else:
                # if its in the middle
                listWords[idx] = re.sub( f"\{word}", f"\" + {glob} + \"",  listWords[idx])
                format = "middle"
            return format

        idx = end = 0
        for str in listWords:
            for word in str.split():
                end +=1

        count = 1
        format = ""
        for str in listWords:

            # if its a non quote work, shrink its spaces
            if str not in doubleQuote and str not in singleQuote:
                listWords[idx] = re.sub(r" +", " ", str)

            for word in str.split():
                # globs wont work if its in single or double quotes.
                if  ("*" in word or "?" in word or  \
                    "[" in word or "]" in word) and \
                    str not in singleQuote and str not in doubleQuote:

                    glob = f"\" \".join(sorted(glob.glob(\"{word}\")))"
                    format = addGlob(count, end, word, glob, idx, format)


            #$@ only works in double quotes or non quotes.
                if "$@" in word and str not in singleQuote:
                    glob = f"\" \".join(sys.argv[1:])"
                    format = addGlob(count, end, "$@", glob, idx, format)

            #$# only works in double quotes or non quotes.

                if "$#" in word and str not in singleQuote:
                    glob = "str(len(sys.argv[1:]))"
                    format = addGlob(count, end, "$#", glob, idx, format)


                count += 1
            idx +=1

        words = "".join(listWords)
        # print(words, listWords)
        # pesky formatting, fixing print f quotations
        if format == "":
            line = f"print({quotation}{words}{quotation})"
        if format == "solo":
            line = f"print({words})"
        if format == "beginning":
            line = f"print({words}{quotation})"
        if format == "end":
            line = f"print({quotation}{words}"
        if format == "middle":
            line = f"print({quotation}{words}{quotation})"


        if indent != None: line = f"{indent.group(1)}{line}"
        # get rod of new line if -n option is enabled
        if nFlag:
            lastIndex = line.rfind(")")
            line = (line[:lastIndex] + ", end=\"\"" + line[lastIndex] )

        for x in singleQuote: ignoreDollar.append(x)

    return line.rstrip()



def tryEqual(line):
    """all this does it add a space between the equals, everything else left to dollar"""

    if words := re.match(r'( *)(\w+)=(?:\"|\')?([^\"\']+)*(?:\"|\')?', line):
        line = f"{words.group(1)}{words.group(2)} = \"{words.group(3)}\""
    return line.rstrip()


def tryDollar(line):
    """subs dollar signs into braces, and adds an f for prints when applicable"""

    linesWithRealDollars = line
    for i in ignoreDollar:
        linesWithRealDollars = linesWithRealDollars.replace(rf'{i.strip()}', '')

    if "$" in line:
        # dont translate if its a a subprocess but remove the $
        word = line.split()
        if word[0] in subs:
            return line

        # for the ${}
        if m := re.search(r"\$(\{[^\{\}\$]+\})", line):
            line = line.replace(f"${m.group(1)}", m.group(1))
            line = re.sub( r"print\(\"", "print(f\"", line)


        dollarWords = re.findall( r"\$([^\$\"\, ]+)", linesWithRealDollars)
        if dollarWords == []: return line
        # for workds, we want to splice out the != and =

        count = 0
        for i in dollarWords:

            if "!=" in i:
                temp = re.sub(r"\!\=.*", "", i)
                dollarWords[count] = (temp)
            elif "=" in i:
                temp = re.sub(r"\=.*", "", i)
                dollarWords[count] = (temp)
            count+= 1

        indent = re.search( r'( *).*', line)

        # if its only 1 variable like print($1) and its not a glob, dont add that f
        # this if for prints
        if m := re.fullmatch(r' *print\(\"\$([^ ]+)\"\)', line):

            if m.group(1) not in glob:
                if indent != None:
                    return f"{indent.group(1)}print({dollarWords[0]})"
                return f"print({dollarWords[0]})"

        # if its only 1 variable like DOG=$DOG dont add that f
        # this if for prints
        if "test" not in line and re.fullmatch(r' *[^\=\$]*= *\"?\$[^\$]+', line):
            # for $1 or $2 etc + vareiables
            py = dollarWords[0]
            if dollarWords[0].isdigit():
                py = f"sys.argv[{dollarWords[0]}]"
            line = re.sub( f"\"\${dollarWords[0]}\"", py, line)
            return line


        for i in dollarWords:

            # in case the word is stuck to a brakcet
            i = re.sub('(\'|\"|\)|\()', "", i)
            if i in glob:
                pyLine = f"print(\" \".join(sorted(glob.glob({i}))))"
                return pyLine
            else:
                # if the i is a number, then this is a sys.argv
                py = i
                if i.isdigit():
                    py = f"sys.argv[{i}]"
                # in case the input if like $file$file2 sub the first instance
                line = re.sub( fr"\${i}", "{"+py+"}", line,  count=1)


        # for prints, add an f
        line = re.sub( r"print\((\"|\')", r"print(f\1", line)
        # for =, add an f
        if "test" not in line: line = re.sub( r"= ", "= f", line)
        #if theres a dollar sign such that its ${string}, remove it
        line = re.sub( r"\$({[^{]+})", r'\1', line)

    return line



def tryGlob(line):
    # globbing
    if line == "echo *":
        line="print(\" \".join(sorted(glob.glob(\"*\"))))"
    elif "*" in line or "?" in line or  "[" in line or "]" in line:
        # if its an assignment
        if not " " in line and re.match(r'\w+=.*', line):
            words = re.search( r'(\w+)=(.*)', line)
            glob.append(words.group(1))
        # if its an echo
        if re.search( r'^echo', line):
            glob.append(line)

    return line

def tryFor(line):
    if words := re.search( r'(^for \b.+\b in) (.*)', line):
        listt = words.group(2).split()
        newList = [ f"\"{x}\"" for x in listt]
        joinedNewList = ", ".join(newList)

        # if its a glob the replace with with glob
        if "*" in joinedNewList or "?" in joinedNewList and len(newList) == 1:
            line = f"{words.group(1)} sorted(glob.glob({joinedNewList})):"
        else:
            line = f"{words.group(1)} [{joinedNewList}]:"
    return line.rstrip()


def tryExit(line):

    if re.fullmatch( r'(\s+)?exit ?\d?(\s+)?', line):
        if exitStat := re.match( r'(\s+?)exit (\d)', line):
             # for indents with number
            line = f"{exitStat.group(1)}sys.exit({exitStat.group(2)})"

        elif exitStat := re.match( r'exit (\d)', line):
            # for no indent with numbe
            line = f"sys.exit({exitStat.group(1)})"

        elif exitt := re.match( r'(\s+?)exit\s*', line):

            line = f"{exitt.group(1)}sys.exit()"
        else:
            line = "sys.exit()"

    return line

def tryCd(line):
    if re.match( r' *cd .*', line):

        # for indent
        if  m := re.match( r'( *)cd (.*)', line):
            line = f"{m.group(1)}os.chdir(\"{m.group(2)}\")"
        else:
            m = re.match( r'cd (.*)', line)
            line = f"os.chdir(\"{m.group(1)}\")"
    return line

def trySoloSubprocess(line):
    """single word subprocess - no variables"""
    if line.strip() in soloSubs:
        # for indent pwd
        if  m := re.match( r'( *)(.*)', line):
            line = f"{m.group(1)}subprocess.run([\"{m.group(2)}\"])"
    return line.rstrip()

def tryRead(line):
    if re.match( r' *read .*', line):
         # for indent
        if m := re.match( r'( *)read (.*)', line):
            line = f"{m.group(1)}{m.group(2)} = input()"
        else:
            m = re.match( r'read (.*)', line)
            line = f"{m.group(1)} = input())"
    return line

def trySubprocess(line):
    """ subprocesses with variables, simple version without stdout flags etc"""
    for i in subs:
        temp = line
        if  sList := re.match( rf'( *)({i} .*)', line):

            sist = [ x for x in sList.group(2).split() if "$@" not in x]

            line = f"{sList.group(1)}subprocess.run({sist})"
            # if the words is dollared, get rid of it and its quotes
            line = re.sub( r'\'\$([^\']+)\'', r"\1", line)

            # idk this is like dodgy af but
            if "$@" in temp:
                line = re.sub(r"\)$", r' + sys.argv[1:])', line)
    return line.rstrip()


def tryTest(line):
    ifORwhile = "(?:if|elif|while)"
    str1 = "(?:\"|\')?([^-=!\"\']+)(?:\"|\')?"
    str2 = "(?:\"|\')?([^\"\']+)(?:\"|\')?"
    multipleBraces = "[^\{]*\{[^\{\}]+\}\{[^\{\}]+\}.*"
    singleBraces = "[^\{]*\{[^\{\}]+\}"
    deleteBraces = True


    if re.match( rf' *{ifORwhile} test .*',line):
        if (parts := re.match( rf'(^ *)({ifORwhile}) test (\-[rwx]) *(.*)', line)):

            # for file permissions
            operator = parts.group(3)
            file = parts.group(4)
            if not re.match(r'[^\{]*\{[^\{\}]+\}', file):
                file = "\"" + file + "\""
            elif re.match(rf'{multipleBraces}', file):
                # more than 2 braces then add that f
                file = "f\"" + parts.group(4) + "\""
                deleteBraces = False

            if operator in testPerms:
                line = fr"{parts.group(1)}{parts.group(2)} os.access({file}, {testPerms[operator]}):"

        elif  parts := re.match( rf'(^ *)({ifORwhile}) test (\-[zn]) *(.*)', line):
            # testing null strings
            operator = parts.group(3)
            if operator in testOther:
                line = f"{parts.group(1)}{parts.group(2)} {parts.group(4)} {testOther[operator]}:"

        elif parts := re.match( rf'(^ *)({ifORwhile}) test (\-[df]) *(.*)', line):
            # for file stuff
            operator = parts.group(3)
            if operator in testFile:
                line = f"{parts.group(1)}{parts.group(2)} os.path.{testFile[operator]}(\"{parts.group(4)}\"):"

        elif parts := re.match( rf'(^ *)({ifORwhile}) test *{str1} *([^ ]+) *{str2}', line):

            # for math operators
            indent = parts.group(1)
            ifelif = parts.group(2)
            arg1 = parts.group(3).rstrip()
            operator = parts.group(4)
            arg2 = parts.group(5)

            if operator in testStrOp:
                # note that = and != are always just string comparisons
                if "{" not in arg1: arg1 = "\"" + arg1 + "\""
                if "{" not in arg2: arg2 = "\"" + arg2 + "\""
            else:
                if "{" not in arg1 and not arg1.isdigit(): arg1 = "\"" + arg1 + "\""
                if "{" not in arg2 and not arg2.isdigit(): arg2 = "\"" + arg2 + "\""


            if re.match(rf'{multipleBraces}', arg1) or (re.match(rf'\w+{singleBraces}', arg1)):
                deleteBraces = False
                arg1 = f"f\"{arg1}\""
            else:
                 arg1 = arg1.replace(r"{", "").replace(r"}", "")


            if re.match(rf'{multipleBraces}', arg2) or (re.match(rf'\w+{singleBraces}', arg2)):
                deleteBraces = False
                arg2 = f"f\"{arg2}\""
            else:
                arg2 = arg2.replace(r"{", "").replace(r"}", "")

            if operator in testMathOp:
                line = f"{indent}{ifelif} int({arg1}) {testMathOp[operator]} int({arg2}):"

            if operator in testStrOp:
                line = f"{indent}{ifelif} {arg1} {testStrOp[operator]} {arg2}:"

        # if theres a variables ( e.g. a $row)
        if deleteBraces:
            line = re.sub("(\"|\')?{", "",line)
            line = re.sub("}(\"|\')?", "",line)



    return line

def tryElse(line):
    if line.strip() == "else":
        line = line.replace("else", "else:")
    return line



    ##################################################
    #       TRANSPILATION FACTORY
    ##################################################

def transpile(line):
    """a transpiler factory, transforms each line step by step"""
    pyLine = tryShebang(line)
    pyLine = tryBackTick(pyLine)
    pyLine = tryGlob(pyLine)
    pyLine = tryEcho(pyLine)
    pyLine = tryEqual(pyLine)
    pyLine = tryDollar(pyLine)
    pyLine = tryFor(pyLine)
    pyLine = tryExit(pyLine)
    pyLine = tryCd(pyLine)
    pyLine = trySoloSubprocess(pyLine)
    pyLine = tryRead(pyLine)
    pyLine = trySubprocess(pyLine)
    pyLine = tryTest(pyLine)
    pyLine = tryElse(pyLine)
    return pyLine



    ##################################################
    #       MAIN FUNCTITON
    ##################################################

with open(shellFile) as shell:
    """ the main, and loops through all lines, printing the transpiled version"""
    for line in shell:
        line = line.rstrip("\n")

        # separtes the line and the comment if applicable
        comment = ""
        index = line.rfind("#")
        if not re.match( r'^#', line):
            if not "\"" in line[index:] and not "\'" in line[index:] and not index == -1:
                #makeing sure its not a $#
                if not re.search(r' *\$\# *', line):
                    comment = line[index:]
                    line = line[:index]


        ##################################################
        #   pre-transpile prep work (conversions)
        ##################################################

        # converts [] into test for simpler code
        if re.match(r' *\w+ \[ [^\[\]]+ \]', line):
            line = re.sub("\[", "test", line)
            line = re.sub ("\]", "", line)

        # convert andrew=god to andrew = god and != as well
        # edge case: if the args have an = or != in it then nothing will work anytmore
        if ( m := re.match( fr' *\w+ test [^=!]+(=|!=)[^ ]', line)):
            operator = m.group(1)
            line = re.sub(rf'{operator}', rf' {operator} ', line)

        # if its an eraseable line like do or dont, only keep the comments
        if line.strip() in eraseLine:
            if comment.strip() != "":
                print(comment)
            continue

        # transpule and add comment back again
        line = transpile(line)
        line += " " + comment


        print(line.rstrip())

        if checkImport[0]:
            checkImports(shellFile)
            checkImport[0] = False
        ignoreDollar = []