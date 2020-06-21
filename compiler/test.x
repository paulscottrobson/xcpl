var n;

define c.to.print 	"41"
star() {
	print.char(42);
}
double(cz) {
	print.char(cz);print.char(cz);
}
star2() { star();star();double(64); }

twoChar(c1,c2) { print.char(c1);print.char(c2); }

lotsChar(n,c) { do(n) { print.char(c); } }

main() {
	do(40,n) {
	lotsChar(n+1,c.to.print);
	print.char(13); }
}