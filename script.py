import re
import gzip
import json


module_name = []
findtop = {}
module_and_inst = {}
lib_files = {}
new_filelist={}
wrapper_need = 0
lib_true = 0
filelist_lines = ""
top_module = []
filelist = []




provide_filelist_path='!!!put your filelist here!!!'

def file_open(filelist_path):
    global filelist_lines
    file = open(filelist_path, 'r')
    filelist_lines = file.readlines()

def module_names(Lines):
    flag = False
    for line in Lines:
        if(re.findall("^\s?module\s+(\D\S+)\(",line)):
            module_name.append(re.findall("module\s+(\D\S+)\(",line)[0])
        elif(re.findall("^\s?module\s?[\n]",line) or flag==True):
            if(re.findall("\s+(\D\S+)\(",line)):
                if(flag):
                    flag=False
                    module_name.append(re.findall("(\D\S+)\(",line)[0])
            elif(re.findall("\s?(\D\S+)\(",line)):
                if(flag):
                    flag=False
                    module_name.append(re.findall("(\D\S+)\(",line)[0])
            elif(re.findall("[\t+](\D\S+)\(",line)):
                if(flag):
                    flag=False
                    module_name.append(re.findall("(\D\S+)\(",line)[0])
                
            elif(re.findall("\s+(\D\S+)#",line) ):
               
                if(flag):
                    flag=False
                    module_name.append(re.findall("(\D\S+)#",line)[0])
                
            elif(re.findall("\s+(\D\S+)\s?[\n]",line)):
                
                if(flag):
                    flag=False
                    module_name.append(re.findall("(\D\S+)\s?[\n]",line)[0])
            else:
                
                flag=True
                continue
        elif(re.findall("^\s?module\s+(\D\S+)\s?[\n]",line)):
            module_name.append(re.findall("module\s+(\D\S+)",line)[0]) 
        elif(re.findall("^\s+module\s+(\D\S+)\s?[\n]",line)):
            module_name.append(re.findall("module\s+(\D\S+)",line)[0]) 
        elif(re.findall("^\s?module\s+(\D\S+)",line)):
            module_name.append(re.findall("^\s?module\s+(\D\S+)",line)[0]) 
        else:
            continue
   
    return module_name

def instance_count(Lines,module_list,findtop):
    module_and_inst = {}
    flag = []
    for i in range(4):
        flag.append(False)
    
    count = []
    module = ""
    for i in module_list:
        for line in Lines:
            if(re.findall("^.*module\s+"+i,line)):
                module = i
                break



    for line in Lines:
        if(re.findall("^\s*//.*|^\s*/\*.*|^\s*module.*",line)):
                continue
        else:
            if(re.findall(".*#.*\(.*",line)  or flag[0] == True ):
                if(re.findall("^\s*\w+\s*#.*\(.*",line)):
                    module_count=re.findall("^\s*(\w+)\s*#.*\(.*",line)[0]

                if(re.findall("^.*\)\s+(\w+)\s*\(.*",line)):
                    flag[0] ==False
                    count.append(re.findall("^.*\)\s+(\w+)\s*\(.*",line))
                    inst= re.findall("^.*\)\s+(\w+)\s*\(.*",line)[0]
                    if(module_and_inst.get(module_count) is not None):
                        module_and_inst[module_count].append(inst)
                    else:    
                        module_and_inst[module_count] = [inst]
 
                elif(re.findall("^\s*\..*\)\s*\).*",line) or flag[1] == True ):
                    if(re.findall("^\s*(\w+)\s*\(",line)):
                        flag[1] = False
                        count.append(re.findall("^\s*(\w+)\s*\(",line))
                        inst = re.findall("^\s*(\w+)\s*\(",line)[0]
                        if(module_and_inst.get(module_count) is not None):
                            module_and_inst[module_count].append(inst)
                        else:    
                            module_and_inst[module_count] = [inst]
                    else:
                        if(flag[1]): 
                            flag[1] = False
                        else:
                            flag[1] = True
                        continue
                else: 
                    flag[0] = True
                    continue
            elif(re.findall("^\s*(\w+)\s+(\w+)\s*\(\..*",line)):
                module_count=re.findall("^\s*(\w+)\s+.*",line)[0]
                inst = re.findall("^\s*\w+\s+(\w+)\s*\(\..*",line)[0]
                if(module_and_inst.get(module_count) is not None):
                    module_and_inst[module_count].append(inst)
                else:    
                    module_and_inst[module_count] = [inst]
            elif(re.findall("^\s*\w+\s+(\w+)\s*[\n]",line) or flag[2]  == True):
                if(flag[2]==False):
                    module_count=re.findall("^\s*(\w+)\s+.*",line)[0]
                else:
                    pass

                if(flag[2]==False):
                    inst_temp = re.findall("^\s*\w+\s+(\w+)\s*[\n]",line)[0]
                else:
                    pass

                if(re.findall("^\s*\..*",line)):
                    inst = inst_temp
                    if(module_and_inst.get(module_count) is not None):
                        module_and_inst[module_count].append(inst)
                    else:    
                        module_and_inst[module_count] = [inst]
                    flag[2]  = False
                else:
                    if(flag[2]): 
                        flag[2] = False
                    else:
                        flag[2] = True
                    continue
            elif(re.findall("^\s*(\w+)\s+(\w+)\s+\(\s*[\n]",line) or flag[3]  == True):
              
                if(flag[3]==False):
                    module_count=re.findall("^\s*(\w+)\s+.*",line)[0]
                else:
                    pass

                if(flag[3]==False):
                    inst_temp = re.findall("^\s*\w+\s+(\w+)\s+\(\s*[\n]",line)[0]
                else:
                    pass

                if(re.findall("^\s*\..*",line)):
                    inst = inst_temp
                    if(module_and_inst.get(module_count) is not None):
                        module_and_inst[module_count].append(inst)
                    else:    
                        module_and_inst[module_count] = [inst]
                    flag[3]  = False
                else:
                    if(flag[3]): 
                        flag[3] = False
                    else:
                        flag[3] = True
                    continue

            else:
                continue

    findtop[module] = module_and_inst

        
    return findtop

