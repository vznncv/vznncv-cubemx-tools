#!/usr/bin/env bash
# helper script to upload compiled application to microcontroller using OpenOCD

build_dir="{{ build_dir }}"
openocd_script="openocd_stm.cfg"

elf_target=$(find "$build_dir" -maxdepth 1 -name "*.elf" | head -n1)
if [ ! -f "$elf_target" ]; then
	echo "Cannot find elf file." 1>&2
	exit 1
fi

echo "OpenOCD config: $openocd_script" 1>&2
echo "elf file: $elf_target" 1>&2
echo "Flush ..." 1>&2
openocd --file "$openocd_script" --command "program \"${elf_target}\" verify reset exit"
echo "Complete" 1>&2
