# S.T.A.R. (Speech-to-Text Analytic Resource)

S.T.A.R. is a user friendly interface which allows an Instructor to retrieve analytics from recorded lectures. 

The current analytics that are calculated by S.T.A.R. are:

- Average Wait Time

- Average time given for Clarification Pauses

The two main objectives of S.T.A.R. is:

- Give the less computer savy users an easy downloadable file with an intuitive user interface...

- Give the inquistive programmer the ablilty to replace the CMU Sphinx API with any of their choosing (instructions for this adaptation is given later)

With these goals in mind we have created two versions of the S.T.A.R. program:

- S.T.A.R. JAVA

- S.T.A.R. Python

The Python version is written using a few public  of libraries which makes it's installation more taxing on the educator that is less familiar with programing, while the version written with Java has only the dependicy of java and as such can be used across platforms with no programming understanding, yet this makes the program a lot less versitile with a lot less features.

## Getting Started

These instructions will help you get a version of S.T.A.R. up and running on your local machine for basic use, development or testing purposes. 

Supported Platforms
-------------------

- Windows 7
- Windows 8
- Windows 10
- Ubuntu 14.10

Installing (JAVA VERSION) on Windows
------------------ 
To install the Java version of S.T.A.R. one only needs to download the .jar file from the folder with the correct operating system.
For example if you are using a Windows machine you need to open the Java_Windows folder from this GIT-repository and download the .jar file.




Installing (PYTHON VERSION) on Windows
------------------
S.T.A.R. is written using a few public libraries which do a lot of audio processing and in the advanced settings uses a CMU website to load a language model. To download all of these dependicies one only needs a passing familiarity with the use of command line (DOS). 




### Dependencies/Libraries

- [Python 2.7](https://www.python.org/download/releases/2.7/)
- [CMU PocketSphinx](https://github.com/cmusphinx/pocketsphinx-python)
- [pydub](https://pypi.org/project/pydub/)
- [ffmpeg](https://www.ffmpeg.org/)
- [mechanize](https://pypi.org/project/mechanize/)
- [easyGUI](https://pypi.org/project/easygui/)



Downloading Python 2.7
------------------
The primary language in which S.T.A.R. is written is Python. It was written using Python 2.7 and it is recommended that this version is the one used to run it. We recommend using the link: [Python 2.7](https://www.python.org/download/releases/2.7/) and downloading the package from one of the links on the official page. You can install this program anywhere on your computer, yet for the further steps please make note of where you saved this package. (For example it could be saved in C:\Program Files\Python27\)



Using PIP
------------------
To use the further dependencies we suggest using [pip](https://pypi.python.org/pypi/pip/)



