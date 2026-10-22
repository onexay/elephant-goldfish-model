# Harnesses

EGM is one set of skills and personas. This repository serves as the
plugin source for each supported harness. No harness gets a fork of the skill
text.

## Install

| Harness | Install |
| --- | --- |
| Antigravity | `/plugin`, then install from `https://github.com/google/elephant-goldfish-model` |
| Gemini CLI | `gemini extensions install https://github.com/google/elephant-goldfish-model` |
| Claude Code | `/plugin marketplace add google/elephant-goldfish-model`, then `/plugin install egm@elephant-goldfish-model` |
| Claude Desktop (Cowork) | Customize > Plugins > Add marketplace, enter `google/elephant-goldfish-model`, then install `egm` |

Install the whole plugin. Skill-only installers that copy `skills/` alone
break EGM, because the skills read `agents/` and
`resources/document_standards/` at run time.

## Manifests

| Harness | Manifest | Skills | Subagents |
| --- | --- | --- | --- |
| Antigravity | `plugin.json` | `skills/` (default) | `agents/` (default) |
| Gemini CLI | `gemini-extension.json` | `skills/` (default) | `agents/` (default) |
| Claude Code, Claude Desktop | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` | `skills/` (default) | `agents/` (default) |

Persona prompts live in `agents/`, the directory Antigravity and Gemini CLI
scan for subagents. Each persona has `name` and `description` frontmatter, so
harnesses that load `agents/*.md` register them as named subagents
(`egm-design`, `egm-zoom-out`, and so on).

## Delegation

Skills say "spawn a subagent" and name a persona. Each harness maps that
phrase to its own tool:

| Harness | Subagent tool | Named personas | Nesting |
| --- | --- | --- | --- |
| Antigravity | `invoke_subagent` | Yes | Yes |
| Gemini CLI | Subagents | Yes | Not verified |
| Claude Code, Claude Desktop (Cowork) | Agent tool (`egm:<name>`) | Yes | Yes, 3 levels by default |

Where a harness has no named persona, the skill spawns a general-purpose
subagent and tells it to read `agents/<file>.md` first. If a harness cannot
nest subagents, use direct dispatch instead of the synthesizer.

A Goldfish review needs a fresh context. If a harness has no subagent tool,
the review skills stop instead of running in the same context.

## Claude Code and Claude Desktop

Claude Code namespaces plugin skills and subagents with the plugin name. Run
skills as `/egm:egm-brainstorm`, `/egm:egm-draft`, `/egm:egm-review`, and so on
(the bare `/egm-review` form also works when no other skill has that name).
Persona subagents register as `egm:egm-zoom-out`, `egm:egm-design`, and so on.

The skills set `disable-model-invocation: true`, so Claude only runs them when
you type the command. When one skill hands off to another (for example
`egm-review` to `egm-review-loop` and `egm-resolve`), it reads the other skill's
`SKILL.md` from the plugin root instead of calling it as a skill, because Claude
Code blocks model calls to these skills.

Claude Code installs plugins into a cache directory, not your project. Skills
and personas resolve `agents/`, `resources/`, and `skills/` through
`${CLAUDE_PLUGIN_ROOT}`, which Claude Code replaces with the installed plugin
path. Reports and drafts are written to your project.

The seven Goldfish reviewer personas set `omitClaudeMd: true`, so Claude Code
starts them without the user, project, and local `CLAUDE.md` files (managed
policy files still load). This needs Claude Code 2.1.271 or later. They also set
`omitAgentsMd: true` to keep `AGENTS.md` out of reviewer context. Claude Code
does not load `AGENTS.md`, and no harness has been verified to read this key
yet. The synthesizer and bootstrap orchestrator keep the files. Isolation covers
context only: reviewers can still read any file they can reach.

Structured gates use Claude's `AskUserQuestion` tool. It always adds an "Other"
option for free-text answers.

Bootstrap and review need at most two levels of nested subagents, within Claude
Code's default limit. Do not set `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`.

To test a local checkout without installing it, load it as a plugin and let
Claude read it, since reviewers read personas and standards from the plugin
directory:

```bash
claude plugin validate .
claude --plugin-dir /path/to/elephant-goldfish-model --add-dir /path/to/elephant-goldfish-model
```

In Claude Desktop, install the plugin in Cowork (or the Code tab, which runs
Claude Code). Plain chat cannot run EGM: chat skills have no subagents and are
uploaded one skill folder at a time, so they cannot read the shared `agents/`
and `resources/` directories.

## Support Status & Contributing Other Harnesses

Our initial release officially supports **Antigravity** and **Gemini CLI**.
**Claude Code** and **Claude Desktop** packaging is in place; end-to-end
verification of `/egm-brainstorm`, `/egm-draft`, and `/egm-review` is pending. We welcome
contributors who want to help add and verify support for other agent harnesses!

### Contributing Support for New Harnesses

A harness counts as supported after `/egm-brainstorm`, `/egm-draft`, and
`/egm-review` run end to end through its plugin install. When contributing
support for another harness:

1. Add the appropriate manifest or configuration file to the repository root
   (e.g., matching the harness's plugin/extension standard).
2. Document install steps, manifest mapping, and delegation mechanics in this guide
   (`docs/harnesses.md`).
3. Verify that `/egm-brainstorm`, `/egm-draft`, and `/egm-review` run end to end,
   and attach verification notes or execution transcripts in your Pull Request description
   (as outlined in the [Pull Request Template](../.github/PULL_REQUEST_TEMPLATE.md)).
