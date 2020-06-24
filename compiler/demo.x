#
#		Clear screen
#
clear.screen() {
	print.char($90);print.char(1);print.char($99);
	print.char(147);
}
#
#		Show object data via stdout
#
dump.object(addr) {
	print.hex(addr);print.char(':');
	print.hex(addr!0);
	print.hex(addr!2);
	print.hex(addr!4);
	print.hex(addr!6);
	print.char(13);
}
#
#		Draw character on screen
#
draw.char(addr,char) {
	var screen;screen = (addr!0 << 1)+(addr!2 << 8);
	!$9f20 = screen;?$9f22 = 16;
	?$9f23 = char;?$9f23 = addr?8;
}
#
#		Move character.
#
move.char(addr) {
	draw.char(addr,32);
	var x,y;x = addr!0+addr!4;y = addr!2+addr!6;
	if (y >= 60) { addr!6 = -(addr!6); }
	if (x >= 80) { addr!4 = -(addr!4); }
	addr!0=x;addr!2=y;
	draw.char(addr,42);
}
#
#		Random direction function
#
get.direction(ad) {
	var x;x = random()&1;
	if (x == 0) x = -1;
	!ad = x;
}
#
#		Create character.
#
create.char(addr) {
	var n1,n2;
	n1 = random();
	addr!0 = random()%80;
	addr!2 = random()%60;
	get.direction(addr+4);
	get.direction(addr+6);
	addr!8 = (random()%15)+1;
}

var mem[2048];

main() {
	clear.screen();
	var count,a;
	count = 100;
	do (count,a) { 
		create.char(a<<4+mem);
		draw.char(a<<4+mem,42);
	}
	do (110) {
		do (count,a) {
			move.char(mem+a<<4);
		}
	}
}