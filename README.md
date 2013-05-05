PMIS
====

Codebase for the DPWRT PMIS application (how's that for a mouthful?)

Requirements
------------

You are required to have ansible (and all its dependencies) and vagrant both
installed.

If you run bin/install.sh from the root folder, good things should happen.
It sets up ansible and vagrant.

Verify this is the base box you want before running install.sh:

    vagrant box add base http://files.vagrantup.com/precise64.box

The first time around it might take some time, as vagrant will have to
download the VM image. Be patient!

Installation
------------------

You can create the VM with:

    vagrant up

Once the VM is created, it will automatically provision the application.

Should you want to repeat the provision:

    vagrant provision

Should the machine install completely without error, browse to (http://localhost:8080/)

Once you are happy with the state of the machine, you can package it:

    vagrant package --vagrantfile Vagrantfile.pkg

This leaves you with package.box, which captures the state of the machine for use later:

    vagrant box add project package.box
    vagrant init project
    vagrant up
