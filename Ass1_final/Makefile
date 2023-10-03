obj-m += chardev.o
all:
	sudo make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
clean:
	sudo make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
test:
	-sudo rmmod chardev
	sudo dmesg -C  
	sudo insmod chardev.ko
	dmesg	
