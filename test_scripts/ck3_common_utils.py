import os
import re
import glob
import sys

from math import floor

'''
search_over_mod_structure
Arguments:
  root_dir: Directory Root Dir
  file_keyword: file keyword to search for in the file name (e.g., either the item type or '.+' 
    (everything in the database)
  file_action_object: class building the data object (a dictionary or a list, depending). Must have method action
    which takes a file name as an argument
  database: Which database to search; default is "common/", "events/", and "history/" top level folders
  check_localization: if the *.yml files should be searched; default is False
Desc:
  Finds a list of text files based on comparison of dir_name to item_type and does file_action
  (making a list of items to search over OR a dictionary of database instance counts)
  
  Note 1:
  Why wouldn't we add localization files? Because removal of other database items might void localization
  items. So stuff that's used in only in localization (like 'clan_government_levies_max_possible') should
  be an exclusion instead
'''
def search_over_mod_structure(root_dir,file_keyword,file_action_object,data_object,console_output,\
                              database=['common','events','history'],\
                              check_localization=False):
    if ( len(database)== 0): RuntimeError("Did not provide a database to search in cke_common_utils.py:search_over_mod_structure(); failing")
    
    print(root_dir)
    
    database_items = '('
    for item in database:
        database_items += item
        database_items += '|'
    database_items = database_items[:-1] #Remove the last '|'
    database_items += ')'
    
    file_list = [y for x in os.walk(root_dir) for y in glob.glob(os.path.join(x[0], '*.txt'))]
    
    #print(file_list)
    
    if ( check_localization ):
        file_list.extend([y for x in os.walk(root_dir) for y in glob.glob(os.path.join(x[0], '*.yml'))])
    for file,index in zip(file_list,range(len(file_list))):
        if ( console_output ): task_progress_meter(index,len(file_list))
        if ( re.search(file_keyword,file) and \
             compare_file_path_with_item(file,database_items) ):
            if ( isinstance(data_object,list) ):
                data_object.extend(file_action_object.action(file))
            else:
                data_object = file_action_object.action(file)
    if ( console_output ): task_progress_meter(len(file_list),len(file_list))
    return data_object

def compare_file_path_with_item(file_path,re_pattern):
    found_item = False
    file_path = file_path.split('/')
    file_path = file_path[:-1]
    
    for folder in file_path:
        if ( re.search('^'+re_pattern+'$',folder) ):
            found_item |= True
    
    return found_item

def task_progress_meter(workDone,totalWork):
    progress_meter_len = 20
    fracWorkDone = floor((workDone/totalWork)*progress_meter_len)
    progress_meter_string = '['+'*'*fracWorkDone+' '*(progress_meter_len-fracWorkDone)+']'
    print('\r'+progress_meter_string,end='')

def load_exceptions_list(fname):
    exception_list = []
    with open(fname,'r',encoding='utf-8') as f:
        for line in f:
            if ( not '#' in line ):
                exception_list.append(line.replace('\n',''))
    return list(set(exception_list))

def remove_exceptions_list(item_list,exception_list):
    return list(set(item_list)-set(exception_list))

#argument_list should be sys.argv
def determine_root_dir(root_dir_argument):
    # root_dir needs a trailing slash (i.e. /root/dir/)
    root_dir = ''
    #General case of modname/modname/common structure
    if os.path.isdir( './'+str(sys.argv[1])+'/' ):
        root_dir = sys.argv[1]
    #Case of modname/common
    elif ( os.path.basename(os.getcwd())==sys.argv[1] ):
        root_dir = './'
    else:
        print('No folder named '+str(sys.argv[1])+' exists; stopping execution')
        sys.exit(1)
    return root_dir

def console_input_parsing(exception_file_suffix):
    root_dir = determine_root_dir(sys.argv[1])
    exceptions_dir = '.known_errors/'
    item_type = []
    if (len(sys.argv)>2):
        item_type = sys.argv[2]
    else:
        item_type = '.+'
    #Exceptions file handling
    exceptions_fname = ''
    if(len(sys.argv)>3):
        exceptions_fname = sys.argv[3]
    else:
        if ( item_type == '.+' ): exceptions_fname = exceptions_dir+'all'+exception_file_suffix+'.txt'
        else: exceptions_fname = exceptions_dir+item_type+exception_file_suffix+'.txt'
    return root_dir,item_type,exceptions_fname

def common_exit(errors_found,item_type):
    if ( errors_found ):
        sys.exit(1)
    else:
        print('No '+item_type+' issues found')
        sys.exit(0)