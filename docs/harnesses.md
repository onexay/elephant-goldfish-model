# Harnesses

EGM is one set of skills and personas. This repository serves as the
plugin source for each supported harness. No harness gets a fork of the skill
text.

## Install

| Harness | Install |
| --- | --- |
| Antigravity | `/plugin`, then install from `https://github.com/google/elephant-goldfish-model` |
| Gemini CLI | `gemini extensions install https://github.com/google/elephant-goldfish-model` |
| Claude Code | `/plugin marketplace add onexay/elephant-goldfish-model`, then `/plugin install egm@elephant-goldfish-model` |
| Claude Desktop (Cowork) | Customize > Plugins > Add marketplace, enter `onexay/elephant-goldfish-model`, then install `egm` |
| Codex | `codex plugin marketplace add onexay/elephant-goldfish-model`, then `codex plugin add egm@elephant-goldfish-model` |

Install the whole plugin. Skill-only installers that copy `skills/` alone
break EGM, because the skills read `agents/` and
`resources/document_standards/` at run time.

## Manifests

| Harness | Manifest | Skills | Subagents |
| --- | --- | --- | --- |
| Antigravity | `plugin.json` | `skills/` (default) | `agents/` (default) |
| Gemini CLI | `gemini-extension.json` | `skills/` (default) | `agents/` (default) |
| Claude Code, Claude Desktop | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` | `skills/` (default) | `agents/` (default) |
| Codex | `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json` | `skills/` | Not registered; personas are read from `agents/` |

Persona prompts live in `agents/`, the directory Antigravity, Gemini CLI, and
Claude Code scan for subagents. Each persona has `name` and `description` frontmatter, so
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
| Codex | `spawn_agent` with `fork_turns: "none"` | No | Yes |

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
`omitAgentsMd: true` to keep `AGENTS.md` out of reviewer context, but no
supported harness reads this key: Claude Code never loads `AGENTS.md`, and
Codex loads it regardless (see [Codex](#codex)). The synthesizer and bootstrap orchestrator keep the files. Isolation covers
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

## Codex

EGM runs in Codex, but its Goldfish reviews are less isolated than in Claude
Code: reviewers start fresh only when the skill passes `fork_turns: "none"`,
they load `AGENTS.md`, and personas are read from a file rather than loaded as
subagent types. The details follow.

Codex names the skills `egm:egm-brainstorm`, `egm:egm-draft`,
`egm:egm-review`, and so on. Invoke one by mentioning it, for example
`$egm:egm-review docs/designs/<feature>.md`, or pick it from `/skills`. Each
skill ships `agents/openai.yaml` with `policy.allow_implicit_invocation: false`,
the Codex counterpart of `disable-model-invocation`, so Codex never starts an
EGM skill on its own.

Codex does not register the personas in `agents/` as subagent types. Skills
spawn a general-purpose subagent with `spawn_agent` and tell it to read the
persona file. Every Goldfish spawn must set `fork_turns` to `"none"`: when
`fork_turns` is omitted, Codex copies the parent conversation into the subagent.

Codex has no plugin-root variable for skill text. The skills resolve
`agents/`, `resources/`, and `skills/` from the installed `SKILL.md` path: the
plugin root is three directories above it.

Codex subagents load the project's `AGENTS.md` even with `fork_turns: "none"`.
The `omitClaudeMd` and `omitAgentsMd` persona keys have no effect in Codex, and
it offers no per-subagent way to skip `AGENTS.md`. Keep design-specific
context out of `AGENTS.md` if you want reviews free of it.

`codex exec` has no question tool, so gates fall back to plain chat.

To test a local checkout without touching your Codex setup, install it into a
throwaway Codex home. Codex copies the plugin into its cache at install time, so
re-run `codex plugin add` after each change:

```bash
export CODEX_HOME=$(mktemp -d)
ln -s ~/.codex/auth.json "$CODEX_HOME/auth.json"
codex plugin marketplace add /path/to/elephant-goldfish-model
codex plugin add egm@elephant-goldfish-model
```

## Support Status & Contributing Other Harnesses

Our initial release officially supports **Antigravity** and **Gemini CLI**.

**Claude Code**, **Claude Desktop**, and **Codex** packaging is in place. Stage 5
of `/egm-review` (Initial Zoom Out) has run end to end from the plugin in
Claude Code and Codex, with the reviewer in a fresh subagent and the report
written to the project. Full runs of `/egm-brainstorm`, `/egm-draft`, and
`/egm-review`, and any run in Claude Desktop, are not yet verified.

We welcome contributors who want to help add and verify support for other agent
harnesses!

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
