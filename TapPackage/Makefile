rename: Tap.pex
	mv Tap.pex Tap
Tap.pex:
	python setup.py bdist_wheel
	python -m pex -r requirements.txt ./dist/gdtap-1.1-py2-none-any.whl -e gdtap.run:runit -o Tap.pex
clean:
	rm -r ./*.egg-info ./build ./dist