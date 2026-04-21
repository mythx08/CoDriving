output "server_public_ip" {
  description = "L'adresse IP publique de notre serveur CoDrive"
  value       = aws_instance.codrive_server.public_ip
}