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