def file_process(Lines,filelist):
    module_list = []
    counter = 0 
    if(len(Lines)==0):
        print("Please insert a valid filelist!")
    elif(len(Lines)>1):
        for i in Lines:
            j=re.split("[\n]",i)[0]
            files = open(j, 'r')
            read_line = files.readlines()
            module_list.append(module_names(read_line))
            if(len(module_name)!=len(list(filelist.keys()))):
                filelist[module_name[counter]] = i
                counter += 1
            
        for i in Lines:
            j=re.split("[\n]",i)[0]
            files = open(j, 'r')
            read_line = files.readlines()
            instance_count(read_line,module_list[-1],findtop)
    else:
        module_list = []
        if(re.split("\.",Lines[0])[-1]=='gz'):
            file=gzip.open(Lines[0],'rb')
            read_line=file.read()
        else:
            j=re.split("[\n]",Lines[0])[0]
            files = open(j, 'r')
            read_line = files.readlines()
        module_list.append(module_names(read_line))
        instance_count(read_line,module_list[-1],findtop)
        
    return filelist

def lib_finder(Lines,lib_files):
    filelist = open('new_filelist.txt',"w")
    filelist.close()
    lib_files["lib"]    = []
    lib_files["others"] = [] 
    counter = 0
    spec_counter = 0 
    if(len(Lines)==0):
        print("Please insert a valid filelist!")
    else:
        for i in Lines:
            j=re.split("[\n]",i)[0]
            files = open(j, 'r')
            read_line = files.readlines()
            for lines in read_line:
                if(re.findall("^\s*module.*\(",lines)):
                    
                    counter = counter +  1
                elif(re.findall("^\s*module\s*[\n]",lines)):
                    
                    counter = counter +  1
                elif(re.findall("^\s*module.*[\n]",lines)):
                    
                    counter = counter +  1
                elif(re.findall("^\s*module.*",lines)):
                    
                    counter = counter +  1
                elif(re.findall("^\s*specify.*",lines)):
                    spec_counter = spec_counter +  1
                elif(re.findall("^\s*table.*",lines)):
                    spec_counter = spec_counter +  1
                
            if(counter==0):
                lib_files["others"].append(j)
                
            elif(counter>1 & spec_counter > 1):
                lib_files["lib"].append(j)

            else:
                filelist = open('new_filelist.txt',"a")
                filelist.write(j+'\n')
                filelist.close()
            counter = 0

    return lib_files



file_open(provide_filelist_path)

lib_finder(filelist_lines,lib_files)

file_open("new_filelist.txt") ##Here Put the filelist name that we are getting from the "lib_finder" def. You can put it as a string or put the filename in a variable and put that variable here as argument

file_process(filelist_lines,new_filelist)


findtop_json = json.dumps(findtop,indent=4)



write_file = open('module_instance_report.json',"w")
write_file.write(findtop_json)
write_file.close()



