# How do I build this app?
Look into the [Makefile](Makefile) and you will see all make targets documented. Below are some of the main ones

## Build the RPM
Runs the `pip install` which pulls all python dependencies, creates the required RPMS SRPMS and SOURCES directories, zips up the sources and then invokes `mock-build` to build the actual RPM
```
$ make local
```

## Build the RPM and post the release to Cosmos
Runs the make target above to build the RPMs and then uses `cosmos-release` to publish the packages to the repo service and send the release metadata to Cosmos
```
$ make release
```
