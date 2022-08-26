import sys
import os

from ck3_common_utils import search_over_mod_structure
from ck3_common_utils import load_exceptions_list
from ck3_common_utils import remove_exceptions_list
from ck3_common_utils import console_input_parsing
from ck3_common_utils import common_exit

'''
Searches your CK3 mod to see if *.txt and *.yml files are encoded properly

Will throw a failure when:
    A file is not encoded in UTF-8-BOM

Meant to be launched from your top level git folder with structure

i.e., ./MOD/, where

./MOD/
    |- MOD/
        |- common/
        |- events/
        |- gfx/
        |- gui/
        |- localization
        |- music/

is the expected sort of underlying structure. Will need some tweaks to run under other directory structures.

Arg 1 is mod folder name

Arg 2 is the locations of your exceptions file (e.g., things you overwrite from Vanilla that might not
have references in your codebase). By default, it looks at:
./MOD/.known_errors/<item_type>_database_exceptions.txt

Example run command: "python3 ./CK3_Validator/test_scripts/check_database_item.py MY_MOD_NAME"
'''

''' License: BSD Zero Clause
Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN
AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
OF THIS SOFTWARE.
'''

exception_file_suffix = '_utf8_exceptions'

#Wrapper Class for building a list of items for which to search the database
class CheckFileEncoding:
    BOM = '\ufeff'
    '''
      dir_name: Directory we're search
    Desc
      Pulls the list of items from the database folder
      
      Borrowed from:
        https://stackoverflow.com/questions/3269293/how-to-write-a-check-in-python-to-see-if-file-is-valid-utf-8
    '''
    def action(self,file):
        with open(file,'r') as file_obj:
            try:
                text = file_obj.read()
                if not text.startswith(self.BOM):
                    return [file]
            except UnicodeDecodeError:
                return [file]
        return [None]

def run_test(root_dir,item_type,exceptions_fname,console_output=False):
    errors_found = False
    #Load the list of exceptions if we have it
    exception_list = []
    if ( os.path.isfile(exceptions_fname) ):
        exception_list = load_exceptions_list(exceptions_fname)
    else:
        print('Note: exceptions file not found')
    #Get the list of all items in the database requested
    if(console_output): print('Building Database')
    file_encoding_check = CheckFileEncoding()
    item_list = search_over_mod_structure(root_dir,item_type,file_encoding_check,[],console_output,check_localization=True)
    if(console_output): print('\n')
    #Remove None instances
    item_list = [x for x in item_list if x]
    if(console_output): print('\n')
    #Summary:
    if ( len(item_list)>0 ):
        errors_found = True
        print('Improperly Encoded Files:\n'+str(item_list))
    return errors_found

if __name__ == '__main__':
    root_dir,item_type,exceptions_fname = console_input_parsing(exception_file_suffix)
    
    errors_found = run_test(root_dir,item_type,exceptions_fname,True)
    
    common_exit(errors_found,item_type)
