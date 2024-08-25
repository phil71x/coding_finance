By following these instructions, you'll have a smooth and organized process for cloning an SSD used in a server running Bitcoin and LND services. Remember, throughout this process, your data's integrity is paramount, so ensure you have a solid backup before beginning. It will take less than one hour to clone 1TB of data with USB3 port. Prerequiste: a SSD enclosure


### Preparing for Cloning

1. **Stop Bitcoin and LND Services**: 
   - Prevent database corruption and ensure data consistency by stopping the Bitcoin and LND services.
   ```bash
   sudo systemctl stop bitcoind
   sudo systemctl stop lnd
   ```

2. **Backup Data**: 
   - Create backups of all critical data on the source SSD to prevent potential data loss.

3. **Identify Drives**:
   - Use `lsblk` or `fdisk -l` to determine the device names of your source SSD and the USB-connected destination SSD.
   - Assume `/dev/sdx` is your source and `/dev/sdy` is your destination SSD.

4. **Unmount Source Drive**:
   - If the source SSD is mounted, unmount it to prevent changes during the cloning process.
   ```bash
   sudo umount /dev/sdx1
   ```
   - Repeat for all partitions on the source SSD if applicable.

5. **Clone with `dd`**:
   - Clone the source to the destination SSD using the `dd` command.
   ```bash
   sudo dd if=/dev/sdx of=/dev/sdy bs=64K conv=noerror,sync status=progress
   ```

### Post-Cloning

1. **Shutdown and Swap SSD**:
   - Power off the server after the cloning process is complete.
   - Replace the old SSD with the new one that was connected via USB3.

2. **Boot from New SSD**:
   - Start the server and check that it boots from the new SSD.

3. **Verify New Drive**:
   - Log in and use `lsblk` to ensure the new drive is recognized with the correct size.

4. **Unmount New Drive if Mounted**:
   - If the new SSD has mounted automatically, unmount it to proceed with the resize.
   ```bash
   sudo umount /dev/sdy1
   ```

5. **Check Filesystem**:
   - Perform a filesystem integrity check with `e2fsck` on the unmounted partition.
   ```bash
   sudo e2fsck -f /dev/sdy1
   ```

6. **Resize Partition**:
   - Expand the primary partition to use the full capacity of the new SSD using `parted`.
   ```bash
   sudo parted /dev/sdy resizepart 1 100%
   ```

7. **Resize Filesystem**:
   - Resize the filesystem to occupy the entire space of the partition.
   ```bash
   sudo resize2fs /dev/sdy1
   ```

8. **Reboot the Server**:
   - Reboot the server to apply the changes and allow automatic startup of services.
   ```bash
   sudo reboot
   ```

9. **Final Verification**:
   - Once the server has restarted, confirm the filesystem sizes are correct and services are running properly.
   ```bash
   df -h
   ```
