Austin White
austinw@csu.fullerton.edu
CPSC 456 Section 2
Monday, November 24, 2014
Assignment 2

PART I

C:\Users\AustinVM\Downloads\cpsc456-assignment2> copy /b "Screen Shot 2014-11-23
at 10.31.11 PM.png" + sample.zip result
Screen Shot 2014-11-23 at 10.31.11 PM.png
sample.zip
        1 file(s) copied.

Rename the result file to result.zip (i.e. append the zip extension). Try opening the file. What happens?
Windows returns the error: Windows cannot open the folder, the compressed zip folder is invalid.


Now rename the above file to have a .png extension. Try opening the file. What happens?
 The image opens in the default picture viewer

Explain what is happening. Do some research in order to find out what the above copy command does. In your explanation be sure to explain the role of each argument in the above command. Also, be sure to explain how Windows handles files which leads the above behavior.
COPY source1 + source2.. destination [options]
Windows' copy command copies one or more files to another location. The /b option copies the files in binary mode, simply merging the two files' bits together into a single file. Windows handles opening files by observing their specified extension and opening it with the program that has been assigned to handle the extension.

How can this technique be used for hiding malicious codes?
As we've just seen, the file opens without issue, however contains additional bytes belonging to the zip file. If we inject malicious byte instructions instead using, for instance, a buffer overflow attack, we can hijack the executable and bend it to our will.

How robust is this technique when in terms of avoiding detection by anti-virus tools?
On its own, this method is not very robust at all. Because anti-virus softwares use signatures to scan for malware, the malicious code injected will most likely be detected. To avoid detection, the malicious byte payload should be encoded with a tool such as Metasploit's msfencode. 
Source: http://www.admin-magazine.com/Articles/How-to-Hide-a-Malicious-File

PART II