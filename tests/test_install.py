from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "install.py"
SPEC = importlib.util.spec_from_file_location("harness_craft_install", MODULE_PATH)
INSTALL = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(INSTALL)


class InstallScriptTests(unittest.TestCase):
    def test_resolve_skill_names_flagship(self) -> None:
        self.assertEqual(
            INSTALL.resolve_skill_names("flagship", []),
            ["repo-bootstrap", "longrun-dev", "learn", "agent-team-dev"],
        )

    def test_upsert_managed_block_preserves_user_content(self) -> None:
        existing = "# User notes\n\nKeep this.\n"
        managed = "{0}\nhello\n{1}\n".format(INSTALL.MANAGED_BEGIN, INSTALL.MANAGED_END)
        updated = INSTALL.upsert_managed_block(existing, managed)
        self.assertIn("# User notes", updated)
        self.assertIn("hello", updated)

    def test_upsert_managed_block_replaces_existing_managed_block(self) -> None:
        existing = (
            "before\n"
            "{0}\nold\n{1}\n"
            "after\n"
        ).format(INSTALL.MANAGED_BEGIN, INSTALL.MANAGED_END)
        managed = "{0}\nnew\n{1}\n".format(INSTALL.MANAGED_BEGIN, INSTALL.MANAGED_END)
        updated = INSTALL.upsert_managed_block(existing, managed)
        self.assertIn("before", updated)
        self.assertIn("after", updated)
        self.assertIn("new", updated)
        self.assertNotIn("old", updated)

    def test_install_codex_guardrails_writes_project_agents(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            agents_path = INSTALL.install_codex_guardrails(
                scope="project",
                project_root=project_root,
                include_python=True,
            )
            text = agents_path.read_text(encoding="utf-8")
            self.assertTrue(agents_path.exists())
            self.assertIn("harness-craft Codex Guardrails", text)
            self.assertIn("## Python", text)
            self.assertIn(INSTALL.MANAGED_BEGIN, text)
            self.assertIn(INSTALL.MANAGED_END, text)


if __name__ == "__main__":
    unittest.main()
