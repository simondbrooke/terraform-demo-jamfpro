resource "jamfpro_smart_computer_group" "smart_computer_group_001" {
  name = "tf-ghatest-computergroup-operating-system-like-macos-14"

  // optional
  site_id = -1
  criteria {
    name          = "Operating System Version"
    priority      = 0
    and_or        = "and"
    search_type   = "like"
    value         = "14"
    opening_paren = true
    closing_paren = false
  }
  criteria {
    name          = "Operating System Version"
    priority      = 1
    and_or        = "and"
    search_type   = "like"
    value         = "14"
    opening_paren = false
    closing_paren = true
  }

}

resource "jamfpro_smart_computer_group" "smart_computer_group_002" {
  name = "tf-ghatest-non_compliant_macs"

  site_id = -1
  criteria {
    name          = "FileVault 2 Status"
    priority      = 0
    and_or        = "or"
    search_type   = "is"
    value         = "not Encrypted"
    opening_paren = true
    closing_paren = false
  }
  criteria {
    name          = "Gatekeeper Status"
    priority      = 1
    and_or        = "or"
    search_type   = "is"
    value         = "not Enabled"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name          = "SIP Status"
    priority      = 2
    and_or        = "or"
    search_type   = "is"
    value         = "not Enabled"
    opening_paren = false
    closing_paren = true
  }
}

resource "jamfpro_smart_computer_group" "smart_computer_group_003" {
  name = "tf-ghatest-non_compliant_macs"

  site_id = -1
  criteria {
    name          = "Application Title"
    priority      = 0
    and_or        = "and"
    search_type   = "has"
    value         = "Microsoft Word"
    opening_paren = true
    closing_paren = false
  }
  criteria {
    name          = "Application Version"
    priority      = 1
    and_or        = "and"
    search_type   = "is less than"
    value         = " 16.50"
    opening_paren = false
    closing_paren = true
  }
}