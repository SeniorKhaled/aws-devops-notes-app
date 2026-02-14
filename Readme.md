# 📘 Secure Note-Taking Web App on AWS EC2

## 🎯 Project Overview
This project involves deploying a dynamic **Note-Taking Web Application** on an **AWS EC2** instance running **Red Hat Enterprise Linux (RHEL 10)**. The application is built using **Python (Flask)** and connected to a **MariaDB** database. 

Live Demo: 34.247.232.184

A key feature of this project is the implementation of a **Data Backup Strategy** by mounting an external **EBS Volume** to persist database backups securely.

---

## 🏗️ Architecture & Tech Stack
* **Cloud Provider:** AWS (Amazon Web Services)
* **OS:** Red Hat Enterprise Linux (RHEL 10) [cite: 15]
* **Server:** EC2 (t2.micro / t3.micro) [cite: 16]
* **Language:** Python 3 (Flask Framework) [cite: 20]
* **Database:** MariaDB (SQL) [cite: 5]
* **Storage:** 1GB EBS Volume mounted at `/backup` [cite: 29]

---

## ⚙️ Installation & Setup Steps

### 1. Infrastructure Setup (AWS)
1.  Launched an **EC2 Instance** using the RHEL 10 AMI.
2.  Configured **Security Group** to allow:
    * **SSH (Port 22):** For remote administration. [cite: 17]
    * **HTTP (Port 80):** For web traffic. [cite: 17]
3.  Created a **1GB EBS Volume** in the same Availability Zone.
4.  Attached the volume to the EC2 instance.

### 2. Linux Server Configuration
**Mounting the Backup Volume:**
```bash
lsblk                       # Identify the new disk (e.g., nvme1n1)
sudo mkfs.xfs /dev/nvme1n1  # Format the volume
sudo mkdir /backup          # Create mount point
[cite_start]sudo mount /dev/nvme1n1 /backup # Mount the volume [cite: 29]
Installing Dependencies:

Bash
sudo dnf update -y
sudo dnf install python3 python3-pip mariadb-server mariadb git firewalld -y
pip3 install flask mysql-connector-python
3. Database Configuration (MariaDB)
Starting the Service:

Bash
sudo systemctl start mariadb
sudo systemctl enable mariadb
Schema & User Setup: Executed the following SQL commands to create the database with UTF-8 support (for Arabic text) and a dedicated user:

SQL
CREATE DATABASE notes_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; [cite: 25]

USE notes_db;

CREATE TABLE notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE USER 'admin'@'localhost' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON notes_db.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
4. Application Deployment
Created the app.py file containing the Flask logic and HTML/CSS UI.

Configured the application to run on Port 80.

Firewall Configuration:

Bash
sudo systemctl start firewalld
sudo firewall-cmd --zone=public --add-port=80/tcp --permanent
sudo firewall-cmd --reload
Running the App (Background Process):

Bash
sudo nohup python3 app.py > output.log 2>&1 &
The app is now accessible via the Public IP.

🛡️ Backup Strategy
To ensure data safety, a backup process was implemented to export the database to the mounted EBS volume.

Backup Command:

Bash
sudo mysqldump -u admin -p notes_db > /backup/final_backup.sql
Verification:

Bash
ls -l /backup

Result: -rw-r--r--. 1 root root 2438 Jan 29 20:19 notes_backup_2026-01-29_20:19:18.sql
