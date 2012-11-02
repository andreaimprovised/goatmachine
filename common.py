import os
import platform

firefox_profile_locations = {
	'darwin': "Library/Application Support/Firefox/Profiles/",
	'linux': ".mozilla/firefox/"
}

def get_firefox_profile_path():
	root = firefox_profile_locations[platform.system()]
	profiles_path = os.path.join(os.environ.get("HOME"), root)
	profile_path = None

	uname = os.environ.get("USER")

	if profile_path is None:
		raise LookupError("Could not find a profile for firefox!")

	for path in os.listdir(profiles_path):
		if "default" in path:
			profile_path = path
			break
		elif uname in path:
			profile_path = path
			break
