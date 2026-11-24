import unittest
from check_tracked_files import forbidden


class FilenamePolicyTests(unittest.TestCase):
    def test_block(self):
        for path in [
            ".env", "src/.ENV.production", "infra/state.tfstate.backup",
            "infra/run.tfplan", "infra/prod.tfvars.json", ".terraform/modules/x",
            "key.PEM", "credentials.json", "nested/gha-creds-1.json",
            "application_default_credentials.json", "evidencias/raw/test.json",
            "evidencias/privadas/test.png", "backup.db", "secrets/.env.example",
            "x/packet.pcapng", "backups/report.zip", "nested/.ssh/config",
        ]:
            with self.subTest(path=path):
                self.assertTrue(forbidden(path))

    def test_allow(self):
        for path in [
            ".env.example", "infraestructura/gcp/terraform.tfvars.example",
            "infra/demo.example.tfvars", "demo.example.tfvars.json",
            "infra/.terraform.lock.hcl", "main.tf", "docs/ALCANCE.md",
            "evidencias/publicas/resumen.json",
        ]:
            with self.subTest(path=path):
                self.assertFalse(forbidden(path))


if __name__ == "__main__":
    unittest.main()
