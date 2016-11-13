.section .text

.globl rdtsc
rdtsc:
	cpuid
	rdtsc
	ret
