usbstick:
	rm -rf $(usb-dir)/*
	cp -r . $(usb-dir)
	cp -r $(selenium-dir) $(usb-dir)
	cat $(usb-dir)/config.py | sed "s/DRY_RUN = True/DRY_RUN = False/" > $(usb-dir)/config.py

clean:
	rm -rf *.py[co]