
resource "jamfpro_dock_item" "jamfpro_dock_item_001" {
  name = "tf-dw-ghatest-dockItem-app-iTunes"
  type = "App"
  path = "file://localhost/Applications/iTunes.app/"
}

resource "jamfpro_dock_item" "jamfpro_dock_item_002" {
  name = "tf-dw-ghatest-dockItem-file-hosts"
  type = "File" // App / File / Folder
  path = "/etc/hosts"
}

resource "jamfpro_dock_item" "jamfpro_dock_item_003" {
  name = "tf-dw-ghatest-dockItem-folder-downloadsFolder"
  type = "Folder" // App / File / Folder
  path = "~/Downloads"
}

resource "jamfpro_dock_item" "jamfpro_dock_item_004" {
  name = "tf-dw-ghatest-dockItem-folder-downloadsFolder2"
  type = "Folder" // App / File / Folder
  path = "~/Downloads"
}
resource "jamfpro_dock_item" "jamfpro_dock_item_005" {
  name = "tf-dw-ghatest-dockItem-folder-downloadsFolder3"
  type = "Folder" // App / File / Folder
  path = "~/Downloads"
}