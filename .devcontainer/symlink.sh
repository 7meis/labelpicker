#!/bin/bash

rm -rfv $OMD_ROOT/local/lib/python3/labelpicker
ln -sv $WORKSPACE/lib/python3/labelpicker $OMD_ROOT/local/lib/python3/labelpicker

rm -rfv $OMD_ROOT/local/bin
ln -sv $WORKSPACE/bin $OMD_ROOT/local/bin

# Reset password of default user
htpasswd -b $OMD_ROOT/etc/htpasswd cmkadmin cmkadmin