import sys
import os
import check_database_item as cdi

if __name__ == '__main__':
    # root_dir needs a trailing slash (i.e. /root/dir/)
    root_dir = ''
    if ( os.path.isdir(sys.argv[1]) ):
        print('No folder named '+str(sys.argv[1])+' exists; stopping execution')
        sys.exit(1)
    else:
        root_dir = sys.argv[1]
        
    exceptions_dir = '.known_errors/'
    item_type_list = ['script_values','scripted_triggers','scripted_effects']
    errors_found = False
    for item_type in item_type_list:
        exceptions_fname = exceptions_dir+item_type+cdi.exception_file_suffix+'.txt'
        test_error_found = cdi.run_test(root_dir,item_type,exceptions_fname)
        if ( not test_error_found ):
            print('No '+item_type+' issues found')
        errors_found |= test_error_found
    
    if ( errors_found ):
        sys.exit(1)