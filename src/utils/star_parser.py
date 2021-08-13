#!/usr/bin/env python
# coding: utf-8

# In[3]:


#file types
'''
star
box
topaz file
filament_style file
'''


# In[4]:


class star_parser:
    def __init__(self, input_type, output_type, input_file):
        self.input = input_type
        self.mode = output_type
        self.input_file = input_file
    
    def parse():
        strategy.parse()


# In[5]:


from abc import ABC, abstractmethod

class strategy(ABC):
    @abstractmethod
    def parse(self):
        pass


# In[8]:


class correct_strategy_1(strategy):
    def correct(x, dx, pixel_size):
        return float(x)-float(dx)/pixel_size


# In[19]:


import os

class star3_to_topaz(strategy):
    
    def __init__(self, input_file, output_path, selection_list, value_index, pixel_size, split = True, callback = correct_strategy_1.correct,                name_index = 1, optional_attributes = [], header = "",                basename = True):
        self.input = input_file
        self.output_path = output_path
        self.selection_list = selection_list
        self.split = split
        self.pixel_size = pixel_size
        self.callback = callback
        self.name_index = name_index
        self.value_index = value_index # index of x ,y, dx, dy in a list, 1-start
        self.optional_attributes = optional_attributes # for example, dummy threshold scores to add to the end of files
        self.header = header
        self.basename = basename

        
    
    def parse(self):
        f = open(self.input, "r")
        
        Lines = f.readlines()
        print(f.name)
        
        Lines = Lines[len(Lines) - Lines[::-1].index("loop_\n"):]
        print(Lines[1])
        
        oldName = ""
        
        #for single file mode:
        contains_header = False
        
        
        for line in Lines:
            if line[0] == "_":
                continue
            print(line)
            parts = line.split()
            print(parts)
            
            parts[self.value_index[0]-1] = self.callback(parts[self.value_index[0]-1],                                                      parts[self.value_index[2]-1],                                                      self.pixel_size)
            parts[self.value_index[1]-1] = self.callback(parts[self.value_index[1]-1],                                                      parts[self.value_index[3]-1],                                                      self.pixel_size)
            
            if (self.basename) :
                output_line_list = [os.path.basename(str(parts[i-1])) for i in self.selection_list]
            else:
                output_line_list = [(str(parts[i-1])) for i in self.selection_list]
            
            for item in self.optional_attributes:
                output_line_list.append((str(item)))
            
            output_line = "\t".join(output_line_list) + "\n"
            
            if (self.split):
                if (parts[self.name_index-1]!= oldName):
                    oldName = parts[self.name_index-1]
                    print(oldName)
                    o = open(os.path.join(self.output_path, os.path.splitext(os.path.basename(parts[self.name_index-1]))[0]+".txt"), "w")
                    o.write(self.header)
                    o.write(output_line)
                else:
                    o.write(output_line)
                    
            else:
                o = open(os.path.join(self.output_path, "unsplit_output.txt"),"a")
                
                if (not contains_header):
                    o.write(self.header)
                    contains_header = True
                
                o.append(output_line)
                
        o.close()


'''


parser = star3_to_topaz("C:/Users/Zhe Fan/Documents/J107Output.star", "./Spam", [2,3,4], [3,4,7,8], 2.74, name_index = 2, optional_attributes = [-6,])



parser.parse()
'''

