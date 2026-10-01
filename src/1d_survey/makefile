all: riemann main
	gcc main.o riemann.o -O3 -lm -o test.run
main:
	gcc main.c -O3 -lm -c
riemann:
	gcc riemann.c -O3 -lm -c
