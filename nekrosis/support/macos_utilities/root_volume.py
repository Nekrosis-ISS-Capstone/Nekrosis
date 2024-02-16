"""
root_volume.py: macOS-specific root volume logic.
"""

import plistlib
import platform
import subprocess

from pathlib import Path

from .os_versioning import XNUVersions
from ..error_wrapper import SubprocessErrorLogging


BIN_MOUNT:    str = "/sbin/mount"
BIN_UMOUNT:   str = "/sbin/umount"
BIN_BLESS:    str = "/usr/sbin/bless"
BIN_DISKUTIL: str = "/usr/sbin/diskutil"


class RootVolume:

    def __init__(self) -> None:
        self.xnu_version = int(platform.release().split(".")[0])
        self.root_volume_identifier = self._fetch_root_volume_identifier()


    def mount(self) -> str:
        """
        Mount the root volume.

        Returns the path to the root volume.
        """
        return self._mount_root_volume()


    def unmount(self) -> None:
        """
        Unmount the root volume.
        """
        self._unmount_root_volume()


    def _fetch_root_volume_identifier(self) -> str:
        """
        Resolve path to disk identifier

        ex. / -> disk1s1
        """
        try:
            content = plistlib.loads(subprocess.run([BIN_DISKUTIL, "info", "-plist", "/"], capture_output=True, text=True).stdout.encode("utf-8"))
        except plistlib.InvalidFileException:
            raise RuntimeError("Failed to parse diskutil output.")

        disk = content["DeviceIdentifier"]

        if "APFSSnapshot" in content and content["APFSSnapshot"] is True:
            # Remove snapshot suffix (last 2 characters)
            # ex. disk1s1s1 -> disk1s1
            disk = disk[:-2]

        return disk


    def _mount_root_volume(self) -> str:
        """
        Mount the root volume.

        Returns the path to the root volume.
        """
        # Root volume same as data volume
        if self.xnu_version < XNUVersions.CATALINA.value:
            return "/"

        # Catalina implemented a read-only root volume
        if self.xnu_version == XNUVersions.CATALINA.value:
            result = subprocess.run([BIN_MOUNT, "-uw", "/"], capture_output=True, text=True)
            if result.returncode != 0:
                SubprocessErrorLogging(result).log()
                raise RuntimeError(f"Failed to mount root volume")
            return "/"

        # Big Sur and newer implemented APFS snapshots for the root volume
        if self.xnu_version >= XNUVersions.BIG_SUR.value:
            if Path("/System/Volumes/Update/mnt1/System/Library/CoreServices/SystemVersion.plist").exists():
                return "/System/Volumes/Update/mnt1"
            result = subprocess.run([BIN_MOUNT, "-o", "nobrowse", "-t", "apfs", f"/dev/{self.root_volume_identifier}", "/System/Volumes/Update/mnt1"], capture_output=True, text=True)
            if result.returncode != 0:
                SubprocessErrorLogging(result).log()
                raise RuntimeError(f"Failed to mount root volume")
            return "/System/Volumes/Update/mnt1"

        # Shouldn't hit this, but keep for future development
        raise NotImplementedError(f"XNU version {self.xnu_version} not supported.")


    def _unmount_root_volume(self) -> None:
        """
        Unmount the root volume.
        """
        if self.xnu_version < XNUVersions.CATALINA.value:
            return

        if self.xnu_version == XNUVersions.CATALINA.value:
            result = subprocess.run([BIN_MOUNT, "-ur", "/"], capture_output=True, text=True)
            if result.returncode != 0:
                SubprocessErrorLogging(result).log()
                raise RuntimeError(f"Failed to unmount root volume")
            return

        if self.xnu_version >= XNUVersions.BIG_SUR.value:
            commands = []
            if platform.machine() == "arm64":
                commands.append([BIN_BLESS, "--mount", "/System/Volumes/Update/mnt1", "--create-snapshot"])
            else:
                commands.append([BIN_BLESS, "--folder", "/System/Volumes/Update/mnt1/System/Library/CoreServices", "--bootefi", "--create-snapshot"])
            commands.append([BIN_UMOUNT, "/System/Volumes/Update/mnt1"])

            for command in commands:
                result = subprocess.run(command, capture_output=True, text=True)
                if result.returncode != 0:
                    SubprocessErrorLogging(result).log()
                    raise RuntimeError(f"Failed to unmount root volume")
            return

        raise NotImplementedError(f"XNU version {self.xnu_version} not supported.")