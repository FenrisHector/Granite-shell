#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_INPUT_SIZE 1024
#define MAX_CMD_SIZE 2048

// Color definitions
#define COLOR_GREEN "\033[1;32m"  // Prompt in green
#define COLOR_CYAN  "\033[1;36m"  // AI response in cyan
#define COLOR_RESET "\033[0m"     // Reset color

int main() {
    char input[MAX_INPUT_SIZE];
    char python_command[MAX_CMD_SIZE];
    char ai_response[MAX_INPUT_SIZE];

    // Clear the console
    system("cls");

    printf("------------------------------------------\n");
    printf("   THE GRANITE SHELL (FAST MODE)          \n");
    printf("------------------------------------------\n\n");

    while (1) {
        // Prompt
        printf(COLOR_GREEN "granite-shell > " COLOR_RESET);

        // Reads input from the user and process it in the Granite Shell program.
        if (fgets(input, MAX_INPUT_SIZE, stdin) == NULL) break;
        input[strcspn(input, "\n")] = 0;

        if (strcmp(input, "exit") == 0) break;
        if (strlen(input) == 0) continue;

        // Construct the system command to invoke the Python brain safely
        snprintf(python_command, sizeof(python_command), "python bridge/brain.py \"%s\"", input);

        // Open a pipe to the Python process in read mode
        FILE *fp = popen(python_command, "r");
        if (fp == NULL) continue; // Skip if process creation fails

        // Capture the AI's output and strip the trailing newline character
        if (fgets(ai_response, sizeof(ai_response), fp) != NULL) {
            ai_response[strcspn(ai_response, "\n")] = 0;

            // 2. AI Response
            printf(COLOR_CYAN "   >> %s" COLOR_RESET "\n", ai_response);

            system(ai_response);
            printf("\n");
        }
        pclose(fp);
    }
    return 0;
}
