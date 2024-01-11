import sys
#======================================taking_input_from_file=======================++=============================#
lines = sys.stdin.read().splitlines()


#take input from file then uncomment
# with open('test_case1.txt') as f: 
#     lines = f.read().splitlines()
n=len(lines)

#=========================================Useful_dictionary========================================================#
operations = {
   "add":["00000","A"],"sub":["00001","A"],"mov1":["00010","B"],
   "mov2":["00011","C"],"ld":["00100","D"],"st":["00101","D"],
   "mul":["00110","A"],"div":["00111","C"],"rs":["01000","B"],
   "ls":["01001","B"],"xor":["01010","A"],"or":["01011","A"],
   "and":["01100","A"],"not":["01101","C"],"cmp":["01110","C"],
   "jmp":["01111","E"],"jlt":["10000","E"],"jgt":["11101","E"],
   "je":["11111","E"],"hlt":["11010","F"]
}
op_symbol = ["add","sub","mov","ld","st","mul","div","rs","ls",
                   "xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt"]
R_address = {
  "R0":"000","R1":"001","R2":"010",
  "R3":"011","R4":"100","R5":"101",
  "R6":"110","FLAGS":"111"}

all = ["add", "sub", "mov", "ld", "st", "mul", "div", "ls", "rs", "xor", "or",
        "label:", "and", "not", "cmp", "jlt", "jmp", "jgt", "je", "hlt",
        "R0", "R1", "R2", "R3", "R4", "R5", "R6", "FLAGS", "var"]

registers_flag= [ "R0", "R1" , "R2" , "R3" , "R4" , "R5" , "R6" , "FLAGS"]

#=================================Storing_all_useful_information_in_list_dictionary=================================#

labels = []
labels_with_adresss={}
M_address = {}
variables = {}
l1=[]
Guess = 1
address = -1

x = 0
i = 0
while i < n:
    a = lines[i].split()
    if len(a) > 1 and a[0] == "var":
        l1.append(a[1])
        all.append(a[1])
        x += 1
    else:
        break
    i += 1


for i in range(0,n):
    a=lines[0].split()
    if len(a)>0 and a[0][-1] == ":":
        all.append(a[0])
        all.append(a[0][:-1])
    if len(a)>2 and a[0] == "mov":
        if a[2][0] == "$":
            all.append(a[2])

#=======================================Storing_address_instruct_in_label============================================#

for line in lines:
    if len(line) == 0:
        continue
    instruct = list(line.split())

    if instruct[0] in op_symbol:
        address += 1

    if instruct[0] == "hlt":
        labels.append(instruct[0])
        labels_with_adresss[instruct[0]+":"]=address
       

    if instruct[0][-1] == ":":
        labels.append(instruct[0])
        labels.append(instruct[0][:-1])
        address += 1
        M_address[instruct[0][:-1]] = address
        labels_with_adresss[instruct[0]]=address

for i in labels:
    all.append(i)

for line in lines:
    if(len(line)==0):
        continue
    instruct = list(line.split())

    if instruct[0]=="var" and len(instruct)==2:
        variables[instruct[1]]=Guess+address
        Guess+=1


#================================================Error_checking_code==============================================#
no_error=False

def missing_hlt():
    global no_error
    count =0
    for i in lines:
        if "hlt" in i:
            count+=1
        else:
            pass
    if count==0:
        print("Error: hlt statement not present!")
        no_error = True

def hlt_not_last():
    global no_error

    i = 0
    while i < n:
        if lines[i] == "hlt" and i != n-1:
            print("Error: hlt can only be used at the end!", i,"lines")
            no_error = True
            break
        i += 1

def undefined_variable():
    global no_error

    i = 0
    while i < n:
        l = lines[i].split()

        if l[0] == "ld" or l[0] == "st":
            if l[2] not in l1:
                print("Error: Use of undefined variables",l[2],i, "lines")
                no_error = True
                break
        i += 1


def undefined_label():
    global no_error
    i = 0
    while i < n:
        l = lines[i].split()
        if l[0] == "jmp" or l[0] == "jlt" or l[0] == "jgt" or l[0] == "je":
            if l[1] not in labels:
                print("Error: Use of undefined labels",i,"lines")
                no_error = True
                break
        i += 1

def illegal_flag():
    global no_error
    i = 0
    while i < n:
        l = lines[i].split()
        if l[0] == "mov":
            pass
        i += 1

def immediate_val():
    global no_error
    
    for i in range(0, n):
        l = lines[i].split()
        if l[0] == "mov" or l[0] == "ls" or l[0] == "rs":
            if l[2][0] == "$":
                if int(l[2][1:]) < 0 or int(l[2][1:]) > 255:
                    print("Error: Illegal Immediate instruct used in line:", i,"lines")
                    no_error = True
                    break


def misuse_lables():
    global no_error 

    for i in range(n):
        l = lines[i].split()
        if l[0] in ["jmp" ,"jlt", "je" , "jgl"]:
            if l[1] in l1:
                print("Error: Misuse of labels as variables or vice-versa",i,"lines")
                no_error = True
                break
        elif l[0] == "st" or l[0] == "ld":
            if l[2] in labels:
                print("Error: Misuse of labels as variables or vice-versa",i,"lines")
                no_error = True
                break


def var_start():
    global no_error
    
    for i in range(1, n):
        l = lines[i].split()
        if l[0] == "var":
            j = i - 1
            while j >= 0:
                if lines[j].split()[0] != "var":
                    print("Error: Variables not declared at the beginning", i,"lines")
                    no_error = True
                    break
                j -= 1
        break

 

