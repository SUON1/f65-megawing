SHELL := /bin/sh
R0A := ./tools/build/r0a.sh
R0B := ./tools/build/r0b.sh
R0C := ./tools/build/r0c.sh
R0D := ./tools/build/r0d.sh

.PHONY: r0a-bootstrap r0a-generate r0a-host-test r0a-build r0a-xemu r0a-evidence r0a-verify r0a-clean r0b-bootstrap r0b-generate r0b-host-test r0b-build r0b-xemu r0b-evidence r0b-verify r0b-clean r0b-fcm-safe-build r0b-fcm-safe-xemu r0b-fcm-visible-build r0b-fcm-visible-xemu r0b-d031-safe-build r0b-d031-safe-xemu r0b-final-build r0b-final-xemu r0c-bootstrap r0c-generate r0c-host-test r0c-build r0c-xemu r0c-evidence r0c-verify r0c-clean r0d-bootstrap r0d-generate r0d-host-test r0d-build r0d-verify r0d-clean
r0a-bootstrap: ; $(R0A) bootstrap
r0a-generate: ; $(R0A) generate
r0a-host-test: ; $(R0A) host-test
r0a-build: ; $(R0A) build
r0a-xemu: ; $(R0A) xemu
r0a-evidence: ; $(R0A) evidence
r0a-verify: ; $(R0A) verify
r0a-clean: ; $(R0A) clean
r0b-bootstrap: ; $(R0B) bootstrap
r0b-generate: ; $(R0B) generate
r0b-host-test: ; $(R0B) host-test
r0b-build: ; $(R0B) build
r0b-xemu: ; $(R0B) xemu
r0b-evidence: ; $(R0B) evidence
r0b-verify: ; $(R0B) verify
r0b-clean: ; $(R0B) clean
r0b-fcm-safe-build: ; $(R0B) fcm-safe-build
r0b-fcm-safe-xemu: ; $(R0B) fcm-safe-xemu
r0b-fcm-visible-build: ; $(R0B) fcm-visible-build
r0b-fcm-visible-xemu: ; $(R0B) fcm-visible-xemu
r0b-d031-safe-build: ; $(R0B) d031-safe-build
r0b-d031-safe-xemu: ; $(R0B) d031-safe-xemu
r0b-final-build: ; $(R0B) final-build
r0b-final-xemu: ; $(R0B) final-xemu
r0c-bootstrap: ; $(R0C) bootstrap
r0c-generate: ; $(R0C) generate
r0c-host-test: ; $(R0C) host-test
r0c-build: ; $(R0C) build
r0c-xemu: ; $(R0C) xemu
r0c-evidence: ; $(R0C) evidence
r0c-verify: ; $(R0C) verify
r0c-clean: ; $(R0C) clean
r0d-bootstrap: ; $(R0D) bootstrap
r0d-generate: ; $(R0D) generate
r0d-host-test: ; $(R0D) host-test
r0d-build: ; $(R0D) build
r0d-verify: ; $(R0D) verify
r0d-clean: ; $(R0D) clean
