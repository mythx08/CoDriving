terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# 1. Création d'un pare-feu (Security Group)
resource "aws_security_group" "codrive_sg" {
  name        = "allow_web_traffic"
  description = "Autoriser le traffic HTTP et SSH"

  # Autoriser l'accès SSH (pour nous connecter au serveur)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Autoriser l'accès à notre API FastAPI sur le port 8000
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Autoriser la sortie vers internet (pour télécharger Docker par exemple)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 2. Création du serveur EC2
resource "aws_instance" "codrive_server" {
  ami           = "ami-00ac45f3917454b37" # Ubuntu 22.04 LTS à Paris
  instance_type = var.instance_type
  vpc_security_group_ids = [aws_security_group.codrive_sg.id]

  tags = {
    Name = "${var.project_name}-server"
  }
}