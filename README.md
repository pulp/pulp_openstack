![build status](https://api.travis-ci.org/pulp/pulp_openstack.png?branch=master)

pulp_openstack
==============

pulp_openstack is a Pulp plugin to work with Openstack. Currently you can use
it to push images into Glance from Pulp.


# setup

You need to create an RDO instance, see http://openstack.redhat.com/Main_Page.
A Fedora 20 VM with 3GB memory and 12GB disk works fine for test purposes.

After RDO is set up, admin credentials are in `/root/openrc_admin`.

# example usage

## create a repo
```
# pulp-admin openstack repo create --repo-id openstack-repo --display-name "openstack repo" --keystone-username <username> --keystone-password <password> --keystone-tenant <tenant> --keystone-url <auth url>
Repository [openstack-repo] successfully created
```

## upload an image
```
# pulp-admin openstack repo uploads upload -f cirros-0.3.2-i386-disk.img --repo-id openstack-repo --name "cirros image"
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

## publish to glance

```
# pulp-admin openstack repo publish glance run --repo-id openstack-repo
+----------------------------------------------------------------------+
                    Publishing Repository [openstack-repo]
+----------------------------------------------------------------------+

This command may be exited via ctrl+c without affecting the request.


Publishing Image Files.
[-]
... completed


Task Succeeded

```

## verify image is in glance

```
# source keystonerc_admin

# glance image-list
+--------------------------------------+--------------+-------------+------------------+----------+--------+
| ID                                   | Name         | Disk Format | Container Format | Size     | Status |
+--------------------------------------+--------------+-------------+------------------+----------+--------+
| b4169977-4403-4f72-9dcb-989c317199d2 | cirros image | qcow2       | bare             | 13167616 | active |
+--------------------------------------+--------------+-------------+------------------+----------+--------+

```


## delete a repo
```
# pulp-admin openstack repo delete --repo-id openstack-repo
This command may be exited via ctrl+c without affecting the request.


[\]
Running...

Repository [openstack-repo] successfully deleted
```
