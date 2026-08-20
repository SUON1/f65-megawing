SHELL := /bin/sh
R0A := ./tools/build/r0a.sh

.PHONY: r0a-bootstrap r0a-generate r0a-host-test r0a-build r0a-xemu r0a-evidence r0a-verify r0a-clean
r0a-bootstrap: ; $(R0A) bootstrap
r0a-generate: ; $(R0A) generate
r0a-host-test: ; $(R0A) host-test
r0a-build: ; $(R0A) build
r0a-xemu: ; $(R0A) xemu
r0a-evidence: ; $(R0A) evidence
r0a-verify: ; $(R0A) verify
r0a-clean: ; $(R0A) clean
