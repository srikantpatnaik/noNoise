#!/usr/bin/python env

"""This script can be used to remove audio noise from 'ogv' videos. 
   
   Usage:(for future Srikant & all users)
  
   1)Remove noise from a single file:
   ----------------------------------
   $ python noNoise.py VideoWithNoise.ogv  CleanVideo.ogv
                         (source file)     (destination file)
                    
                        (OR)

   $ python noNoise.py VideoWithNoise.ogv  CleanVideo.ogv     0.21                      
                         (source file)     (destination file) (noise factor)  

   The third argument is optional(Noise factor). The scale spans from 
   0.0 to 1.0. Zero means no noise supression and 1.0 means full. The full
   scale is avoided. Best optimum result is found between 0.2 to 0.3. By default
   script will take 0.26. One can experiment with noise factor to get best noise
   free video. 
   NOTE: Careful, destination file will be overwritten if exist in given path.
   


   2)Remove noise from all files inside a directory:
   -------------------------------------------------
   $ python noNoise.py allNoisyFiles  allCleanFiles
                        (source dir)  (destination dir)

                        (OR)
                        
   $ python noNoise.py allNoisyFiles  allCleanFiles      0.21
                        (source Dir)   (destination dir) (Noise factor)


   NOTE: Please don't use any '/' after directory name. It will spit error.
   The fix is possible, but I don't want to spend time on it. This script is dirty
   but useful(atleast for me). When I find time, I will surely modify it. Meanwhile
   you all are welcome to add modifications. Please find this copy and future updates
   at http://github.com/srikantpatnaik.
   Thanks for your time.

   Details of each commands are in README.rst.
          
"""

from os   import system, path, listdir, chdir, mkdir
from sys  import argv
from time import sleep

def checkType():
    #Check for type of first argument(file or dir).
    if path.isdir(argv[1]):
        processDir()
    else:
        processFile()
    return


def processDir():
    #make dir to save all new files
    mkdir(argv[2])
    #cd to source dir   
    chdir(argv[1])
    for eachfile in listdir('.'):
        execute(setCommands(eachfile))
    return


def processFile():
    #Calling setCommands with source file.
    #Will return list of commands to be executed
    execute(setCommands(argv[1]))
    return
    

def execute(cli):     
    #total 7 commands with some delay for disk
    #write and sync    
    for each in cli:
        system(each)
        sleep(0.2)
    return    


def setCommands(filename):
     #The dirty function.        
     cli = [None]*7
     cli[0] = 'ffmpeg -i ' + ' ' + filename + ' -sameq -an ' + '.rawVideo.wmv'
     cli[1] = 'ffmpeg -i ' + ' ' + filename + ' -sameq ' + '.rawAudio.wav'
     cli[2] = 'sox .rawAudio.wav -t null /dev/null trim 0 0.5 noiseprof myprofile'
     #Checks for noise factor.
     if len(argv)>3:
         cli[3] = 'sox .rawAudio.wav .noisefree.wav noisered myprofile ' + argv[3]
     else:
         #The default value for noise factor is 0.26. Change accordingly.   
         cli[3] = 'sox .rawAudio.wav .noisefree.wav noisered myprofile 0.26'
     #Creating a less compressed file to retain video quality.
     cli[4] = 'ffmpeg -i .noisefree.wav -i .rawVideo.wmv -sameq .combined.wmv'
     #Checks for file or directory. If dir, the output is saved in different directory.
     if not path.isfile(argv[1]):
         cli[5] = 'ffmpeg2theora .combined.wmv -o ' + '../' + argv[2] + '/' + filename
     else:
         #Will create the final ogv video from wmv.
         cli[5] = 'ffmpeg2theora .combined.wmv -o ' + argv[2]
     cli[6] = 'rm .rawVideo.wmv .rawAudio.wav .noisefree.wav .combined.wmv myprofile'
     return cli



if __name__ == '__main__':
     checkType()
