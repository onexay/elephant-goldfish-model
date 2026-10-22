# Elephant-Goldfish Model (EGM)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Website](https://img.shields.io/badge/Website-egm.dev-black.svg)](https://egm.dev)

Elephant-Goldfish Model is an open-source framework and methodology for Spec-Driven Development (SDD) with autonomous AI coding agents.

It anchors development in context-rich system descriptions and adversarial multi-agent reviews, making complex codebases easier for both humans and AI to navigate, verify, and evolve.

---

## Philosophy

EGM uses two animal metaphors to describe how to prompt, constrain, and structure AI agents at different stages of the software development lifecycle:

*   🐘 **The Elephant (Remembers Everything)**:
    Deep-context agents loaded with system history, architecture diagrams, component boundaries, and user journeys. The Elephant conducts structured brainstorming, probes operational limits, and drafts comprehensive specifications.
*   🐠 **The Goldfish (Zero-Context Memory)**:
    Stateless, isolated subagents that read only the draft design specification and live source code without access to conversational bias. The Goldfish swarm subjects designs to adversarial stress-testing across multiple conflicting perspectives (Design Critic, Naive Reader, Tech Lead, Codebase Auditor, Structural Validator, Style Editor, and Zoom Out Architect; defined under `agents/`).
*   🧑‍💻 **The Human (Owns the Outcomes)**:
    AI is an exploration partner and automated auditor, but human engineers own architectural decisions, trade-offs, and final outcomes.

For the foundational essay introducing this methodology, see Dave Rensin's article: [Elephants, Goldfish, and the New Golden Age of Software Engineering](https://medium.com/@drensin/elephants-goldfish-and-the-new-golden-age-of-software-engineering-c33641a48874).

---

## Repo Structure

```
├── agents/                       # Stateless reviewer and orchestrator persona prompts
├── docs/                         # Documentation, guides, and FAQ
│   └── designs/                  # Living technical design specifications
├── resources/
│   └── document_standards/       # Quality evaluation rubrics and standards
├── skills/                       # Modular agent skills (Brainstorm, Draft, Review, etc.)
└── tests/
    └── evals/                    # Automated YAML evaluation benchmarks
```

---

## Skills

| Skill | Command | Description |
| :---- | :------ | :---------- |
| **Brainstorm** | `/egm-brainstorm` | Zero-doc ideation tool using a multi-lens Goldfish shootdown swarm to stress-test early concepts. |
| **Draft** | `/egm-draft` | Iterative, section-by-section markdown design specification compiler. |
| **Review** | `/egm-review` | Multi-stage verification pipeline orchestrator (Zoom Out → Comprehension → Critic → Readiness). |
| **Review Loop** | `/egm-review-loop` | Concurrent review subagent dispatch engine supporting direct and hierarchical dispatch. |
| **Review Resolve** | `/egm-resolve` | Interactive triage and automated patch application engine for review findings. |
| **Drift Report** | `/egm-drift-report` | Sequential AST scanner detecting divergence between checked-in specs and live code. |
| **Bootstrap** | `/egm-bootstrap` | Recursive bottom-up codebase documentation generator and sentinel-block upserting engine. |

---

## Quickstart

Install EGM as a plugin from this fork:

*   **Claude Code (CLI)**:

    ```
    /plugin marketplace add onexay/elephant-goldfish-model
    /plugin install egm@elephant-goldfish-model
    ```

*   **Claude Desktop**: In Cowork, open Customize > Plugins > Add marketplace, enter `onexay/elephant-goldfish-model`, then install `egm`.
*   **Codex**:

    ```
    codex plugin marketplace add onexay/elephant-goldfish-model
    codex plugin add egm@elephant-goldfish-model
    ```

    In Codex, invoke skills by mention, for example `$egm:egm-review`.

Claude namespaces the commands below: `/egm-review` is also available as `/egm:egm-review`. For other harnesses, see [Harnesses](docs/harnesses.md).

1.  **Ideate & Stress-Test**:
    Run `/egm-brainstorm` to explore problem boundaries and subject raw concepts to a multi-lens Goldfish shootdown swarm.
2.  **Draft**:
    Run `/egm-draft` to convert the egm-brainstorm output (a concept brief) into a living design document under `docs/designs/<feature>.md` (or user designated directory).
3.  **Review & Resolve**:
    Run `/egm-review docs/designs/<feature>.md` to launch the multi-stage Goldfish reviewer swarm on the design document produced by egm-draft (interactive resolution via `/egm-resolve` is integrated directly into the review loop).
4.  **Submit & Implement**:
    Submit the verified design doc via Pull Request, and implement code against the approved specification.

For detailed setup, supported harnesses (**Antigravity**, **Gemini CLI**, and **Claude Code** / **Claude Desktop**), and walkthroughs, see [Getting Started](docs/getting_started.md), [Harnesses](docs/harnesses.md), and the [Framework Architecture](docs/designs/architecture.md).

---

## Contributing

We welcome community contributions! Please review [Harnesses](docs/harnesses.md) and our [Contribution Guidelines](CONTRIBUTING.md) before submitting pull requests.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

This is not an officially supported Google product.
