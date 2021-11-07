import re

with open('INSERT DIRECTORY FOR YOUR TEXT FILE', encoding="utf-8") as f:
    lines = f.readlines()


##############################################################################
#                                                                            #
#                           POSTURING THE DATASET                            #
#                                                                            #
##############################################################################

# Posturing Dataset
tree = str(lines)
INDI = re.compile(r'@ INDI')

# Startig Point for Each Individual
span_start = []
matches = INDI.finditer(tree)
for INDI in matches:
   span_start.append(INDI.start())


##############################################################################
#                                                                            #
#                     EXTRACTING EACH PERSON'S NAME                          #
#                                                                            #
##############################################################################

# Initializing the Start and End points for each person's block
a = 0
b = 1

# Setting up structure for iterations
INDIblock = tree[span_start[a]:span_start[b]]

# Initializing list where all names will be stored
name_list = []

# Iterating through each person's individual block of information
while b < len(span_start):
    INDIblock = tree[span_start[a]:span_start[b]]
    
    # Searching for '1 NAME' within the individual's block 
    pattern_INDIblock = re.compile(r'1 NAME')
    matches_INDIblock = pattern_INDIblock.search(INDIblock)
    
    # Finding Index for Each New Line
    newline_test = re.compile(r'\\n')
    newline_matches_test = newline_test.finditer(INDIblock)
    
    # Initializing list to store the span location for each new line
    new_line = []
    
    # Storing the location of each new line
    for y in newline_matches_test:
        new_line.append(y.start())
        
    # Find Starting Point for INDI Block
    pattern_INDIblock = re.compile(r'1 NAME')
    matches_INDIblock = pattern_INDIblock.finditer(INDIblock)
    name_index = []
    for name in matches_INDIblock:
        name_index.append(name.start())
        
    # Extract the Name Using 1 NAME as Starting Point and /n as Ending Point
    name_search = INDIblock[name_index[0]:((new_line[1]))]
    
    # Regex to extract just the name
    pattern_name = re.compile(r"[-'a-zA-ZÀ-ÖØ-öø-ÿ]+[^1 NAME / , )]")
    matches_name = pattern_name.findall(name_search)

    # Appending name to list
    name_list.append(matches_name)

    # Incrementing block indicators for next person
    a = a + 1
    b = b + 1



##############################################################################
#                                                                            #
#                      EXTRACTING EACH PERSON'S SEX                          #
#                                                                            #
##############################################################################

# Initializing the Start and End points for each person's block
a = 0
b = 1

# Setting up structure for iterations
INDIblock = tree[span_start[a]:span_start[b]]

# Initializing list where all genders will be stored
sex_list= []

# Iterating through each person's individual block of information
while b < len(span_start):
    INDIblock = tree[span_start[a]:span_start[b]]
    
    # Searching for '1 SEX' within the individual's block 
    sex_pattern_INDIblock = re.compile(r'1 SEX')
    sex_matches_INDIblock = sex_pattern_INDIblock.search(INDIblock)

    # Find Starting Point for SEX Block
    sex_pattern_INDIblock = re.compile(r'1 SEX')
    sex_matches_INDIblock = sex_pattern_INDIblock.finditer(INDIblock)
    sex_index = []
    for sex in sex_matches_INDIblock:
        sex_index.append(sex.start())
        
    # Extract the Name Using 1 SEX as Starting Point and only considering 
    # 7 spaces to the right
    sex_search = INDIblock[sex_index[0]:((sex_index[0])+7)]

    # Regex to extract just the M or F
    pattern_sex = re.compile(r"[MFmf]")
    matches_sex = pattern_sex.findall(sex_search)

    # Appending Sex to list
    sex_list.append(matches_sex)

    # Incrementing block indicators for next person
    a = a + 1
    b = b + 1

