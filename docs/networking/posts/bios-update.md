---
date:
  created: 2026-09-07
  updated: 2026-09-07
readtime: 6
pin: false
links:
  - Networking Index: networking/index.md
categories:
  - Homelab
tags:
  - HP Z210
  - BIOS
  - FreeDOS
  - Proxmox
authors:
  - robertovallado
slug: hp-z210-bios-update
---

# Updating the BIOS on an HP Z210 Workstation

How to take an HP Z210 from its original 2011 BIOS to the latest available version using a FreeDOS boot USB, plus the issues that came up along the way.

I had an old Z210 HP tower workstation that was given away at my work. Its been sitting arround for a while now, and I decided to give back life. It has generous space for storage and potentially help me as I learn about networking.

<!-- more -->

## Why Update

The Z210 shipped with BIOS J51 v01.20 from 2011. HP's last release for this board is v01.55 (2018), which updates the Intel microcode and includes mitigations for CVE 2018 3639 and CVE 2018 3640 (Spectre variant 4). 

>I thought this was cool info CVE's on hardware, not my jam but worth knowing none the less. 

Worth doing before running any hypervisor, since these are speculative execution issues that matter more once multiple VMs share the same CPU.

> **Note:** Worth knwoign that I have long ago installed a debian distro, therefore I will speak in Linux commands since it was easy to me this way. Find your current version under `File > System Information` in the F10 Setup Utility, or from a running Linux install with `sudo dmidecode -t bios`.


## What You Need

- The correct BIOS package for your exact model from HP's support site. Search ["HP Z210 Workstations System BIOS,"](https://support.hp.com/nz-en/drivers) Linux/DOS package. 
- A USB stick, 1GB or larger.
- A FreeDOS boot image. The official FreeDOS 1.4 Full USB image works well: `FD14-FullUSB.zip`, containing `FD14FULL.img`.

The HP package extracts to five files:

```
DOSFlash.exe
DOSFlash.txt
flshuefi.cpu
J51_0155.BIN
README.TXT
```

`DOSFlash.exe` is the flashing utility, `flshuefi.cpu` is its driver, and the `.BIN` file is the actual firmware image. They must all sit in the same folder for the tool to run.


## Building the Boot USB

Skip disk imaging tools built around ISOs; the FreeDOS image is a raw disk image, so it goes on with `dd`. A quick google search showed me that `dd` was the way to go.

Confirm `/dev/sdX` is actually the USB stick before running this; `dd` will happily overwrite the wrong disk.

```
lsblk -o NAME,SIZE,MODEL,TRAN
sudo dd if=FD14FULL.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```
It will take a bit to flash the USB and there is no output.

Once written, mount the resulting partition and copy the five HP files onto its root, next to the existing FreeDOS system files (`COMMAND.COM`, `KERNEL.SYS`, and so on):

```
cp DOSFlash.exe DOSFlash.txt flshuefi.cpu J51_0155.BIN README.TXT /run/media/user/FD14 FULL/
```

## Issues Encountered

A few things went wrong before landing on the process above, worth noting for anyone hitting the same walls.

**unetbootin's FreeDOS option produced a broken image.** It wrote its own bootloader (`ubninit`, `ubnkern`) but never bundled an actual FreeDOS kernel underneath, so the USB booted into nothing usable. Switching to the official FreeDOS image written with `dd` solved this cleanly.

**A stale download served the wrong file entirely.** An older reference pointed at a small standalone `balder10.img` hosted on a third party site; that host now serves its own unrelated 600MB Linux rescue ISO instead. Going straight to the official FreeDOS project distribution avoided this.

**The installer tried to install rather than boot to a prompt.** The Full USB image doubles as an installer, so its startup script offers to install FreeDOS to a hard disk. DO NOT ACCEPT! Pressing Escape at that screen dropped to a plain `C:\>` prompt instead, which is all that is needed to run `DOSFlash`.

**The mounted USB reported "busy" when ejecting.** A terminal session had its working directory set inside the mount point. `cd ~` in that terminal resolved it immediately.


## Running the Update

From the FreeDOS prompt, in the folder with all five files present:

```
dosflash
```

With no BIOS Setup password configured, this is enough. `DOSFlash` finds the `.BIN` file automatically, reports the current and target versions, and asks for confirmation before writing.

> **Note:** Do not interrupt power or remove the USB while it writes. A failed flash can leave the board unbootable.

After it reports success, reboot. Confirm the result from Linux:

```
sudo dmidecode -t bios
```

Should now report `Version: J51 v01.55`.

It was extremly brief, no internet connection needed and painless. I have read on reddit and blogs that BIOS update can go wrong easily and damage could potentially render hardware unuseable. So I was a bit scared but at the same time it was either that or just dump the machine. I dont particularly like wasting a good piece of technology so currently the tower is hosting my Proxmox server and hoping to get into the "nitti gridy" of server management and back-end development/operations the way is meant to be: "Hands on!", just like god intended. 


## After the Update

HP's release notes call out that crossing BIOS versions can leave stale boot menu entries, particularly around the USB hard drive placeholder. Clear this by entering F10 Setup and choosing `File > Apply Defaults and Exit`, then rebuild the boot order (drive order, storage devices excluded from boot as appropriate) from a clean state.


## References

- [HP Support: Z210 Workstation BIOS downloads](https://support.hp.com/nz-en/drivers)
- [FreeDOS Project](https://www.freedos.org/download/)
- [HP Community thread](https://h30434.www3.hp.com/t5/Business-PCs-Workstations-and-Point-of-Sale-Systems/how-to-update-bios-of-Z210/td-p/6205126) (url was broken but its easier to figure out and found the help very useful while researching)


