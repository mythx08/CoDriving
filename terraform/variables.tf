variable "aws_region" {
  description = "Région AWS pour le déploiement"
  default     = "eu-west-3" # Paris
}

variable "instance_type" {
  description = "Type d'instance pour le serveur CoDrive"
  default     = "t2.micro" # Gratuit (Free Tier)
}

variable "project_name" {
  default = "codrive-infrastructure"
}