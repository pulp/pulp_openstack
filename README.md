![build status](https://api.travis-ci.org/pulp/pulp_openstack.png?branch=master)

pulp_openstack
==============

pulp_openstack is a Pulp plugin to work with Openstack. It is currently planned
to be used to push VM images to glance.

# example usage

## create a repo
```
# pulp-admin openstack repo create --repo-id openstack-repo
Repository [openstack-repo] successfully created
```

## upload an image
```
# pulp-admin openstack repo uploads upload -f cirros-0.3.2-i386-disk.img --repo-id openstack-repo
+----------------------------------------------------------------------+
                              Unit Upload
+----------------------------------------------------------------------+

Extracting necessary metadata for each request...
[==================================================] 100%
Analyzing: cirros-0.3.2-i386-disk.img
... completed

Creating upload requests on the server...
[==================================================] 100%
Initializing: cirros-0.3.2-i386-disk.img
... completed

Starting upload of selected units. If this process is stopped through ctrl+c,
the uploads will be paused and may be resumed later using the resume command or
cancelled entirely using the cancel command.

Uploading: cirros-0.3.2-i386-disk.img
[==================================================] 100%
12336128/12336128 bytes
... completed

Importing into the repository...
This command may be exited via ctrl+c without affecting the request.


[\]
Running...

Task Succeeded


Deleting the upload request...
... completed
```

## list images
```
# pulp-admin openstack repo list
+----------------------------------------------------------------------+
                         Openstack Repositories
+----------------------------------------------------------------------+

Id:                  openstack-repo
Display Name:        openstack-repo
Description:         None
Content Unit Counts: 
  Openstack Image: 1

```

## delete a repo
```
# pulp-admin openstack repo delete --repo-id openstack-repo
This command may be exited via ctrl+c without affecting the request.


[\]
Running...

Repository [openstack-repo] successfully deleted
```
