variable "GITHUB_SHA" {
  default = "devel"
}

group "default" {
  targets = ["web"]
}

target "web" {
  context = "."
  dockerfile = "Dockerfile"
  tags = [
    "ghcr.io/tigrisdata-community/afflatus:latest",
    "ghcr.io/tigrisdata-community/afflatus:${GITHUB_SHA}"
  ]
  platforms = [
    "linux/amd64",
    #"linux/arm64",
  ]
  cache-from = [
    "type=gha"
  ]
  cache-to = [
    "type=gha,mode=max"
  ]
}