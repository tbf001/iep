#!/usr/bin/python
import sys
import time
import time
import atexit
import argparse
import getpass
import requests
requests.packages.urllib3.disable_warnings()

import ssl

try:
	_create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
	# Legacy Python that doesn't verify HTTPS certificates by default
	pass
else:
 # Handle target environment that doesn't support HTTPS verification
	ssl._create_default_https_context = _create_unverified_https_context
system = sys.argv[1]

from pyVmomi import vim, vmodl
from pyVim import connect
from pyVim.connect import Disconnect, SmartConnect, GetSi


inputs = {'vcenter_ip': '3gbv1apvmw1001.national.core.bbc.co.uk',
          'vcenter_password': 'W@shed5ocks!',
          'vcenter_user': 'ere-mid-tf@national',
          'vm_name': '3gbbmapfbd6001',
          'datastore_iso_path': '[TS S1 DS BACKUP]ISOs/ansible/WinInstall.iso'
	 }


def get_obj(content, vimtype, name):
    """
     Get the vsphere object associated with a given text name
    """
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


def wait_for_task(task, actionName='job', hideResult=False):
    """
    Waits and provides updates on a vSphere task
    """

    while task.info.state == vim.TaskInfo.State.running:
        time.sleep(2)

    if task.info.state == vim.TaskInfo.State.success:
        if task.info.result is not None and not hideResult:
            out = '%s completed successfully, result: %s' % (actionName, task.info.result)
            print out
        else:
            out = '%s completed successfully.' % actionName
            print out
    else:
        out = '%s did not complete successfully: %s' % (actionName, task.info.error)
        raise task.info.error
        print out

    return task.info.result


def main():

    try:
        si = None
        try:
            print "Trying to connect to VCENTER SERVER . . ."
            si = connect.Connect(inputs['vcenter_ip'], 443, inputs['vcenter_user'], inputs['vcenter_password'], version = "vim.version.version8")
        except IOError, e:
            pass
            atexit.register(Disconnect, si)

        print "Connected to VCENTER SERVER !"

        content = si.RetrieveContent()

        vm_name = inputs['vm_name']
        vm = get_obj(content, [vim.VirtualMachine], vm_name)

        print "Attaching iso to CD drive of ", vm_name
        vmconf = vim.vm.ConfigSpec()
     #   vmconf.deviceChange = [cdspec]
        print "Giving first priority for CDrom Device in boot order"
        vmconf.bootOptions = vim.vm.BootOptions(bootOrder=[vim.vm.BootOptions.BootableCdromDevice()])

        task = vm.ReconfigVM_Task(vmconf)

        wait_for_task(task, si)

        print "Power On the VM to boot from iso"
        vm. PowerOnVM_Task()

    except vmodl.MethodFault, e:
        print "Caught vmodl fault: %s" % e.msg
        return 1
    except Exception, e:
        print "Caught exception: %s" % str(e)
        return 1

# Start program
if __name__ == "__main__":
    main()
