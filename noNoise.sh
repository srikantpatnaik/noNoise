#!/bin/bash

# Please install 'libav-tools' for Ubuntu 14.04 onwards
# As ffmpeg is obsolete, it has been replaced by 'avconv'
# Instead of python script, a simple bash one is sufficient

# A beta release for noNoise-v2

# Usage example
# $ bash noNoise.sh noisyVideo.mp4 noise-reduction-factor
							
# noise-reduction-factor: 0 means no reduction, 1 means 
# maximum damping of noise (recommended is 0.2 to 0.4)



# Making a backup of the original video
echo "Back up original video at  /tmp/orig_$1"
cp -v $1 /tmp/orig_$1

# Extracting audio from noisyVideo
avconv -i $1 -f wav -ab 192000 -vn /tmp/noisy.wav

# Creating a noise profile, basically looking for white noise
# in 0 to 0.5 sec of the clip (change if you like)
sox /tmp/noisy.wav -n trim 0 0.5  noiseprof myprofile

# Removing noise using noise profile
sox /tmp/noisy.wav /tmp/noisefree.wav noisered myprofile $2

# Replacing noisyAudio with noisefree audio in original video
avconv -i $1 -i /tmp/noisefree.wav -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 noisefree_$1.mp4
