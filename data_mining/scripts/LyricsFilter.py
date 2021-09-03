import re

def lyrics_filter(infile, outfile, writeMode):

    # Open the in and out files
    f = open(infile, "r", encoding="utf8")
    n = open(outfile, writeMode)

    # Compile the regular expressions to filter out song title lists and album lists
    regex_songtitle = re.compile(".* - .*")
    regex_songtitle2 = re.compile(".* — .*")
    regex_songyear = re.compile(".* \(\d*\)$")
    regex_leadingspace = re.compile(" .*")

    for line in f:
        # skip the regex's above
        if re.match(regex_songyear, line) or re.match(regex_songtitle, line) or re.match(regex_songtitle2, line) or re.match(regex_leadingspace, line):
            continue

        # skip lines >120 chars
        if len(line) >= 120:
            continue

        for i in line:
            # check for uppercase
            if (ord(i) >= 65 and ord(i) <= 90):
                print(i, file=n, end="")
            # check for lowercase
            elif (ord(i) >= 97 and ord(i) <= 122):
                print(i, file=n, end="")
            # check for newlines and spaces
            elif (ord(i) == 32 or ord(i) == 10):
                print(i, file=n, end="")
