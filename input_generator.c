#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// RANDOM RANGE

int random_range(int min, int max) {

    return rand() %

           (max - min + 1)

           + min;
}


int main() {

    FILE *fp =
        fopen("builds/input.txt", "w");

    if (!fp) {

        perror("File error");

        return 1;
    }

    srand(time(NULL) ^ clock());


    int maxCPU = 400;

    int maxRAM = 1000;

    int maxStorage = 4000;

    int maxBW = 1000;

    fprintf(fp,

            "%d %d %d %d\n",

            maxCPU,
            maxRAM,
            maxStorage,
            maxBW);

    // NUMBER OF JOBS

    int n = 10000;

    fprintf(fp, "%d\n", n);

    // JOB GENERATION

    for (int i = 0; i < n; i++) {

        int cpu;
        int ram;
        int storage;
        int bw;

        int type =
            random_range(1, 100);

        // LIGHT JOBS

        if (type <= 50) {

            cpu =
                random_range(1, 4);

            ram =
                random_range(2, 16);

            storage =
                random_range(20, 120);

            bw =
                random_range(5, 30);
        }

        // MEDIUM JOBS

        else if (type <= 90) {

            cpu =
                random_range(4, 12);

            ram =
                random_range(16, 64);

            storage =
                random_range(120, 400);

            bw =
                random_range(30, 120);
        }

        // HEAVY JOBS

        else {

            cpu =
                random_range(12, 32);

            ram =
                random_range(64, 180);

            storage =
                random_range(200, 700);

            bw =
                random_range(120, 300);
        }

        // TIMING

        int arrival =
            random_range(0, n / 10);

        int duration =
            random_range(2, 15);

        int priority =
            random_range(1, 5);

        // REVENUE

        int revenue =

            cpu * 20 +

            ram * 6 +

            storage / 8 +

            bw * 4 +

            random_range(-200, 400);

        if (revenue < 50)
            revenue = 50;

        fprintf(fp,

                "%d %d %d %d %d %d %d %d\n",

                cpu,
                ram,
                storage,
                bw,

                revenue,

                arrival,
                duration,
                priority);
    }

    fclose(fp);

    return 0;
}