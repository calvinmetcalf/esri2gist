esri2couch
==========
takes a file, a url for a couchdb,  the location of your
[esri2open](https://github.com/project-open-data/esri2open) toolbox and an
optional login of the form username:password.  If you use that your going
to want to make sure to put https in the name of your couch. There is a
box you can check to create the DB it only does anything if you've filled in
your authentication. A design document is created with a preview of your layer
viewable at http://your.couch.com/dbname/_design/geojson/_rewrite/ viewing this for
larger layers can crash your browsers FYI