# Nao Project
## Dependencies
### General
* Python Development Files
* PortAudio Development Files
* Atlas Development Files
* SWIG
### apt

`apt-get install portaudio19-dev python-all-dev libatlas-base-dev swig` 
### yum

`yum install python-devel portaudio-devel-19 atlas-devel swig`

## Problems
### Recognizer
If you are facing any issues with the recognizer please generate a custom SWIG interface for snowboy.
Checkout their GitHub Repository for instructions. Afterwards copy snowboydetect.py and _snowboydetect.so into
the misc directory.

