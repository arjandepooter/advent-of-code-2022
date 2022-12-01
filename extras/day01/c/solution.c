#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    char *buffer;
    size_t size = 10;
    size_t chars;
    FILE *f = argc > 1 ? fopen(argv[1], "r") : stdin;

    buffer = malloc(size * sizeof(char));

    uint64_t top3[3] = {0, 0, 0};
    uint64_t block;

    while ((chars = getline(&buffer, &size, f)) != -1)
    {
        if (chars <= 1)
        {
            if (block > top3[0])
            {
                top3[2] = top3[1];
                top3[1] = top3[0];
                top3[0] = block;
            }
            else if (block > top3[1])
            {
                top3[2] = top3[1];
                top3[1] = block;
            }
            else if (block > top3[2])
            {
                top3[2] = block;
            }
            block = 0;
        }
        else
        {

            block += atoi(buffer);
        }
    }

    free(buffer);

    printf("Part 1: %lu\n", top3[0]);
    printf("Part 2: %lu\n", top3[0] + top3[1] + top3[2]);
}