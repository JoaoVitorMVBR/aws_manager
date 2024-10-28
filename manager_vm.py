import boto3
import subprocess


class Manager:
    
    def create_vm(self, ec2_resources, instance_name):
        
        instances = ec2_resources.create_instances(
            ImageId='ami-0f16d0d3ac759edfa', 
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',         
            KeyName='SCS_WORK_SA_EAST',
            SecurityGroupIds=['sg-0cde467bfadfeb70b'],
            TagSpecifications=[
                {
                    'ResourceType':'instance',
                    'Tags':[
                        {
                            'Key':'Name',
                            'Value':instance_name
                        }
                    ]
                }
            ]   
        )

        return instances

    def list_instances(self, ec2_resources):
        instances = ec2_resources.instances.all()
        vms = []

        for instance in instances:
            instance_id = instance.id
            instance_name = ''
            instance_status = instance.state['Name']

            # Tentar obter o nome da instância a partir das tags
            if 'Tags' in instance.meta.data:
                for tag in instance.tags:
                    if tag['Key'] == 'Name':
                        instance_name = tag['Value']

            vm = {
                'id':instance_id,
                'name':instance_name,
                'status':instance_status
            }

            vms.append(vm)

        return vms

    def stop_instance(self, ec2_client, instance_id):
        response = ec2_client.stop_instances(InstanceIds=[instance_id])
        print(f"Instância {instance_id} está sendo parada...")

    def start_instance(self, ec2_client, instance_id):
        response = ec2_client.start_instances(InstanceIds=[instance_id])
        print(f"Instância {instance_id} está sendo iniciada...")
    
    def reboot_instance(self, ec2_client, instance_id):
        response = ec2_client.reboot_instances(InstanceIds=[instance_id])
        print(f"Instância {instance_id} está sendo reiniciada...")

    def delete_instance(self, ec2_client, instance_id):
        response = ec2_client.terminate_instances(InstanceIds=[instance_id])
        print(f"Instância {instance_id} está sendo deletada...")

        response = ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        return [instance for reservation in response['Reservations'] for instance in reservation['Instances']]

    def update_memory(self, ec2_client, instance_id, size):
        instances = ec2_client.describe_instances(InstanceIds=[instance_id])
        volume_id = instances['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeId']
        response = ec2_client.modify_volume(
            VolumeId=volume_id,
            Size=size
        )

    def update_name(self, ec2_client, instance_id, name):
        response = ec2_client.create_tags(
            Resources=[instance_id],
            Tags=[
                {'Key': 'Name', 'Value': name}
            ]
        )
    
    def connect_instance(self, ec2_resources, instance_id, key_path):
        instance = ec2_resources.Instance(instance_id)
        public_ip = instance.public_ip_address
        key_name = instance.key_name 
        key_path = key_path
        if public_ip:
            command = f"ssh -i '{key_path}' ubuntu@{public_ip}"
            subprocess.call(command, shell=True)
        else:
            print("Não foi possível obter o endereço IP da instância.")