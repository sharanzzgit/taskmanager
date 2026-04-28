variable "db_username"{
    description= "RDS master username"
    type = string
}

variable "db_password"{
    description = "RDS master password"
    type = string
    sensitive = true
}

variable "db_name"{
    description = "Database name"
    type = string
    default = "taskmanager"
}

variable "aws_region"{
    description = "AWS region"
    type = string
    default = "ap-south-1"
}
