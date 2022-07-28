#!/usr/bin/env python
# coding=utf-8
import os
import subprocess

import click


@click.command()
@click.argument('kernel', default="kernel.bin", type=click.Path(exists=True))
@click.argument('rootfs', default="rootfs.bin", type=click.Path(exists=True))
@click.argument('driver', default="driver.bin", type=click.Path(exists=True))
@click.argument('appfs', default="appfs.bin", type=click.Path(exists=True))
@click.argument('outfile', default="demo_5.5.1.177.bin")
def cli(kernel, rootfs, driver, appfs, outfile):
    dic = [
        ("kernel", 0x200000, click.format_filename(kernel)),
        ("rootfs", 0x350000, click.format_filename(rootfs)),
        ("driver", 0xa0000, click.format_filename(driver)),
        ("appfs", 0x4a0000, click.format_filename(appfs)),
    ]
    outfile = click.format_filename(outfile)
    tmpfile = "tmp.bin"
    fullflash = open(tmpfile, 'wb')
    for name, size, filename in dic:
        buffersize = os.path.getsize(filename)
        if size < buffersize:
            click.echo(
                f'Size mismatch. The provided {name} has a size of {buffersize}, but it need to have the size {size}. Please try to free some space!'
            )

            return

        part = open(filename, "rb")
        buffer = part.read(size)
        fullflash.write(buffer)
        # Padding with zeros:
        if buffersize < size:
            padsize = size - buffersize
            for _ in range(padsize):
                fullflash.write(bytearray.fromhex('00'))

    cmd = f"mkimage -A MIPS -O linux -T firmware -C none -a 0 -e 0 -n jz_fw -d {tmpfile} {outfile}"


    subprocess.check_output(cmd, shell=True)

    os.remove(tmpfile)

    click.echo(f'Firmware {outfile} was successfully created!')


if __name__ == '__main__':
    cli()
