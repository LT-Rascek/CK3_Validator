import sys
import os
import check_database_item as cdi
from ck3_common_utils import determine_root_dir

if __name__ == '__main__':
    root_dir = determine_root_dir(sys.argv[1])
    console_outuput = False
    if ( len(sys.argv)>2 ):
        console_outuput = True
    
    exceptions_dir = '.known_errors/'
    item_type_list = ['casus_belli_groups',\
                      'effect_localization',\
                      'modifiers',\
                      'opinion_modifiers',\
                      'script_values',\
                      'scripted_effects',\
                      'scripted_modifiers',\
                      'scripted_triggers',\
                      'trigger_localization']
    errors_found = False
    for item_type in item_type_list:
        print('-------------------')
        print('Checking: '+item_type)
        exceptions_fname = exceptions_dir+item_type+cdi.exception_file_suffix+'.txt'
        test_error_found = cdi.run_test(root_dir,item_type,exceptions_fname,console_outuput)
        if ( not test_error_found ):
            print('No '+item_type+' issues found')
        errors_found |= test_error_found
        print('-------------------')
    
    if ( errors_found ):
        sys.exit(1)