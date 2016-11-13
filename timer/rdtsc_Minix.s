.sect .text

.define _rdtsc
_rdtsc:
	! CPUID
	.data1 0x0f
	.data1 0xa2

	! RDTSC
	.data1 0x0f
	.data1 0x31

	ret
