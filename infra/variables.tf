variable "ec2_key_name" {
  description = "Existing EC2 key pair name to use for SSH"
  type        = string
}

variable "my_ip_cidr" {
  description = "Your IP address in CIDR notation for SSH (e.g. 49.37.12.34/32)"
  type        = string
}
