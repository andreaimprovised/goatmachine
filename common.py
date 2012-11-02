import os
import platform

firefox_profile_locations = {
	'Darwin': os.path.expanduser(
		os.path.join(
			'~',
			'Library',
			'Application Support',
			'Firefox',
			'Profiles',
		)
	),
	'Linux': os.path.expanduser(
		os.path.join(
			'~',
			'.mozilla',
			'firefox'
		)
	)
}

chrome_cookies_locations = {
	'Darwin': os.path.expanduser(
		os.path.join(
			'~',
			'Library',
			'Application Support',
			'Google',
			'Chrome',
			'Default',
			'Cookies'
		)
	),
	'Linux': os.path.expanduser(
		os.path.join(
			'~',
			'.config',
			'google-chrome',
			'Default',
			'Cookies'
		)
	)
}

def get_firefox_profile_path():
	root = firefox_profile_locations[platform.system()]
	profiles_path = os.path.join(os.environ.get("HOME"), root)
	profile_path = None

	uname = os.environ.get("USER")

	if profiles_path is None:
		raise LookupError("Could not find a profile for firefox!")

	for path in os.listdir(profiles_path):
		if "default" in path:
			profile_path = path
			break
		elif uname in path:
			profile_path = path
			break
	return os.path.join(profiles_path, profile_path)

def get_chrome_cookies_path():
	return chrome_cookies_locations[platform.system()]

