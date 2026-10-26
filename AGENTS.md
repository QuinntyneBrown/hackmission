# Agent instructions for HackMission

## Purpose

> HackMission is a platform for a Christian hackathon that happens many times a year. The platform uses .NET on the backend and Angular on the frontend.

HackMission brings developers, designers, and mission-driven organizations together for recurring 48-hour events that build tools for churches, charities, and communities. The public site introduces events and manages consent-based mailing-list subscriptions; the product will grow to support participants, organizers, projects, and partner organizations.

The product is defined before code by `docs/journeys.md`, `docs/specs/`, `docs/mocks/`, `docs/design-system/`, `docs/detailed-designs/`, and `docs/estimates/`. Architecture decisions live in `docs/adr/`.

## Repository layout (MANDATORY)

**This folder structure and its contents are mandatory. It is a mandate, not a suggestion.**

- Every file MUST go in the folder this tree assigns it. If no folder fits, stop and ask; do not guess or improvise.
- Do NOT create top-level folders, projects, libraries, or alternative layouts not in this tree.
- Do NOT move, rename, or merge folders or projects in this tree.
- The tree changes only with explicit user approval. Update this section in the same change, before putting code in a new location.

```text
hackmission/
├── AGENTS.md, CLAUDE.md, GEMINI.md              # Agent instructions; AGENTS.md is authoritative
├── README.md                                    # Product overview and development commands
├── LICENSE                                      # MIT License
├── CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, SUPPORT.md
├── CHANGELOG.md                                 # Notable release history
├── .agents/skills/, .claude/skills/             # Shared agent skills and Claude Code skills
├── .github/
│   ├── workflows/                               # CI: build, test, lint, format
│   ├── ISSUE_TEMPLATE/                          # Bug report and feature request templates
│   ├── pull_request_template.md
│   └── copilot-instructions.md                  # Pointer to AGENTS.md
├── backend/                                     # .NET solution
│   ├── HackMission.sln
│   ├── Directory.Build.props, Directory.Packages.props, global.json
│   ├── deploy/                                  # Dockerfiles and local compose configuration
│   ├── src/
│   │   ├── HackMission.Domain/                  # Entities and value objects; zero dependencies
│   │   ├── HackMission.Application/             # Handlers, validators, DTOs, permissions
│   │   ├── HackMission.Infrastructure/          # EF Core, migrations, email, storage, auth, seeding
│   │   ├── HackMission.Api/                     # Endpoints, DI, middleware; no business logic
│   │   └── HackMission.Cli/                     # Explicit migrate, seed, and reset commands
│   └── tests/                                   # Application, Infrastructure, API, and CLI tests
├── frontend/                                    # Angular workspace
│   ├── angular.json, package.json, eslint.config.js, .prettierrc
│   └── projects/
│       ├── hackmission/                         # Application shell and lazy top-level routes only
│       ├── api/                                 # Typed API client, contracts, auth, interceptors
│       ├── components/                          # Shared design-system components and tokens
│       ├── marketing/                           # Public site, mailing list, privacy, unsubscribe
│       ├── account/                             # Sign-in, invitations, and profile
│       ├── events/                              # Event discovery, registration, schedules
│       ├── projects/                            # Challenges, teams, projects, demos
│       ├── organizations/                       # Partner organization and challenge management
│       └── administration/                      # Event operations, roles, settings
├── e2e/                                         # Playwright suite (Chromium only): pages, fixtures, tests
├── eng/                                         # Developer, CI, deployment, and infrastructure scripts
├── tools/                                       # Video narration, build, and screen-recording tooling
└── docs/
    ├── journeys.md                              # Personas and user journeys, ordered by value
    ├── specs/                                   # L1/L2 requirements and acceptance criteria
    ├── mocks/                                   # Static HTML mocks: visual reference
    ├── design-system/                           # Tokens, assets, components, patterns from mocks
    ├── screen-composition.md                    # Required library/local composition per screen
    ├── detailed-designs/                        # Per-subsystem and feature designs and diagrams
    ├── estimates/                               # Effort and percent complete per design
    ├── adr/                                     # Architecture decision records (NNNN-title.md)
    ├── prompts/                                 # Ready-to-run implementation prompts
    └── videos/                                  # Narrated videos and shared assets
```

Every feature uses the same name in `backend/src/HackMission.Application/`, `frontend/projects/`, `docs/specs/`, `docs/detailed-designs/`, `docs/estimates/`, and `e2e/tests/` (case may differ only by platform convention).

## Architecture rules

- Business rules live in application handlers and domain services, never endpoints or controllers.
- Endpoints require authentication by default; anonymous access is explicit, including public marketing, mailing-list, confirmation, unsubscribe, and privacy flows.
- Every server query and endpoint enforces permissions. Never use hidden UI as authorization.
- EF Core migrations live only in `HackMission.Infrastructure/Persistence/Migrations/`; the API never applies them at startup. The CLI applies migrations and runs idempotent seeds.
- Keep secrets out of the repository; use configuration and environment variables.
- Read relevant ADRs before changing an area they cover.

## Components library is mandatory (CRITICAL)

Every UI component defined in `docs/design-system/` MUST be implemented once in `frontend/projects/components/` and reused everywhere.

- Feature libraries and the app compose screens from the components library. Do not create, copy, restyle, or wrap a design-system component locally.
- If a needed component, variant, or state is missing, update the design system and the components library first.
- Feature libraries contain feature-specific pages, routes, dialogs, and API-to-component glue only.
- `components` never depends on `api`, the app, or a feature library; it makes no HTTP calls.
- Use design tokens by role, never literal hex values. Meet WCAG 2.2 AA: keyboard access, visible focus, labelled controls, and sufficient contrast.
- Use Angular CDK Dialog/Overlay for modal behavior. Do not hand-roll modal mechanics.
- Feature libraries depend only on `api` and `components`, never on one another. The app lazy-loads feature route tables.
- API services expose a contract and injection token; pages depend on the token, not a concrete HTTP service. Only `projects/api/` calls `HttpClient`.

## Code, testing, and delivery

- One backend type per file. Angular components have separate `.ts`, `.html`, and, when needed, `.css` files; do not use inline templates or styles.
- Prettier owns frontend formatting and angular-eslint owns frontend linting; CI fails on either.
- .NET tests live only in `backend/tests/`; Angular unit tests live beside the code they cover; Playwright tests live only in `e2e/` and use Chromium.
- Playwright tests use the Page Object Model: page objects own selectors and interactions; tests state intent.
- Test behavior, not repository shape. Do not add architecture, layout, naming, or banned-API tests.
- Every production behavior change needs a requirement, detailed design, and mock before implementation. Implement in small acceptance-test-driven slices: write Given-When-Then criteria and a failing acceptance test first, make it pass, refactor with checks green, then continue. Documentation-only, mock-only, design-system-only, and test-only work skips inapplicable steps.
- Record architectural or scope decisions as ADRs in `docs/adr/`.
