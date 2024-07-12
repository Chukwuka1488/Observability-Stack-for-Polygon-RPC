# Create a network
resource "civo_network" "custom_net_2" {
  label = "my-custom-network"
}

# Create a firewall with custom rules
resource "civo_firewall" "my_firewall" {
  name                 = "my-firewall"
  network_id           = civo_network.custom_net_2.id
  create_default_rules = false

  ingress_rule {
    label      = "kubernetes-api-server"
    protocol   = "tcp"
    port_range = "6443"
    cidr       = ["0.0.0.0/0"]
    action     = "allow"
  }

  ingress_rule {
    label      = "ssh"
    protocol   = "tcp"
    port_range = "22"
    cidr       = ["0.0.0.0/0"]
    action     = "allow"
  }

  egress_rule {
    label      = "all"
    protocol   = "tcp"
    port_range = "1-65535"
    cidr       = ["0.0.0.0/0"]
    action     = "allow"
  }
}

# Query medium instance size
# g4s.kube.medium
data "civo_size" "medium" {
  filter {
    key    = "type"
    values = ["kubernetes"]
  }

  filter {
    key    = "name"
    values = ["g4s.kube.medium"]
  }

  sort {
    key       = "ram"
    direction = "asc"
  }
}

# Create a cluster with k3s
resource "civo_kubernetes_cluster" "cluster" {
  name         = "SRE-cluster"
  firewall_id  = civo_firewall.my_firewall.id
  cluster_type = "k3s"
  network_id   = civo_network.custom_net_2.id

  pools {
    label      = "front-end" // Optional
    size       = data.civo_size.medium.sizes[0].name
    node_count = 3
  }
}
