---
name: Quarkus
category: framework
update:
  versions:
    method: GITHUB
    owner: quarkusio
    repo: quarkus
  
---

> [Quarkus: Supersonic Subatomic Java.](https://quarkus.io/) A Kubernetes Native Java stack tailored for OpenJDK HotSpot
> and GraalVM, crafted from the best of breed Java libraries and standards.

The Quarkus team releases a `major.minor` version every 4 to 6 weeks, and a fix version targeting the latest version
every week in between. Every `major.minor` version
[deprecates the previous version](https://github.com/quarkusio/quarkus/discussions/29161) and there is no LTS versions.
See [Quarkus Roadmap/planning](https://github.com/orgs/quarkusio/projects/13) for upcoming releases and features.

If you need additional guarantees you can take a look at
the [Red Hat build of Quarkus (RHBQ)](https://access.redhat.com/products/quarkus). The code base used for this build is
the same as the one used for the community version, but it comes with support,
a [slower release cadence](https://access.redhat.com/support/policy/updates/jboss_notes#p_quarkus),
and [certified builds of Quarkus its dependencies](https://code.quarkus.redhat.com/). The Red Hat build of Quarkus
requires a Red Hat subscription to run in production.
