// set terraform cloud organization and workspaceterraform {
terraform {
  cloud {
    organization = "SimonDBrooke"
    workspaces {
      tags = ["jamf_pro"]
    }
  }
}