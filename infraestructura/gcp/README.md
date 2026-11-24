# Fundación GCP — Banco Meridian
Borrador inicial de IaC, no ejecutado contra GCP. Terraform CLI >=1.6; proveedor hashicorp/google 6.x (rango explícito, revisar compatibilidad y lockfile al inicializar). Requiere proyecto nuevo con facturación vinculada y permisos de despliegue. No usar ID del proyecto TCP/IP.
## Preparación por el usuario
1. Crear el proyecto independiente en consola, vincular facturación y establecer presupuesto/alertas (no son tope de gasto).
2. Confirmar ID real, región, CIDR local VMware y ausencia de solapamientos. No compartir contraseñas, tokens ni JSON de cuentas de servicio.
3. En Cloud Shell, revisar cuenta y proyecto: gcloud auth list; gcloud projects describe ID_NUEVO. Habilitar APIs exclusivamente en ese proyecto: gcloud services enable compute.googleapis.com iap.googleapis.com oslogin.googleapis.com iam.googleapis.com --project=ID_NUEVO
4. Otorgar a administradores autorizados roles IAP-secured Tunnel User y Compute OS Login u OS Admin Login, y permisos de lectura necesarios, con mínimo alcance posible. No otorgar roles a todos los usuarios. Autenticación de Terraform con ADC; en estación local usar gcloud auth application-default login.
5. Copiar terraform.tfvars.example a terraform.tfvars; ingresar ID real. El ID debe comenzar con sgsi-banco-meridian, o adaptar explícitamente validación si se eligió otro.
## Plan
terraform init
terraform fmt -check
terraform validate
terraform plan -out=meridian.tfplan
Revisar plan antes de aplicar; inicialmente solo VPC, tres subredes y regla IAP. No ejecutar apply hasta revisión. Los cambios de costo (VMs/NAT) requieren habilitación explícita.
La opción enable_vms crea tres VM privadas (app, iam, siem), sin software de aplicación ni acceso público. enable_nat habilita salida a Internet para instalación/actualización; genera cargos. No hay balanceador, VPN, Suricata, WAF ni SIEM instalado todavía. La infraestructura local se prepara en etapa separada. No asignar cuenta de servicio predeterminada ni claves. OS Login e IAP requieren roles previamente configurados.
Prueba SSH tras aprovisionamiento: gcloud compute ssh meridian-app --zone=us-central1-a --project=ID_NUEVO --tunnel-through-iap
Mantener tfstate y tfplan fuera de Git; usar estado protegido y coordinar ejecución con un único operador. No usar terraform destroy sin revisar plan y proyecto.
