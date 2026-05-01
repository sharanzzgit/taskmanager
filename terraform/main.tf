terraform {
    required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~> 5.0"
    }
    }
}

provider "aws" {
region = var.aws_region
}

resource "aws_db_instance" "taskmanager" {
  identifier        = "taskmanager-db"
  engine            = "postgres"
  engine_version    = "15"
  instance_class    = "db.t3.micro"
  allocated_storage = 20
  db_name           = var.db_name
  username          = var.db_username
  password          = var.db_password
  
  publicly_accessible    = true
  skip_final_snapshot    = true
  deletion_protection    = false

  tags = {
    Name = "taskmanager-db"
  }
}

resource "aws_key_pair" "taskmanager"{
  key_name = "taskmanager-key"
  public_key = file("~/.ssh/taskmanager-key.pub")
}

resource "aws_security_group" "taskmanager_ec2"{
  name = "taskmanager-ec2-sg"
  description = "Allow HTTP, HTTPS and SSH"

  ingress{
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress{
    from_port = 8000
    to_port = 8000
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress{
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "taskmanager" {
  ami = "ami-0f58b397bc5c1f2e8"
  instance_type = "t3.micro"
  key_name = aws_key_pair.taskmanager.key_name
  vpc_security_group_ids = [aws_security_group.taskmanager_ec2.id]

  user_data = <<-EOF
    #!/bin/bash
    apt-get update -y 
    apt-get install -y docker.io docker-compose git
    systemctl start docker
    systemctl enable docker
    usermod -aG docker ubuntu
  EOF

  tags={
    Name = "taskmanager-ec2"
  }
}