# 🚀 Deployment & Security Hardening Guide

This guide details how to deploy VibeFinance on a Linux host with **Full Disk Encryption (LUKS)** to ensure physical security, in addition to our built-in Application-Level Encryption (ALE).

## 📑 Table of Contents
1. [Prerequisites](#1-prerequisites)
2. [OS-Level Encryption (LUKS)](#2-os-level-encryption-luks)
3. [Docker Installation & Setup](#3-docker-installation--setup)
4. [Deploying VibeFinance](#4-deploying-vibefinance)
5. [Security Hardening](#5-security-hardening)

---

## 1. Prerequisites
- A Linux-based server (Ubuntu 22.04+ or Debian 12+ recommended).
- Root or sudo access.
- A secondary partition or an external drive for encrypted data storage.

---

## 2. OS-Level Encryption (LUKS)

LUKS protects your data against physical theft of the hardware. We will create an encrypted volume and mount it to `/mnt/vibe_data`.

### Step 2.1: Identify your target drive/partition
```bash
lsblk
```
*Note: We will assume the target is `/dev/sdb1`. **WARNING: This will erase all data on the target.***

### Step 2.2: Format the partition with LUKS
```bash
sudo cryptsetup luksFormat /dev/sdb1
```
You will be prompted to enter a passphrase. **Do not lose this passphrase.**

### Step 2.3: Open the encrypted volume
```bash
sudo cryptsetup open /dev/sdb1 vibe_encrypted
```
This maps the encrypted partition to `/dev/mapper/vibe_encrypted`.

### Step 2.4: Create a filesystem
```bash
sudo mkfs.ext4 /dev/mapper/vibe_encrypted
```

### Step 2.5: Mount the volume
```bash
sudo mkdir -p /mnt/vibe_data
sudo mount /dev/mapper/vibe_encrypted /mnt/vibe_data
```

---

## 3. Docker Installation & Setup

Install Docker and Docker Compose using the official repository to ensure you have the latest security patches.

```bash
# Update and install dependencies
sudo apt update && sudo apt install -y ca-certificates curl gnupg

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Set up the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update && sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

---

## 4. Deploying VibeFinance

### Step 4.1: Clone the repository
```bash
git clone https://github.com/Alternate-Media/vibefinance.git
cd vibefinance
```

### Step 4.2: Configure Environment
Copy the example environment file and update the secrets.
```bash
cp .env.example .env
nano .env
```
**Required:** Change `POSTGRES_PASSWORD` and `SECRET_KEY`.

### Step 4.3: Configure Docker to use the LUKS Mount
Update your `docker-compose.yml` to point the database volume to the encrypted mount.

```yaml
volumes:
  postgres_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /mnt/vibe_data/postgres
```
*Note: Ensure the directory `/mnt/vibe_data/postgres` exists.*

### Step 4.4: Start the application
```bash
sudo docker compose up -d
```

---

## 5. Security Hardening

### 🛡️ Firewall (UFW)
Only allow Traefik (HTTP/HTTPS) and SSH.
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 🔑 LUKS Auto-mount (Optional/Advanced)
If you want the volume to mount automatically on boot, you can use `/etc/crypttab` and `/etc/fstab`, but this typically requires storing the key on the unencrypted OS partition, which lowers security unless combined with TPM or a USB key.

**Recommended:** Manual mounting after boot for maximum security.
```bash
# Post-reboot manual mount
sudo cryptsetup open /dev/sdb1 vibe_encrypted
sudo mount /dev/mapper/vibe_encrypted /mnt/vibe_data
sudo docker compose start
```

