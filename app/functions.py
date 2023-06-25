import re
import unicodedata
from glob import glob
from os import path
from flask import current_app
import csv
import re


BASEDIR = path.abspath(path.dirname(__file__))


#########################################
# SLUGIFY                               #
#########################################  
def slugify(value:str, allow_unicode:bool=False) ->str:
    """
    This function converts a string to a URL-friendly format by removing non-alphanumeric
    characters, converting spaces to dashes, and converting to lowercase.
    
    @param value The input string that needs to be slugified.
    @param allow_unicode A boolean parameter that determines whether non-ASCII characters should be
    allowed in the output or not. If set to True, non-ASCII characters will not be converted to their
    ASCII equivalents. If set to False, non-ASCII characters will be converted to their ASCII
    equivalents using the NFKD normalization form

    @return A string that has been converted to ASCII if `allow_unicode` is False, with spaces or
    repeated dashes converted to single dashes, non-alphanumeric characters removed, and converted to
    lowercase. The resulting string has leading and trailing whitespace, dashes, and underscores
    stripped.
    """
 
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())

    return re.sub(r'[-\s]+', '_', value).strip('-_')


#########################################
# GET DATA TYPE                         #
#########################################  
def get_data_types() ->list:
    """
    The function extracts a list of data types from the file names of CSV files located in a specific
    directory.
    
    @return A list. The first element of the list is a boolean value indicating whether the function
    executed successfully or not. The second element of the list is either a list of tuples containing
    the data type and its title extracted from the file names of CSV files located in a specific
    directory, or an empty list if no CSV files were found. If the function encountered an exception,
    the first element
    """

    try:
        data_type = [(path.splitext(path.basename(x))[0], path.splitext(path.basename(x))[0].title()) for x in glob(path.join(BASEDIR, *current_app.config["DATA_DIR"], "registry","*.csv"))]
        result = [True, data_type] if data_type else [True, []]
    except Exception as e:
        result = [False, repr(e)]

    return result


#########################################
# GET DATA FROM CSV                     #
#########################################  
def get_data_from_csv(csv_filename:str, target:str, run_reference:str=None) ->list:
    """
    This function reads data from a CSV file and returns a list based on the target and run reference
    provided.
    
    @param Csv_filename The name of the CSV file (without the .csv extension) that contains the data to
    be retrieved.
    @param Target The "target" parameter is a string that specifies the type of data to retrieve from
    the CSV file. It can be either "run-reference" or "run-configuration".
    @param Run_reference The reference for a specific run in the CSV file.
    
    @return A list with two elements. The first element is a boolean value indicating whether the
    function executed successfully or not. The second element is either a list of data (if the function
    executed successfully) or a string representation of the error that occurred during execution (if
    the function failed).
    """

    try:
        data = []
        
        CSVPATH = path.join(BASEDIR, *current_app.config["DATA_DIR"], "registry", csv_filename + ".csv")
        with open(CSVPATH) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                if target == "run-reference":
                    data.append([row[0], row[0].title()])
                if target == "run-configuration":
                    if row[0] == run_reference:
                        elems = row[1].split(",")
                        for elem in elems:       
                            data.append([elem, elem.title()])
        result = [True, data]
    except Exception as e:
        result = [False, repr(e)]
            
    return result

def get_images_basedirs(csv:str, run_reference:str, run_configuration:str, date:str) ->list:
    """ 
    """
 
    try:
        images_basedir = glob(path.join(BASEDIR, *current_app.config["DATA_DIR"], csv, run_reference, run_configuration, date + "*"))

        result = [True, images_basedir]
    except Exception as e:
        result = [False, repr(e)]
        
    return result

def list_images(dirs):
    """ 
    """
    
    try:
        all_imgs = [img.replace(BASEDIR, "") for d in dirs for img in glob( path.join(d, "*.png") )]
        return [True, all_imgs]
    except Exception as e:
        pass