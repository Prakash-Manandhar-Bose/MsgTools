all :: *.py
	pylint $< -rn --rcfile=$(BUILDROOT)/.pylintrc