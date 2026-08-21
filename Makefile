SHELL := /bin/sh
R0A := ./tools/build/r0a.sh
R0B := ./tools/build/r0b.sh

.PHONY: r0a-bootstrap r0a-generate r0a-host-test r0a-build r0a-xemu r0a-evidence r0a-verify r0a-clean r0b-bootstrap r0b-generate r0b-host-test r0b-build r0b-xemu r0b-evidence r0b-verify r0b-clean r0b-fcm-safe-build r0b-fcm-safe-xemu r0b-fcm-visible-build r0b-fcm-visible-xemu r0b-d031-safe-build r0b-d031-safe-xemu r0b-final-build r0b-final-xemu
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
