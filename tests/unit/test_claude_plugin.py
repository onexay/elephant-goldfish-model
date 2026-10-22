# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for the Claude Code plugin and marketplace manifests."""

import json
import pathlib
import re
from typing import Any, Dict

# Matches plugin-root paths that skills and personas tell the agent to read.
PLUGIN_PATH_PATTERN = re.compile(
    r"`((?:skills|agents|resources)/[A-Za-z0-9_./-]+\.md)`"
)


def read_json(path: pathlib.Path) -> Dict[str, Any]:
  return json.loads(path.read_text(encoding="utf-8"))


def test_claude_manifest_matches_gemini_extension(
    repo_root: pathlib.Path,
) -> None:
  """Verifies shared metadata does not drift between harness manifests."""
  claude = read_json(repo_root / ".claude-plugin" / "plugin.json")
  gemini = read_json(repo_root / "gemini-extension.json")
  for field in ("name", "version", "description"):
    assert claude[field] == gemini[field], f"'{field}' differs"


def test_claude_marketplace_points_at_repo_root(
    repo_root: pathlib.Path,
) -> None:
  """Verifies the marketplace lists this plugin from the repository root."""
  marketplace = read_json(repo_root / ".claude-plugin" / "marketplace.json")
  plugin = read_json(repo_root / ".claude-plugin" / "plugin.json")
  assert marketplace["owner"]["name"]
  assert len(marketplace["plugins"]) == 1
  entry = marketplace["plugins"][0]
  assert entry["name"] == plugin["name"]
  assert (repo_root / entry["source"]).resolve() == repo_root.resolve()


def test_plugin_root_paths_exist(repo_root: pathlib.Path) -> None:
  """Verifies concrete plugin-root paths in skills and personas exist."""
  sources = list((repo_root / "skills").glob("*/SKILL.md"))
  sources += list((repo_root / "agents").glob("*.md"))
  for source in sources:
    for match in PLUGIN_PATH_PATTERN.finditer(source.read_text("utf-8")):
      target = match.group(1)
      if "{" in target or "<" in target:
        continue
      assert (repo_root / target).is_file(), (
          f"{source.relative_to(repo_root)} references missing {target}"
      )
