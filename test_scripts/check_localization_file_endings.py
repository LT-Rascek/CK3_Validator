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

OR

./MOD/
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

Example run command: "python3 ./CK3_Validator/test_scripts/check_localization_file_endings.py MY_MOD_NAME"
'''

''' License: BSD Zero Clause
Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN
AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
OF THIS SOFTWARE.
'''

exception_file_suffix = '_localization_ending_exceptions'

class CheckFileName:
    '''
      file: the file we're cehcking
      returns: None if properly formatted, file name if improperly formatted
    Desc
      Pulls the list of items from the database folder
    '''
    def action(self,file):
        fname = os.path.basename(file)
        
        english_ending = '_l_english.yml'
        french_ending = '_l_french.yml'
        german_ending = '_l_german.yml'
        korean_ending = '_l_korean.yml'
        russian_ending = '_l_russian.yml'
        simp_chinese_ending = '_l_simp_chinese.yml'
        spanish_ending = '_l_spanish.yml'
        
        if ( fname[-len(english_ending):] == english_ending or \
             fname[-len(french_ending):] == french_ending or \
             fname[-len(german_ending):] == german_ending or \
             fname[-len(korean_ending):] == korean_ending or \
             fname[-len(russian_ending):] == russian_ending or \
             fname[-len(simp_chinese_ending):] == simp_chinese_ending or \
             fname[-len(spanish_ending):] == spanish_ending ):
            return [None]
        else:
            return [fname]

def run_test(root_dir,item_type,exceptions_fname,console_output=False):
    errors_found = False
    #Load the list of exceptions if we have it
    exception_list = []
    if ( os.path.isfile(exceptions_fname) ):
        exception_list = load_exceptions_list(exceptions_fname)
    else: print('Note: exceptions file not found')
    #Get the list of all items in the database requested
    if(console_output): print('Building Database')
    file_ending_check = CheckFileName()
    item_list = search_over_mod_structure(root_dir,item_type,file_ending_check,[],console_output,\
                                          database=['localization'],\
                                          check_localization=True)
    if(console_output): print('\n')
    #Remove None instances
    item_list = [x for x in item_list if x]
    if(console_output): print('\n')
    #Summary:
    if ( len(item_list)>0 ):
        errors_found = True
        print('Improperly Ended Localization Files:\n'+str(item_list))
    return errors_found

if __name__ == '__main__':
    root_dir,item_type,exceptions_fname = console_input_parsing(exception_file_suffix)
    
    errors_found = run_test(root_dir,item_type,exceptions_fname,console_output=False)
    
    common_exit(errors_found,'localization files ending')
