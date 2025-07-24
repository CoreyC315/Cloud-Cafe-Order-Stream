# Cloud-Cafe-Order-Stream
Continuation of the Cloud Cafe, working on developing more cloud skills

🚀 Project Overview
Welcome to Cloud Cafe Order Stream, a cutting-edge backend system for the Cloud Cafe web application! This project takes cloud engineering to the next level by implementing a robust, serverless order processing pipeline. It's designed to showcase advanced Azure services and modern DevOps practices, demonstrating how to build truly scalable, resilient, and automated cloud-native solutions.

From order placement to persistent storage, every step in the latte's journey is meticulously managed and secured. This isn't just about code; it's about the entire lifecycle automation of cloud infrastructure and applications.

✨ Core Technologies & Concepts
This project is a deep dive into critical Azure services and contemporary development methodologies:

☁️ Serverless Computing: Azure Functions for event-driven, cost-effective order processing.

💾 Data Persistence: Azure SQL Database for reliable and scalable relational data storage.

➡️ Message Queueing: Azure Storage Queue (or Azure Service Bus) for asynchronous communication, ensuring system resilience and decoupling.

🔐 Secure Access: Azure Managed Identity & Role-Based Access Control (RBAC) for secure, credential-less interactions between Azure services.

🏗️ Infrastructure as Code (IaC): Terraform to define and deploy all Azure resources declaratively and repeatably.

⚙️ CI/CD Pipeline: GitHub Actions for end-to-end automation of application builds, deployments, and even infrastructure provisioning.

🌐 Container Orchestration: Your existing Azure Kubernetes Service (AKS) for the frontend web application.

📐 High-Level Architecture
The "Latte Lifecycle" in Cloud Cafe Order Stream flows through a series of decoupled, intelligent components:

Frontend (Cloud Cafe Web App on AKS): User places an order, which is then sent to a reliable message queue.

Order Queue (Azure Storage Queue): A robust buffer holding incoming orders, decoupling the frontend from backend processing.

Order Processor (Azure Function): Triggered by new queue messages, this serverless function processes orders and securely persists them.

Database (Azure SQL Database): Stores all order details, status, and historical data persistently.

📐 High-Level Architecture
The "Latte Lifecycle" in Cloud Cafe Order Stream flows through a series of decoupled, intelligent components:

Frontend (Cloud Cafe Web App on AKS): User places an order, which is then sent to a reliable message queue.

Order Queue (Azure Storage Queue): A robust buffer holding incoming orders, decoupling the frontend from backend processing.

Order Processor (Azure Function): Triggered by new queue messages, this serverless function processes orders and securely persists them.

Database (Azure SQL Database): Stores all order details, status, and historical data persistently.

(DIAGRRAM AFTER BUILDING IT)

🚀 Getting Started
Follow these steps to explore and deploy the CloudCafeOrderStream project.

Prerequisites
Before you begin, ensure you have the following installed and configured:

Azure CLI

Terraform

.NET SDK (or Python/Node.js SDK, depending on your Azure Function language choice)

Docker Desktop (for frontend development/testing)

kubectl (for AKS interaction)

A GitHub account with secrets configured for Azure authentication (for CI/CD).

Setup & Deployment
Clone the Repository:

Bash

git clone https://github.com/YourGitHubUser/CloudCafeOrderStream.git
cd CloudCafeOrderStream
Azure Infrastructure Deployment (Terraform):
Navigate to the terraform/ directory and follow the instructions in its README.md to deploy all necessary Azure resources (Resource Group, SQL DB, Storage Account, Function App, etc.).

Bash

cd terraform
# Follow README.md instructions here
Azure Function Deployment:
Head into the src/OrderProcessorFunction/ directory. Instructions there will guide you on building and deploying your Azure Function code. This step will eventually be automated by GitHub Actions!

Bash

cd ../src/OrderProcessorFunction
# Follow README.md instructions for manual deployment OR rely on CI/CD
Frontend Application Update & Deployment:
Update your existing Cloud Cafe frontend application (in its separate repository or in src/WebApp/ if you moved it here) to send orders to the newly created Azure Storage Queue and query the Azure SQL Database for status updates. Deploy the updated frontend to your AKS cluster. This will also be handled by GitHub Actions.

Bash

# Update frontend code to interact with new backend services
# Trigger your existing frontend CI/CD pipeline

