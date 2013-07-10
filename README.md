recon-stats
===============

Python package to parse stats from recon-all. Given a Freesurfer subject, this flattens all of the stats files into a single python dictionary. It'd be very easy to upload this dictionary to REDCap, for example.

Why?
----

Freesurfer outputs too much data to import it by hand into REDCap. So I scratched an itch.

Usage
-----

I use this package in my code the following way:

``` python
from recon_stats import Subject
s = Subject('SUBJECTID') # where SUBJECTID is in your SUBJECTS_DIR

# load measures
s.get_measures()

# produce a dictionary
data = s.upload_dict()

# Then using pycap, upload the data quickly
from redcap import Project
p = Project(URL, TOKEN)
data[p.def_field] = 'SUBJECTID' # or however this subject is indexed in your REDCap

response = p.import_records([data])
```

Boom

The above won't actually work until you've got all ~2655 fields in your REDCap data dictionary. Search for "Freesurfer Reconstruction Stats" in the Shared Library and download it into your project. Then you're good to go with the above.


Questions/Comments?
-------------------

Submit an issue, fork and PR, etc.

I'm [@scottsburns](https://twitter.com/scottsburns) on twitter.
