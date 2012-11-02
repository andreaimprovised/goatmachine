usbstick:
	cp -rf . $(usb-dir)
	cp -r $(selenium-dir) $(usb-dir)
	cat config.py | sed "s|DRY_RUN = True|DRY_RUN = False|" > $(usb-dir)/config.py

clean:
	rm -rf *.py[co]
