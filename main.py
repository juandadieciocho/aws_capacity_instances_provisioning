from capacity_provisioning import DeployInfraestructure
import sys
import time
DeployInfraestructure = DeployInfraestructure()
selection = sys.argv[1]
if selection == "Raise web apis instamces":
    print(DeployInfraestructure.raise_webapis())
elif selection == "Raise integration server instances":
    print(DeployInfraestructure.raise_integrationserver())
elif selection == "Raise web apis instances":
    print(DeployInfraestructure.raise_webapisext())
elif selection == "Raise extended integration server instances":
    print(DeployInfraestructure.raise_asg_integrationserver())
elif selection == "Register web apis targets":
    print(DeployInfraestructure.register_was())
elif selection == "Register integration server targets":
    print(DeployInfraestructure.register_integration())
elif selection == "Register extended web api targets":
    print(DeployInfraestructure.register_wasext())
elif selection == "Register extended integration server targets":
    print(DeployInfraestructure.register_integrationext())
elif selection == "Deregister integration server extended targets":
    print(DeployInfraestructure.disregister_integrationext())
elif selection == "Deregister web api targets":
    print(DeployInfraestructure.deregister_webapi)
elif selection == "Deregister integration server targets":
    print(DeployInfraestructure.deregister_integrationser())
elif selection == "Deregister integration extended targets":
    print(DeployInfraestructure.deregister_integrationext())
elif selection == "Deregister web api extended targets":
    print(DeployInfraestructure.deregister_webapiext())
elif selection == "End web api instances":
    print(DeployInfraestructure.end_web_api())
elif selection == "End integration server instances":
    print(DeployInfraestructure.end_integrationseervers())
elif selection == "End web api extended instances":
    print(DeployInfraestructure.end_web_apiext())
elif selection == "End integration server extended instances":
    print(DeployInfraestructure.deregister_integrationext())
    print(DeployInfraestructure.end_integration_asg())

