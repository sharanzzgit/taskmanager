output "db_endpoint"{
    description = "RDS endpoint"
    value = aws_db_instance.taskmanager.endpoint
}

output "db_name"{
    description = "Database name"
    value = aws_db_instance.taskmanager.db_name
}

output "db_username"{
    description = "Database username"
    value = aws_db_instance.taskmanager.username
}