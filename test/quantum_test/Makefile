all: sanity unit validate-modules-unit

.PHONY: sanity
sanity:
	$(abspath ${CURDIR}/../../bin/quantum-test) sanity test/lib/ ${FLAGS}

.PHONY: unit
unit:
	PYTHONPATH=$(abspath ${CURDIR}/../lib) pytest unit ${FLAGS}

.PHONY: validate-modules-unit
validate-modules-unit:
	PYTHONPATH=$(abspath ${CURDIR}/../lib/quantum_test/_data/sanity/validate-modules):$(abspath ${CURDIR}/../../lib) pytest validate-modules-unit ${FLAGS}
