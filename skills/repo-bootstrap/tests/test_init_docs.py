import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "init_docs.py"


def load_module():
    spec = importlib.util.spec_from_file_location("repo_bootstrap", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RepoBootstrapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_repo_fixture(self) -> None:
        (self.repo_root / "README.md").write_text(
            "# Example App\n\nA sample service for managing durable repo context.\n",
            encoding="utf-8",
        )
        (self.repo_root / "package.json").write_text(
            json.dumps(
                {
                    "name": "example-app",
                    "scripts": {
                        "dev": "next dev",
                        "build": "next build",
                        "test": "vitest",
                        "lint": "eslint .",
                    },
                    "dependencies": {
                        "next": "15.0.0",
                        "react": "19.0.0",
                    },
                    "devDependencies": {
                        "typescript": "5.0.0",
                    },
                }
            ),
            encoding="utf-8",
        )
        (self.repo_root / "src").mkdir()
        (self.repo_root / "src" / "index.ts").write_text("export const ready = true;\n", encoding="utf-8")

    def test_bootstrap_creates_useful_baseline_files(self) -> None:
        self.write_repo_fixture()

        result = self.module.sync_docs(self.repo_root, context={})

        self.assertTrue((self.repo_root / "codex" / "state.json").exists())
        self.assertEqual(result["docs"]["memory.md"], "created")
        self.assertIn("/codex/", (self.repo_root / ".gitignore").read_text(encoding="utf-8"))

        repowiki = (self.repo_root / "codex" / "repowiki.md").read_text(encoding="utf-8")
        prompt_log = (self.repo_root / "codex" / "prompt.md").read_text(encoding="utf-8")

        self.assertIn("Example App", repowiki)
        self.assertIn("A sample service for managing durable repo context.", repowiki)
        self.assertIn("Next.js", repowiki)
        self.assertIn("npm run build", repowiki)
        self.assertIn("Captured automatically during bootstrap", prompt_log)

    def test_update_rolls_memory_and_prompt_history_forward(self) -> None:
        self.write_repo_fixture()
        self.module.sync_docs(
            self.repo_root,
            context={
                "latest_prompt": "Bootstrap this repo memory system.",
                "intent": "Create the first durable memory baseline.",
                "objective": "Bootstrap docs",
                "next_actions": ["Inspect repo structure"],
            },
        )

        self.module.sync_docs(
            self.repo_root,
            context={
                "latest_prompt": "Add rolling update support.",
                "intent": "Persist new knowledge without losing prior history.",
                "objective": "Implement rolling updates",
                "work_summary": "Added structured state-backed updates.",
                "decisions": [
                    {
                        "summary": "Use a state.json source of truth",
                        "reason": "Keep markdown docs synchronized across turns",
                        "tradeoff": "Adds one machine-readable artifact",
                    }
                ],
                "next_actions": ["Run unit tests", "Review rendered docs"],
            },
        )

        memory = (self.repo_root / "codex" / "memory.md").read_text(encoding="utf-8")
        prompt_log = (self.repo_root / "codex" / "prompt.md").read_text(encoding="utf-8")
        state = json.loads((self.repo_root / "codex" / "state.json").read_text(encoding="utf-8"))

        self.assertIn("Implement rolling updates", memory)
        self.assertIn("Use a state.json source of truth", memory)
        self.assertIn("Add rolling update support.", prompt_log)
        self.assertIn("Bootstrap this repo memory system.", prompt_log)
        self.assertEqual(len(state["prompt_log"]["history"]), 2)

    def test_plan_and_checklist_stay_aligned(self) -> None:
        self.write_repo_fixture()

        self.module.sync_docs(
            self.repo_root,
            context={
                "latest_prompt": "Plan the bootstrap enhancement.",
                "plan": {
                    "request_summary": "Enhance repo bootstrap to support rolling updates.",
                    "in_scope": ["Durable state", "Markdown rendering"],
                    "out_of_scope": ["Remote sync"],
                    "assumptions": ["Context docs stay gitignored"],
                    "dependencies": ["Python 3"],
                    "steps": [
                        {
                            "id": "P1",
                            "step": "Create a state-backed sync layer",
                            "why": "Preserve knowledge across turns",
                            "owner": "Agent",
                            "status": "in_progress",
                        }
                    ],
                    "files": [
                        {
                            "path": "skills/repo-bootstrap/scripts/init_docs.py",
                            "change_type": "modify",
                            "purpose": "Add sync logic",
                            "linked_step": "P1",
                        }
                    ],
                    "validation": {
                        "automated_checks": ["python3 -m unittest"],
                        "manual_checks": ["Inspect codex/*.md output"],
                        "artifacts": ["codex/state.json"],
                    },
                    "risks": ["State schema drift"],
                    "mitigations": ["Render markdown from one source of truth"],
                    "rollback": "Re-run bootstrap with a clean codex directory.",
                },
                "checklist": {
                    "plan_mapping": [
                        {
                            "plan_step": "P1",
                            "item": "Implement sync layer",
                            "status": "[x]",
                            "evidence": "state-backed rendering added",
                        }
                    ],
                    "implementation_checks": [
                        {"item": "Code changes completed for planned files", "status": "[x]"},
                        {"item": "Docs/config updates applied", "status": "[x]"},
                    ],
                    "files": [
                        {
                            "path": "skills/repo-bootstrap/scripts/init_docs.py",
                            "purpose": "Add sync logic",
                            "linked_step": "P1",
                            "status": "done",
                        }
                    ],
                    "validation_results": [
                        {
                            "check": "python3 -m unittest",
                            "result": "pass",
                            "notes": "All repo bootstrap tests passed.",
                        }
                    ],
                    "post_implementation": [
                        {"item": "Plan and checklist synchronized", "status": "[x]"}
                    ],
                },
            },
        )

        plan = (self.repo_root / "codex" / "plan.md").read_text(encoding="utf-8")
        checklist = (self.repo_root / "codex" / "checklist.md").read_text(encoding="utf-8")

        self.assertIn("| P1 | Create a state-backed sync layer |", plan)
        self.assertIn("skills/repo-bootstrap/scripts/init_docs.py", plan)
        self.assertIn("| P1 | Implement sync layer | [x] |", checklist)
        self.assertIn("state-backed rendering added", checklist)


if __name__ == "__main__":
    unittest.main()
