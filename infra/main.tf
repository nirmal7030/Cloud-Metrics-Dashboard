terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"  # Must match your AWS_REGION secret
}

# -----------------------------
# ECR Repository for Docker image
# -----------------------------
resource "aws_ecr_repository" "cloud_metrics_repo" {
  name = "cloud-metrics-dashboard"

  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# -----------------------------
# Security Group for EC2
# -----------------------------
resource "aws_security_group" "cloud_metrics_sg" {
  name        = "cloud-metrics-sg"
  description = "Allow SSH and HTTP for Cloud Metrics Dashboard"

  # SSH - open so GitHub Actions runners can SSH into EC2
  # (OK for demo; in production you would restrict this)
  ingress {
    description = "SSH from anywhere (CI/CD demo)"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP - from anywhere (for your dashboard)
  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound - allow all
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# -----------------------------
# Get latest Ubuntu 22.04 LTS AMI
# -----------------------------
data "aws_ami" "ubuntu" {
  most_recent = true

  owners = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# -----------------------------
# EC2 Instance
# -----------------------------
resource "aws_instance" "cloud_metrics_ec2" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t2.micro"
  key_name               = var.ec2_key_name
  vpc_security_group_ids = [aws_security_group.cloud_metrics_sg.id]

  tags = {
    Name = "cloud-metrics-dashboard-ec2"
  }

  # Install Docker and AWS CLI on first boot
  user_data = <<-EOF
              #!/bin/bash
              apt-get update -y
              apt-get install -y docker.io awscli
              systemctl start docker
              systemctl enable docker
              EOF
}
