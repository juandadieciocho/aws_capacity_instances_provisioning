import boto3
import os
from dotenv import load_dotenv
load_dotenv(".env")
from environs import Env

class TagInformation:
    def __init__(self) -> None:
        self.ec2 = boto3.client('ec2')
    def get_info_instance(self,tagsInstance: list):
        response= []
        response=self.ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': tagsInstance}])
        listInstancesWas = list()
        for tag in range(len(tagsInstance)):
                try:
                    listInstancesWas.append(response['Reservations']
                                            [tag]['Instances'][0]['InstanceId'])
                except:
                    continue
        return listInstancesWas
      
        
class DeployInfraestructure:
    def __init__(self):
        self.arn_was = os.getenv("arn_web_api")
        self.arn_iib = os.getenv("arn_integration_servers")
        self.env = Env()
        self.env.read_env() 
        self.tags_Was =['web_api03', 'web_api04','web_api05', 'web_api06', 'web_api07','web_api08', 'web_api09', 'web_api10']
        self.tags_Bus =['integration_server03', 'integration_server04', 'integration_server08','integration_server09', 'integration_server10']
        self.was_tags_extendedlist=['web_api03', 'web_api04', 'web_api05','web_api06','web_api07','web_api08', 'web_api09', 'web_api10','web_api11', 'web_api12','web_api13','web_api14','web_api15',
                                    'web_api16','web_api17','web_api16','web_api17','web_api18','web_api19','web_api20','web_api21','web_api22','web_api23','web_api24','web_api25','web_api26','web_api27','web_api29','web_api30','web_api31','web_api32','web_api33','web_api35','web_api34','web_api36','web_api38','web_api39','web_api40']
        self.asg=boto3.client('autoscaling')
        self.tag_info=TagInformation()
        self.was_list = self.tag_info.get_info_instance(self.tags_Was)
        self.was_extendedlist=self.tag_info.get_info_instance(self.was_tags_extendedlist)
        self.iib_list = self.tag_info.get_info_instance(self.tags_Bus)
        self.targetswas = list()
        self.targetsiib = list()
        self.targets_ext = list()
        for inst in self.was_list:
            self.targetswas.append({'Id': inst, 'Port': 9443})
        for inst in self.iib_list:
            self.targetsiib.append({'Id': inst, 'Port': 4443})
        for inst in self.was_extendedlist:
            self.targets_ext.append({'Id': inst, 'Port': 9443})
        self.ec2 = boto3.client('ec2')
        self.elb = boto3.client('elbv2')

    def raise_webapis(self) -> str:
        self.ec2.start_instances(InstanceIds=self.was_list)
        outcome = 'begginning web api instances'
        return outcome

    def raise_integrationserver(self) -> str:
        try:
            self.ec2.start_instances(InstanceIds=self.iib_list)
            outcome = 'begginning integration servers'
        except:
            self.error()
        return outcome
    def raise_asg_integrationserver(self)->str:
        try:
            self.asg.update_auto_scaling_group(AutoScalingGroupName='ag-integration_server-asg',DesiredCapacity=10,MinSize=10,MaxSize=40)
            outcome="raising ASG integration servers"
        except:
            self.error()
        return outcome
    def raise_webapisext(self)->str:
        self.ec2.start_instances(InstanceIds=self.was_extendedlist)
        outcome="raising extended web api instances"
        return outcome
    def end_web_api(self) -> str:
        try:
            self.elb.deregister_targets(
                TargetGroupArn=self.arn_was, Targets=self.targetswas)
        finally:
            try:
                self.ec2.stop_instances(InstanceIds=self.was_list)
                outcome = 'ending web api instances'
            except:
                self.error()
        return outcome

    def end_integrationseervers(self) -> str:
        try:
            self.elb.deregister_targets(
                TargetGroupArn=self.arn_iib, Targets=self.targetsiib)
        finally:
            try:
                self.ec2.stop_instances(InstanceIds=self.iib_list)
                outcome = 'ending integration servers'
            except:
                self.error()
        return outcome
    def end_integration_asg(self)->str:
        try:
            self.asg.update_auto_scaling_group(AutoScalingGroupName='ag-integration_server-asg',DesiredCapacity=0,MaxSize=0,MinSize=0)
            outcome="Ending ASG Integration servers"
        except:
            self.error()
        return outcome   
    def end_web_apiext(self)->str:
        try:
            self.elb.deregister_targets(TargetGroupArn=self.arn_was,Targets=self.targets_ext)
            self.ec2.stop_instances(InstanceIds=self.was_extendedlist)
        except:
            self.error()
        finally:
            outcome='ending extended web api instances'
        return outcome
    
    def register_webapi(self) -> str:
        try:
            self.elb.register_targets(TargetGroupArn=self.arn_was, Targets=self.targetswas)
            outcome = "registering web api instances"
        except:
            self.error()
        return outcome

    def register_integration(self) -> str:
        try:
            self.elb.register_targets(
                TargetGroupArn=self.arn_iib, Targets=self.targetsiib)
        except:
            self.error()
    def register_wasext(self)->str:
        try:
            self.elb.register_targets(TargetGroupArn=self.arn_was,Targets=self.targets_ext)
            outcome="raising extended web api instances"
        except:
            self.error()
        return outcome
    def register_integrationext(self)->str:
        try:
            self.asg.attach_load_balancer_target_groups(AutoScalingGroupName='ag-integration_server-asg',TargetGroupARNs=[self.arn_iib])
        except:
            self.error()
        outcome="registering integration servers ASG instances"
        return outcome
   
    def register_webapiext(self)->str:
        try:
            self.elb.register_targets(TargetGroupArn=self.arn_was,Targets=self.targets_ext)
            outcome="raising extended web api instances"
        except:
            self.error()
        return outcome

    def deregister_integrationser(self) -> str:
        try:
            self.elb.deregister_targets(
                TargetGroupArn=self.arn_iib, Targets=self.targetsiib)
        except:
            self.error()
    def deregister_webapi(self) -> str:
       try:
           self.elb.deregister_targets(
               TargetGroupArn=self.arn_was, Targets=self.targetswas)
           outcome = "Deregistering instances web api"
       except:
           self.error()
       return outcome
    def deregister_webapiext(self)->str:
        try:
            self.elb.deregister_targets(TargetGroupArn=self.arn_was,Targets=self.targets_ext)
            outcome="Deregistering instances extended web api"
        except:
            self.error()
        return outcome
    def deregister_integrationext(self)->str:
        try:
            self.asg.detach_load_balancer_target_groups(AutoScalingGroupName='ag-integration_server-asg',TargetGroupARNs=[self.arn_iib])
        except:
            self.error()
        outcome="Deregistering ASG instances"
        return outcome

    def error(self):
        raise ValueError("Proccess failed")
