#!/bin/bash

for DIR in 'agents' 'checkman' 'checks' 'doc' 'inventory' 'notifications' 'pnp-templates' 'web'; do
    rm -rfv $OMD_ROOT/local/share/check_mk/$DIR
    ln -sv $WORKSPACE/$DIR $OMD_ROOT/local/share/check_mk/$DIR
done;

mkdir -p $OMD_ROOT/local/lib/check_mk/gui/plugins/wato/
mkdir -p $OMD_ROOT/local/lib/check_mk/gui/plugins/wato/check_parameters
ln -sv $WORKSPACE/agent_based_check_parameters $OMD_ROOT/local/lib/check_mk/gui/plugins/wato/check_parameters

ln -sv $WORKSPACE/lib/python3/labelpicker $OMD_ROOT/local/lib/python3/labelpicker

rm -rfv $OMD_ROOT/local/bin
ln -sv $WORKSPACE/bin $OMD_ROOT/local/bin

# Reset password of default user
source /omd/sites/cmk/.profile && echo 'cmkadmin' | /omd/sites/cmk/bin/cmk-passwd -i cmkadmin