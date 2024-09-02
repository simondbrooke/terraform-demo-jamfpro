resource "jamfpro_category" "jamfpro_category_001" {
  name     = "tf-ghatest-operating-system"
  priority = 10
}

resource "jamfpro_category" "jamfpro_category_002" {
  name     = "tf-ghatest-self-service"
  priority = 10
}

resource "jamfpro_category" "jamfpro_category_003" {
  name     = "tf-ghatest-security"
  priority = 10
}

resource "jamfpro_category" "jamfpro_category_004" {
  name     = "tf-ghatest-network"
  priority = 10
}