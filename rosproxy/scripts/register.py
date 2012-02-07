#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2010, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

NAME="register.py"

import roslib; roslib.load_manifest('rosproxy')

import os
import sys

import roslib.network
import rosgraph.masterapi
import rospy

def register_main():
    from optparse import OptionParser
    parser = OptionParser(usage="\n\t%prog service /service_name rosrpc://HOSTNAME:PORT\n"+\
                              "\t%prog pub /topic_name topic_msg/Type http://HOSTNAME:PORT", prog=NAME)
    options, args = parser.parse_args(rospy.myargv()[1:])
    if len(args) < 3:
        parser.print_usage()
        sys.exit(os.EX_USAGE)
        
    reg = args[0]
    if reg == 'service':
        if len(args) != 3:
            parser.error("Please specify service name and URI")
        _, name, uri = args
        
        m = rosgraph.masterapi.Master('rosproxy_register')
        # register proxy with URI of port zero. this will create bad info
        # on master, but at least it will accumulate under the same port
        fake_api = 'http://%s:0'%roslib.network.get_host_name()
        m.registerService(name, uri, fake_api)

    elif reg == 'pub':
        if len(args) != 4:
            parser.error("Please specify topic name, topic type, and URI")
        _, name, topic_type, uri = args

        
        m = rosgraph.masterapi.Master('rosproxy_register')
        m.registerPublisher(name, topic_type, uri)
    else:
        parser.error("Please specify 'pub' or 'service'")
    
if __name__ == '__main__':
    register_main()