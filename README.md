# Intel Xeon 6 201: Building an AI Agent

Canonical Showroom source for the RHDP Publishing House migration of the
45-minute Intel Xeon 6 201 lab.

Learners deploy a lightweight solution-advisor stack in their assigned
OpenShift namespace, connect three MCP tools, and use an automatically assigned
RACMaaS virtual key for CPU inference on Intel Xeon 6.

## Repository roles

- This repository owns the learner-facing Showroom content and configuration.
- [`rhpds/triforce`](https://github.com/rhpds/triforce) remains the implementation
  repository for the application services and deployment manifests.
- The lab's executable manifest URLs are pinned to Triforce commit
  [`f484cb66c3dcddff323df8814f637dc92c73c179`](https://github.com/rhpds/triforce/commit/f484cb66c3dcddff323df8814f637dc92c73c179),
  the commit referenced by release `201-v1.0.0` at review time.

## Publishing House migration

Use this public repository as the source repository for the Publishing House
Migration template. Its `main` branch uses the paths expected by the importer:

- `content/`
- `site.yml`
- `ui-config.yml`

The intended Publishing House settings are:

- content type: `lab`
- deployment mode: `rhdp_published`
- Showroom type: `classic`
- automation type: `ansible`
- initiative: `none`, unless assigned to a named RHDP initiative

## Safety and validation

Workshop recommendations are illustrative, not validated customer sizing.
Learners must not enter confidential, regulated, export-controlled, or
customer-identifying information.

Maintainer: Jonathan Kershaw (`jkershaw@redhat.com`)
