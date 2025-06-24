#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// function to do the calculation
float run(char inp_string[]) {
    char *tokens[100];
    int token_count = 0;

    char *token = strtok(inp_string, " ");
    while (token != NULL) {
        tokens[token_count++] = token;
        token = strtok(NULL, " ");
    }

    int i = 0;
    while (i < token_count) {
        // Check if current token is an operator
        if (strcmp(tokens[i], "+") == 0 ||
            strcmp(tokens[i], "-") == 0 ||
            strcmp(tokens[i], "*") == 0 ||
            strcmp(tokens[i], "/") == 0) {

            // Get previous and next numbers
            float prev = atof(tokens[i - 1]);
            float next = atof(tokens[i + 1]);
            float result = 0.0;

            // Perform operation
            if (strcmp(tokens[i], "+") == 0)
                result = prev + next;
            else if (strcmp(tokens[i], "-") == 0)
                result = prev - next;
            else if (strcmp(tokens[i], "*") == 0)
                result = prev * next;
            else if (strcmp(tokens[i], "/") == 0)
                result = prev / next;

            // Shift tokens to remove old values
            char buffer[32];
            snprintf(buffer, sizeof(buffer), "%f", result);
            tokens[i - 1] = strdup(buffer);  // replace with result
            for (int j = i; j + 2 < token_count; j++) {
                tokens[j] = tokens[j + 2];
            }
            token_count -= 2;
            i = i - 1;  // move back

        } else {
            i++;
        }

        if (token_count == 1) break;
    }

    return atof(tokens[0]);
}

int main() {
    char input[] = "5 + 3 + 4 - 1";
    float output = run(input);
    printf("Result: %f\n", output);
    return 0;
}
