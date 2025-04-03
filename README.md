# Team12 - Flask + SQLite DevOps Pipeline

This project showcases the deployment of a Flask application using SQLite as a local database through a complete CI/CD pipeline.

---

## Project Overview

This project demonstrates a complete DevOps pipeline integrating a Flask web application with SQLite, Jenkins for continuous integration, Ansible for automated deployment, and AWS S3 for artifact storage.

---

## features

- **Flask** – Lightweight Python web framework
- **SQLite** – Local file-based database
- **GitHub** – Code collaboration and version control
- **Jenkins** – CI/CD pipeline automation
- **AWS S3** – Artifact storage and backup
- **AWS EC2** – Hosting our app and Jenkins
- **Ansible** – App deployment and provisioning
- **Dynamic Inventory** – Uses EC2 tags to target app instances

---

## CI/CD Pipeline Flow

1. Jenkins pulls the latest code from GitHub
2. Installs dependencies and runs basic tests
3. Archives the Flask app as `flask_app.tar.gz`
4. Uploads the artifact to an AWS S3 bucket
5. Triggers Ansible to deploy the app using dynamic inventory
6. App becomes publicly accessible over port 5000

---

## Expected Output

When visiting the deployed app in your browser, you'll see:


---

## Team Status

This marks the successful implementation of a real-world DevOps workflow.

**We are officially DevOps Engineers!**
