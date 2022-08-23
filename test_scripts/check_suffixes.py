import sys
import os
import check_suffix_item as csi
from ck3_common_utils import determine_root_dir

if __name__ == '__main__':
    root_dir = determine_root_dir(sys.argv[1])
    console_outuput = False
    
    console_outuput = False
    if ( len(sys.argv)>2 ):
        console_outuput = True
    
    
    exceptions_dir = '.known_errors/'
    item_type_list = ['scripted_triggers','scripted_effects']
    
    errors_found = False
    for item_type in item_type_list:
        suffix = csi.only_allow_effects_and_trigger(item_type)
        exceptions_fname = exceptions_dir+item_type+csi.exception_file_suffix+'.txt'
        test_error_found = csi.run_test(root_dir,item_type,suffix,exceptions_fname,console_outuput)
        if ( not test_error_found ):
            print('No '+item_type+' issues found')
        errors_found |= test_error_found
    
    if ( errors_found ):
        sys.exit(1)