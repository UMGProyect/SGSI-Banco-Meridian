terraform {
  required_version = ">= 1.6, < 2.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}
provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}
locals {
  subnets = {
    app   = "10.20.10.0/24"
    sec   = "10.20.20.0/24"
    admin = "10.20.30.0/24"
  }
  nodes = {
    app  = { subnet = "app", machine = "e2-medium", disk = 20 }
    iam  = { subnet = "sec", machine = "e2-medium", disk = 20 }
    siem = { subnet = "sec", machine = "e2-standard-4", disk = 60 }
  }
}
resource "google_compute_network" "meridian" {
  name                    = "meridian-vpc"
  auto_create_subnetworks = false
  routing_mode            = "REGIONAL"
}
resource "google_compute_subnetwork" "segments" {
  for_each                 = local.subnets
  name                     = "meridian-${each.key}"
  ip_cidr_range            = each.value
  region                   = var.region
  network                  = google_compute_network.meridian.id
  private_ip_google_access = true
}
resource "google_compute_firewall" "iap_ssh" {
  name          = "meridian-iap-ssh"
  network       = google_compute_network.meridian.id
  direction     = "INGRESS"
  source_ranges = ["35.235.240.0/20"]
  target_tags   = ["meridian-admin"]
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
  log_config {
    metadata = "EXCLUDE_ALL_METADATA"
  }
}
resource "google_compute_router" "nat" {
  count   = var.enable_nat ? 1 : 0
  name    = "meridian-nat-router"
  region  = var.region
  network = google_compute_network.meridian.id
}
resource "google_compute_router_nat" "outbound" {
  count                              = var.enable_nat ? 1 : 0
  name                               = "meridian-nat"
  router                             = google_compute_router.nat[0].name
  region                             = var.region
  nat_ip_allocate_option              = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "LIST_OF_SUBNETWORKS"
  dynamic "subnetwork" {
    for_each = { for k, v in google_compute_subnetwork.segments : k => v if k != "admin" }
    content {
      name                    = subnetwork.value.id
      source_ip_ranges_to_nat = ["PRIMARY_IP_RANGE"]
    }
  }
}
resource "google_compute_instance" "nodes" {
  for_each     = var.enable_vms ? local.nodes : {}
  name         = "meridian-${each.key}"
  machine_type = each.value.machine
  zone         = var.zone
  tags         = ["meridian-admin", "meridian-${each.key}"]
  labels       = { project = "meridian", environment = "lab" }
  boot_disk {
    initialize_params {
      image = "projects/ubuntu-os-cloud/global/images/family/ubuntu-2404-lts-amd64"
      size  = each.value.disk
      type  = "pd-balanced"
    }
  }
  network_interface {
    subnetwork = google_compute_subnetwork.segments[each.value.subnet].id
  }
  metadata = {
    enable-oslogin         = "TRUE"
    block-project-ssh-keys = "TRUE"
  }
  shielded_instance_config {
    enable_secure_boot          = true
    enable_vtpm                 = true
    enable_integrity_monitoring = true
  }
}
