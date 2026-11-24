output "project_id" {
  value = var.project_id
}
output "network" {
  value = google_compute_network.meridian.name
}
output "subnets" {
  value = { for k, s in google_compute_subnetwork.segments : k => s.ip_cidr_range }
}
output "private_ips" {
  value = { for k, vm in google_compute_instance.nodes : k => vm.network_interface[0].network_ip }
}