def typo_error():
    global no_error
    for i in range(0, n):
        l = lines[i].split()
        if l[0] not in all:
            print("Error: Typos in instruction name or register name ",i,"lines")
            no_error = True
            break
        elif l[0] in ["add", "sub", "mul" ,"or" , "and" , "xor"]:
            if l[1] not in all or l[2] not in all or l[3] not in all:
                print("Error: Typos in instruction name or register name ",i,"lines")
                no_error = True
                break
        elif l[0] in ["mov" , "rs" ,"ls"]:
            if l[1] not in all:
                print("Error: Typos in instruction name or register name ",i,"lines")
                no_error = True
                break
        elif l[0] in ["div", "not" , "cmp"]:
            if l[1] not in all or l[2] not in all:
                print("Error: Typos in instruction name or register name ",i,"lines")
                no_error = True
                break
        elif l[0] == "ld" or l[0] == "st":
            if l[1] not in all:
                print("Error: Typos in instruction name or register name",i,"lines")
                no_error= True
                break
#================================================#Calling function*================================================#
missing_hlt()
hlt_not_last()
undefined_variable()
undefined_label()
illegal_flag()
immediate_val()
misuse_lables()
var_start()
typo_error()


#============================================='''If there is no errror'''=========================================#
#==============================================The_running_part_of_the_code=======================================#
if not no_error:
    
    for line in lines:
        if len(line) == 0:
            continue

        instruct = list(line.split())

        if len(instruct) > 1 and instruct[0] in labels_with_adresss and instruct[1] in op_symbol:
            instruct.pop(0)

        if instruct[0] in op_symbol:
            if instruct[0] == "mov":
                if instruct[2][0] == "$":
                    instruct[0] = "mov1"
                else:
                    instruct[0] = "mov2"

            if instruct[0]=="add":
                a = instruct[1]
                b = instruct[2]
                c = instruct[3]
                final = operations[instruct[0]][0] + "00" + R_address[a] + R_address[b] + R_address[c]

            elif instruct[0]=="sub":
                a = instruct[1]
                b = instruct[2]
                c = instruct[3]
                final = operations[instruct[0]][0] + "00" + R_address[a] + R_address[b] + R_address[c]
            
            elif instruct[0]=="mul":
                a = instruct[1]
                b = instruct[2]
                c = instruct[3]
                final = operations[instruct[0]][0] + "00" + R_address[a] + R_address[b] + R_address[c]

            elif instruct[0]=="xor":
                a = instruct[1]
                b = instruct[2]
                c = instruct[3]
                final = operations[instruct[0]][0] + "00" + R_address[a] + R_address[b] + R_address[c]

            elif instruct[0]=="or":
                a = instruct[1]
                b = instruct[2]
                c = instruct[3]
                final = operations[instruct[0]][0] + "00" + R_address[a] + R_address[b] + R_address[c]

            elif instruct[0]=="and":
                a = instruct[1]
                b = instruct[2]
                c = instruct[3]
                final = operations[instruct[0]][0] + "00" + R_address[a] + R_address[b] + R_address[c]


            elif instruct[0]== "mov1":
                a = instruct[1]
                b = instruct[2][1:]
                b1 = bin(int(b))[2:]

                final = operations[instruct[0]][0] + "0"+ R_address[a] + (8-len(b1)-1)*"0" + b1
            
            elif instruct[0]== "rs":
                a = instruct[1]
                b = instruct[2][1:]
                b1 = bin(int(b))[2:]
                final = operations[instruct[0]][0] + R_address[a] + (8-len(b1))*"0" + b1

            elif instruct[0]== "ls":
                a = instruct[1]
                b = instruct[2][1:]
                b1 = bin(int(b))[2:]
                final = operations[instruct[0]][0] + R_address[a] + (8-len(b1))*"0" + b1

            
            elif instruct[0] == "mov2":
                a = instruct[1]
                b = instruct[2]
                final = operations[instruct[0]][0] + "00000" + R_address[a] + R_address[b]

            elif instruct[0]== "div":
                a = instruct[1]
                b = instruct[2]
                final = operations[instruct[0]][0] + "00000" + R_address[a] + R_address[b]

            elif instruct[0]== "not":
                a = instruct[1]
                b = instruct[2]
                final = operations[instruct[0]][0] + "00000" + R_address[a] + R_address[b]

            elif instruct[0] == "cmp":
                a = instruct[1]
                b = instruct[2]
                final = operations[instruct[0]][0] + "00000" + R_address[a] + R_address[b]

            
            elif instruct[0]== "ld":
                a = instruct[1]
                b = bin(variables[instruct[2]])[2:]
                final = operations[instruct[0]][0] + "0"+R_address[a] + (8 - len(b)-1) * "0" + b
                

            elif instruct[0]== "st":
                a = instruct[1]
                b = bin(variables[instruct[2]])[2:]
                final = operations[instruct[0]][0] + "0"+ R_address[a] + (8 - len(b)-1) * "0" + b
    
            elif instruct[0] == "jmp":
                a=instruct[1]
                b=bin(labels_with_adresss[a+":"])[2:]
                final=operations[instruct[0]][0] + "000" + (8 - len(b)) * "0" + b

            elif instruct[0] == "jgt":
                a = instruct[1]
                b=bin(labels_with_adresss[a+":"])[2:]
                final=operations[instruct[0]][0] + "000" + (8 - len(b)) * "0" + b

            elif instruct[0] == "jlt":
                a = instruct[1]
                b=bin(labels_with_adresss[a+":"])[2:]
                final=operations[instruct[0]][0] + "000" + (8 - len(b)) * "0" + b

            
            elif instruct[0] == "je":
                a=instruct[1]
                b=bin(labels_with_adresss[a+":"])[2:]
                final=operations[instruct[0]][0] + "000" + (8 - len(b)) * "0" + b

            elif instruct[0] == "hlt":
                final = operations[instruct[0]][0] + "00000000000"


            print(final)

































