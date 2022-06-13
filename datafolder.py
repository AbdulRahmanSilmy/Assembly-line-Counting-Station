import numpy as np
import os
import shutil

class datafolder():
  """
    A class that generates subfolders based on filename of the images

    ...


    Attributes
    ------------
    foldersource : str
      A string that contains the path of the folder containing source images.
    
    classes: list 
      A list of strings containing the classes expected to be present in the
      filename of images 


    Methods
    -----------
    generate()
      Generates the subfolders

    
  """
    
  def __init__(self,foldersource,classes):
      """
      Parameters
      ------------
      foldersource : str
        A string that contains the path of the folder containing source images.
    
      classes: list 
        A list of strings containing the classes expected to be present in the
        filename of images 
      """
      self.foldersource=foldersource
      self.classes=classes
    
    
  def generate(self):
      """
      Generates the subfolders
      """
      #create the mainfolder to place subfolders 
      if not os.path.exists('dataset'):
        os.mkdir('dataset')  

      for _class in self.classes:
          #filepath for the subfolders
          class_path=os.path.join('dataset',_class) 
          #create subfolder
          if not os.path.exists(class_path): 
            os.mkdir(class_path) 

      #build list of filenames from source folder     
      filenames = next(os.walk(self.foldersource), (None, None, []))[2]  
        
      for filename in filenames:
        for _class in self.classes:
          #look to see if filename contains a class
          if filename.endswith("_"+_class+".png"): 
            #copy the identified image from the source folder to the corresponding 
            #subfolder
            path_to_subfolder='dataset/'+_class+'/'+filename
            if not os.path.exists(path_to_subfolder):
              shutil.copyfile(self.foldersource+"/"+filename, path_to_subfolder)
            break
                 