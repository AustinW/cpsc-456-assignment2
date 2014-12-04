/*****************************
 * Author: Austin White
 * Email: austinw@csu.fullerton.edu
 * Class: CPSC 456
 * Professor: Mikhail Gofman
 * Assignment: #2
 * Date: November 30, 2014
 */

#include "codearray.h"
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/wait.h>
#include <sys/stat.h>

using namespace std;

bool DEBUG = false;

int main()
{
	
	// The child process id
	pid_t childProcId = -1;
		
	// Go through the binaries
	for (int progCount = 0; progCount < NUM_BINARIES; ++progCount)
	{
			
		// Create a temporary file you can use the tmpnam() function for this.
		char templateName[] = "/tmp/binderXXXXXX";
		char* fileName = mktemp(templateName);
		
		// Open the file and write the bytes of the first program to the file.
		// These bytes are found in codeArray[progCount]
		FILE* fp = fopen(fileName, "wb");

		if ( ! fp) {
			perror("fopen");
			exit(-1);
		}

		if (fwrite(codeArray[progCount], sizeof(char), programLengths[progCount], fp) != programLengths[progCount]) {
			perror("fwrite");
			exit(-1);
		}

		fclose(fp);
		
		// Make the file executable: this can be done using chmod(fileName, 0777)
		chmod(fileName, 0777);
		
		// Create a child process using fork
		childProcId = fork();

		// I am a child process; I will turn into an executable
		if (childProcId == 0)
		{
			// Use execlp() in order to turn the child process into the process
			// running the program in the above file.
			printf("Filename: %s", fileName);
			if (execlp(fileName, fileName, NULL) < 0) {
				perror("execlp");
				exit(-1);
			} else {
				fprintf(stderr, "Fork failed\n");
				exit(-1);
			}
		}
	}

	// Wait for all programs to finish
	for (int progCount = 0; progCount < NUM_BINARIES; ++progCount)
	{
		// Wait for one of the programs to finish
		if (wait(NULL) < 0)
		{
			perror("wait");
			exit(-1);
		}
	}
}