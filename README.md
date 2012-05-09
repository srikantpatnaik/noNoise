Introduction
============
With home made videos or screencasts, we often find a constant noise in our recording due to electric wiring, fan, choke coil of fluorescent
lamp etc. This could be  irritating.But fortunately, these noises can be easily detected and can be removed with GUI based tools, such as 
Audacity.
To use any GUI based tool, we need to extract audio manually and then feed it to the software, once done we have to again join the noisefree
audio with the video. This is OK with 1 or 2 files. But to for automating each step and to handle multiple files we need a simple script.

One can simply use `sox` and `ffmpeg` commands shown below in given order to get the same result(see `Working`).



Required packages
-----------------

 *  sox

 * ffmpeg

 * ffmpeg2theora

 * libmp3lame0

 * Linux machine with default python 



Usage
-----

### Remove noise from a single file

    
      $ python noNoise.py VideoWithNoise.ogv  CleanVideo.ogv
                            (source file)     (destination file)
                    
(OR)

      $ python noNoise.py VideoWithNoise.ogv  CleanVideo.ogv     0.21
                            (source file)     (destination file) (noise factor)  

   The third argument is optional(Noise factor). The scale spans from 
   `0.0` to `1.0`. Zero means no noise supression and 1.0 means full. The full
   scale is avoided. Best optimum result is found between `0.2` to `0.3`. By default
   script will take `0.26`. One can experiment with noise factor to get best noise
   free video. 
   NOTE: Careful, destination file will be overwritten if exist in given path.
   


### Remove noise from all files inside a directory

      
      $ python noNoise.py allNoisyFiles  allCleanFiles
                            (source dir)  (destination dir)

(OR)
                        
      $ python noNoise.py allNoisyFiles  allCleanFiles      0.21
                          (source Dir)   (destination dir) (Noise factor)

NOTE: Please don't use any '/' after directory name. It will spit error.
The fix is possible, but I don't want to spend time on it. This script is dirty
but useful(atleast for me). When I find time, I will surely modify it. Meanwhile
you all are welcome to add modifications.



Working:
-------
###1. Extracting video in less compressed format

        ffmpeg -i 1.ogv -sameq -an 2.wmv 
   
   Extracting video in wmv format for easy editing(less compressed
   than mp4,ogv,avi). We can leave the video intact and combine the
   noiseless audio later to it, but it will hamper the video quality
   of the newly joined video.
   The size of this 'wmv' will be approximately 5 times than that of
   original 'ogv' video.
   

###2. Extracting audio in less compressed format
   
        ffmpeg -i 1.ogv -sameq 2.wav
   
   Extracting audio in wav format for fast & easy editing.The size of the
   `wav` audio file will be approximately 8 times larger than the original.


###3. Getting noise profile
        
        sox 2.wav -t null /dev/null trim 0 0.5 noiseprof myprofile
   
   Creating a noise profile of original audio at 0 to 0.5 second.
   One can change this duration if required. In most cases the
   standard noise is evenly distributed throughout the recording(eg: 
   fan, PC etc), so the default 0 to 0.5 value will do the trick.

###4. Converting audio according to noise profile
    
       sox 2.wav 2-noisefree.wav noisered myprofile 0.26

   Creating a noisefree audio based on our noise profile. The value 
   `0.26` is important. This is scale for noise removal. 0 means no removal
   and 1 means full removal. The full removal will supress most of the
   orginal audio too. So as per my R&D, I found `0.26` to be most optimized
   one for noise removal.

   
###5. Combining back audio and video
   
       ffmpeg -i 2-noisefree.wav -i 2.wmv -sameq vid.wmv

   Merging new noiseless audio and old video together.


###6. Final conversion
       
       ffmpeg2theora vid.wmv -o vid.ogv

   Now converting wmv into our favorite ogv format. This will create a 
   `vid.ogv` of almost same size that of original video.


License
-------
GNU GPLV3
