#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/stat.h>

#ifdef _MINIX
#include <lib.h>
#endif

#define NSAMPLES 4096
#define MAX_CYCLES 100000

extern unsigned rdtsc(void);

unsigned buf[NSAMPLES];

#ifdef _MINIX
void setup_process(int param) {
	message msg;

	msg.m1_i1 = getpid();
	msg.m1_i2 = group_no;

	return _syscall(MM, SETGROUP, &msg);
}
#else
void setup_process(int param) {}
#endif

int main(int argc, char **argv) {

	unsigned index;
	unsigned prev, val;
	int group_no;
	int i;
	int proc_no = 0;
	unsigned total_pause = 0, total_run = 0;
	int wrap_count = 0;
	FILE *out;
	char filename[100];

	index = 0;
	prev = rdtsc();

	/* wait for wraparound */
	while((val = rdtsc()) > prev) {
		prev = val;
	}

	while(argc > 1) {
		group_no = atoi(argv[1]);
		argc--;
		argv++;
		proc_no++;
		if(argc > 1 && fork() != 0) break;
	}
  setup_process(group_no);

	prev = rdtsc();

	buf[index++] = prev;
	while(index + 1 < NSAMPLES) {
		val = rdtsc();

		if(val < prev && ++wrap_count >= 5) {
			break;
		}

		if(val - prev > MAX_CYCLES) {
			buf[index++] = prev;
			buf[index++] = val;
		}
		prev = val;
	}

	buf[index++] = rdtsc();
	prev = buf[0];
  mkdir("data", 0777);
	sprintf(filename, "data/p%d.log", proc_no);
	out = fopen(filename, "w");
	for(i = 0; i < index; i+=2) {
		unsigned pause_time = buf[i] - prev;
		unsigned run_time = buf[i+1] - buf[i];
		fprintf(out, "%u %u\n", buf[i], buf[i+1]);

		prev = buf[i+1];

		total_run += run_time;
		total_pause += pause_time;
	}
	fclose(out);

	fprintf(stderr, "p=%d wraps=%d total run=%u pause=%u (run %.2f%%) total=%u %u\n",
			proc_no, wrap_count, total_run, total_pause, 
			(float) 100 * total_run / (total_run + total_pause),
			total_run + total_pause, buf[index-1] - buf[0]);
	return 0;
}
