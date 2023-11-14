# This script is used to update the version of jQuery that is packaged in
# sweetviz/templates/js. It downloads jquery-x.x.x-min.js from the official
# jQuery CDN, updates the specified version in the files that import it
# (currently only sweetviz/templates/dataframe_page.html), and deletes the
# old version.

# This should be run from the root sweetviz directory, as the file operations
# are relative to root. The only things that should need to be updated each
# time are the old_version and new_version variables.

import urllib.request
from os import remove

# Set the old version and the new version
old_version = "3.4.1"
new_version = "3.7.1"

# Set filenames and the CDN URL
old_jquery_filename = f"jquery-{old_version}.min.js"
new_jquery_filename = f"jquery-{new_version}.min.js"
url = f"https://code.jquery.com/{new_jquery_filename}"

try:
    # Download and save minified jQuery
    urllib.request.urlretrieve(url, f"sweetviz/templates/js/{new_jquery_filename}")

    # Find and replace all instances of importing the old version of jQuery
    dataframe_page = "sweetviz/templates/dataframe_page.html"
    with open(dataframe_page) as file:
        filedata = file.read()

    filedata = filedata.replace(old_jquery_filename, new_jquery_filename)

    with open(dataframe_page, "w") as file:
        file.write(filedata)

    # Delete the old version of jQuery
    remove(f"sweetviz/templates/js/{old_jquery_filename}")

except Exception as ex:
    print("Error in updating jQuery; old version not replaced.")
    print(ex)
