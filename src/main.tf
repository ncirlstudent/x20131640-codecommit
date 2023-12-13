terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "4.15.1"
    }
  }
}
provider "aws" {
  region     = "us-east-1"
  access_key = "ASIAT2P6UD6LH2YO4ISI"    # Replace with your actual access key
  secret_key = "TDQQlZa134m0ZENf22dwXeGzRloxuGYRBK0M4Csn" # Replace with your actual secret key
  token      = "FwoGZXIvYXdzEMj//////////wEaDHQ83tEVyFU5Qof+WCLLAcIVCeck3WBWAXkrb78pxHTHFhUNr6HG29o0sAutUyEYi5QenfGKRwwFvXq33KBezetlx5p0Ipq8h5u5X6eg/d9BYxmKNcXfF0dWZnDW9rNQHvTGITsr5zGjBJo/Aj8Mm0gPRSGPsYPfy15V5Bym+cNQ/ODZ5GIYKORpbkjFUCkeBEyJeaeQNVaRCW+tgb9wn9Ia470wDADb9Kl6Mz3tvJ2PANlougcVlm9g5B5StGsNSWX5le7IFMLVfvnufmbAtBHI+PqbuRpnVLGxKJ/b4asGMi3kigQgyQNarqRPItfrzKiuNoA8VdySs3jZLWM2i4pYEQdldEjsn/UEecXCGVE="
  }   

data "aws_ami" "latest_ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] // Canonical's official owner ID for Ubuntu AMIs
}

resource "aws_security_group" "allow_web" {
  name        = "allow_web_traffic"
  description = "Allow web inbound traffic"

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_web_traffic"
  }
}

resource "aws_instance" "web_server" {
  ami                    = data.aws_ami.latest_ubuntu.id
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.allow_web.id]
  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update -y
              sudo apt-get install -y nginx
              sudo service nginx start
              EOF

  tags = {
    Name = "UbuntuWebServer"
  }
}

output "public_ip" {
  value = aws_instance.web_server.public_ip
}

