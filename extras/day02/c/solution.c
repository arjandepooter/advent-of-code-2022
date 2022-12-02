#include <stdio.h>
#include <stdlib.h>

#define BUF_SIZE 0x10 << 20

static char buf[BUF_SIZE];

int main(int argc, char **argv)
{
    int score_1 = 0;
    int score_2 = 0;
    size_t len;
    FILE *f = argc > 1 ? fopen(argv[1], "r") : stdin;

    while ((len = fread(buf, 1, sizeof(buf), stdin)) != 0)
    {
        for (char *ch = buf, *end = buf + len; ch != end; ch += 4)
        {
            int a = *ch - 'A';
            int b = *(ch + 2) - 'X';

            score_1 += 1 + b + 3 * ((4 + b - a) % 3);
            score_2 += 3 * b + 1 + ((a + b + 2) % 3);
        }
    }

    printf("%d\n", score_1);
    printf("%d\n", score_2);

    return 0;
}