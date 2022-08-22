import sys
import os
import check_encoding_item as cei

if __name__ == '__main__':
    # root_dir needs a trailing slash (i.e. /root/dir/)
    root_dir = ''
    if not os.path.isdir( './'+str(sys.argv[1])+'/' ):
        print('No folder named '+str(sys.argv[1])+' exists; stopping execution')
        sys.exit(1)
    else:
        root_dir = sys.argv[1]
    
    console_outuput = False
    if ( len(sys.argv)>2 ):
        console_outuput = True
    
    exceptions_dir = '.known_errors/'
    item_type_list = ['.+']
    errors_found = False
    for item_type in item_type_list:
        exceptions_fname = exceptions_dir+'all'+cei.exception_file_suffix+'.txt'
        test_error_found = cei.run_test(root_dir,item_type,exceptions_fname,console_outuput)
        if ( not test_error_found ):
            print('No encoding issues found')
        errors_found |= test_error_found
    
    if ( errors_found ):
        sys.exit(1)