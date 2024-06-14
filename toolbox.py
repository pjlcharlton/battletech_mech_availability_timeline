# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 15:58:11 2024

Toolbox of useful python functions created by me or found around the internet.

@author: pjlch
"""

import os, shutil

def cleanup_folder(folder):
    """
    Delete everything in the provided folder, use with care!
    
    Source: https://stackoverflow.com/a/185941
    
    Parameters
    ----------
    folder : str
        Path to folder to clean up
    """
    
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            
def create_folder(foldername):
    """
    Generate a folder with provided foldernme, but remove it if it exists, first
    
    Parameters
    ----------
    foldername : string
        Desired name for created folder.
    """
    
    if os.path.exists(foldername): 
        os.remove(foldername)
    os.mkdir(foldername)