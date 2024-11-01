#!/bin/bash

/usr/bin/qemu-system-x86_64 \
    -kernel ./bzImage \
    -initrd ./initramfs.cpio.gz \
    -cpu kvm64,+smep,+smap \
    -nographic \
    -monitor none \
    -append "console=ttyS0 nokaslr panic=1" \
    -no-reboot \
    -s


