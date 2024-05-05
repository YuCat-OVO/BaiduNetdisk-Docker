variable "TAG" {
  default = "baidunetdisk-docker:latest"
}

group "linux-amd64" {
  targets = ["image-amd64"]
}
group "linux-arm64" {
  targets = ["image-arm64"]
}

target "docker-metadata-action" {
  tags = ["${TAG}"]
}

target "image-amd64" {
  platforms  = ["linux/amd64"]
  inherits   = ["docker-metadata-action"]
  dockerfile = "Dockerfile"
}
target "image-arm64" {
  platforms  = ["linux/arm64"]
  inherits   = ["docker-metadata-action"]
  dockerfile = "Dockerfile.arm64"
}
