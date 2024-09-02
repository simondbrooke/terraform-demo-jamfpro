resource "jamfpro_script" "jamfpro_script_001" {
  name            = "tf-dw-ghatest-correct-application-permissions-v1.0"
  script_contents = file("${path.module}/support_files/scripts/Correct Application Permissions.sh")
  os_requirements = "13"
  priority        = "BEFORE"
  info            = "Adds target user or group to specified group membership, or removes said membership."
  notes           = "Jamf Pro script parameters: 4 -> 7"
  parameter4      = "Google Chrome" // targetApplication
}

resource "jamfpro_script" "jamfpro_script_002" {
  name            = "tf-dw-ghatest-encrypt-apfs-volume-v5.0.1"
  script_contents = file("${path.module}/support_files/scripts/Encrypt APFS Volume.zsh")
  os_requirements = "13"
  priority        = "BEFORE"
  info            = "Adds target user or group to specified group membership, or removes said membership."
  notes           = "Jamf Pro script parameters: 4"
  parameter4      = "/" // targetVolume
}

resource "jamfpro_script" "jamfpro_script_003" {
  name            = "tf-dw-ghatest-reset-safari-v2.1.4"
  script_contents = file("${path.module}/support_files/scripts/Reset_Safari.sh")
  os_requirements = "13"
  priority        = "BEFORE"
  info            = "Deleting Safari preference files to reset to system default."
  notes           = "Jamf Pro script parameters: none"
}
