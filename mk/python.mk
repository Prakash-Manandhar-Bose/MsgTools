all :: *.py
	pylint $< -rn --rcfile=$(BUILDROOT)/.pylintrc --init-hook="sys.path.append('$(BUILDROOT)/MsgApp')"