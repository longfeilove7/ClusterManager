#!/usr/bin/python
# -*- coding: UTF-8 -*-
#注意：popen定义的时候就会执行命令,所以不要直接用popen去定义变量。
import os, sys, commands
#host=os.popen('echo -n 10.18.10.10').read( )
#host=commands.getoutput('echo 10.18.10.10')
host = "10.18.10.10"
user = "admin"
password = "admin"

powerStatus = "ipmitool -H " + host + " -U " + user + " -P " + password + " power status"
powerOn = "ipmitool -H " + host + " -U " + user + " -P " + password + " power on"
powerOff = "ipmitool -H " + host + " -U " + user + " -P " + password + " power off"
powerCycle = "ipmitool -H " + host + " -U " + user + " -P " + password + " power cycle"
powerReset = "ipmitool -H " + host + " -U " + user + " -P " + password + " power reset"
powerDiag = "ipmitool -H " + host + " -U " + user + " -P " + password + " power diag"
powerSoft = "ipmitool -H " + host + " -U " + user + " -P " + password + " power soft"
#powerStatus = os.popen("ipmitool -H " + host + " -U " + user + " -P " + password + " power status")
#powerOn = os.popen("ipmitool -H " + host + " -U admin -P admin power on")
#powerOff = os.popen("ipmitool -H " + host + " -U admin -P admin power off")
#powerCycle = os.popen("ipmitool -H " + host + " -U admin -P admin power cycle")
#powerReset = os.popen("ipmitool -H " + host + " -U admin -P admin power reset")
#powerDiag = os.popen("ipmitool -H " + host + " -U admin -P admin power diag")
#powerSoft = os.popen("ipmitool -H " + host + " -U admin -P admin power soft")
print type(powerStatus)
powerStatus = os.popen(powerStatus)
#powerStatus = os.popen('echo $host')
print(powerStatus.read())
print(host)
