
# # //-------------------------------------------------------------------//
resource "jamfpro_computer_extension_attribute" "computer_extension_attribute_popup_menu_1" {
  name        = "tf-ghatest-cexa-popup-menu-example"
  enabled     = true
  description = "An attribute collected from a pop-up menu."
  data_type   = "String"

  input_type {
    type    = "Pop-up Menu"
    choices = ["Option 1", "Option 2", "Option 3"]
  }

  inventory_display = "User and Location"
}

# //-------------------------------------------------------------------//

# resource "jamfpro_computer_extension_attribute" "computer_extension_attribute_text_field_1" {
#   name        = "tf-example-cexa-text-field-example"
#   enabled     = true
#   description = "An attribute collected from a text field."
#   data_type   = "String"

#   input_type {
#     type = "Text Field"
#   }

#   inventory_display = "Hardware"
# }


# //-------------------------------------------------------------------//


# resource "jamfpro_computer_extension_attribute" "computer_extension_attribute_script_1" {
#   name        = "tf-example-cexa-hello-world"
#   enabled     = true
#   description = "An attribute collected via a script."
#   data_type   = "String"

#   input_type {
#     type     = "script"
#     platform = "Mac"
#     script   = "#!/bin/bash\necho 'Hello, World!!!!! :)'"
#   }

#   inventory_display = "General"
# }



# resource "jamfpro_computer_extension_attribute" "computer_extension_attribute_script_2" {
#   name        = "tf-example-cexa-logged-in-user"
#   enabled     = true
#   description = "An attribute collected via a script."
#   data_type   = "String"

#   input_type {
#     type     = "script"
#     platform = "Mac"
#     script   = file("support_files/computer_extension_attribute.sh") // Point to the script file using the file function
#   }

#   inventory_display = "Operating System"
# }

resource "jamfpro_computer_extension_attribute" "computer_extension_attribute_script_batch" {
  count       = 5
  name        = "tf-example-cexa-logged-in-user-${format("%03d", count.index + 1)}"
  enabled     = true
  description = "An attribute collected via a script."
  data_type   = "String"

  input_type {
    type     = "script"
    platform = "Mac"
    script   = file("support_files/computer_extension_attributes/logged_in_user.sh") // Point to the script file using the file function
  }

  inventory_display = "Operating System"
}
