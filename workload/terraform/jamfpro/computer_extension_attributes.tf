
# resource "jamfpro_computer_extension_attribute" "jamfpro_computer_extension_attribute_001" {
#   name        = "tf-state-migration-test-001"
#   enabled     = true
#   description = "An attribute collected from a pop-up menu."
#   input_type  = "Pop-up Menu"
#   input_popup = ["Option 1", "Option 2", "Option 3"]


#   inventory_display = "User and Location"
# }

# # //-------------------------------------------------------------------//

# resource "jamfpro_computer_extension_attribute" "jamfpro_computer_extension_attribute_002" {
#   name              = "tf-state-migration-test-002"
#   enabled           = true
#   description       = "An attribute collected from a text field."
#   input_type        = "Text Field"
#   inventory_display = "Hardware"
# }

# # //-------------------------------------------------------------------//

# resource "jamfpro_computer_extension_attribute" "jamfpro_computer_extension_attribute_003" {
#   name         = "tf-state-migration-test-003"
#   enabled      = true
#   description  = "An attribute collected via a script."
#   input_type   = "script"
#   input_script = <<-SHELL
#   #!/bin/sh
#   /bin/echo "<result>sample</result>"
#   SHELL

#   inventory_display = "General"
# }

# resource "jamfpro_computer_extension_attribute" "sample" {
#   name                   = "sample"
#   enabled                = true
#   inventory_display_type = "EXTENSION_ATTRIBUTES"
#   data_type       = "STRING"
#   input_type      = "SCRIPT"
#   script_contents = <<-SHELL
# #!/bin/sh
# /bin/echo "<result>sample</result>"
# SHELL
# }







# # Pop-up Menu Example
# resource "jamfpro_computer_extension_attribute" "jamfpro_computer_extension_attribute_popup_menu_1" {
#   name                   = "tf-demo-popup-menu-example"
#   enabled                = true
#   description            = "An attribute collected from a pop-up menu."
#   input_type             = "POPUP"
#   popup_menu_choices     = ["Option 1", "Option 2", "Option 3"]
#   inventory_display_type = "USER_AND_LOCATION"
#   data_type              = "STRING"
# }

# # Text Field Example
# resource "jamfpro_computer_extension_attribute" "computer_extension_attribute_text_field_1" {
#   name                   = "tf-demo-text-field-example"
#   enabled                = true
#   description            = "An attribute collected from a text field."
#   input_type             = "TEXT"
#   inventory_display_type = "HARDWARE"
#   data_type              = "STRING"
# }

# # Script Example
# resource "jamfpro_computer_extension_attribute" "computer_extension_attribute_script_1" {
#   name                   = "tf-demo-hello-world"
#   enabled                = true
#   description            = "An attribute collected via a script."
#   input_type             = "SCRIPT"
#   script_contents        = "#!/bin/bash\necho 'Hello, World!!!!! :)'"
#   inventory_display_type = "GENERAL"
#   data_type              = "STRING"
# }

# # Script Example
# resource "jamfpro_computer_extension_attribute" "computer_extension_attribute_script_2" {
#   name                   = "tf-demo-logged-in-user"
#   enabled                = true
#   description            = "An attribute collected via a script."
#   input_type             = "SCRIPT"
#   script_contents        = file("support_files/computer_extension_attributes/logged_in_user.sh")
#   inventory_display_type = "GENERAL"
#   data_type              = "STRING"
# }