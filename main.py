import click
import boto3
from manager_vm import *


def plot_intances(instances):
    if instances:
        for instance in instances:
                print(f"ID:{instance['id']}, Nome: {instance['name']}, Status: {instance['status']}")
    else:
        print("0 instancias")

@click.command()
def main():
    manager = Manager()
    ec2_resources = boto3.resource('ec2', region_name='sa-east-1')
    ec2_client = boto3.client('ec2', region_name='sa-east-1')

    while 1:
        """Menu de opções para gerenciar instâncias EC2"""
        click.echo("1. Criar uma instância")
        click.echo("2. Listar instâncias")
        click.echo("3. parar uma instância")
        click.echo("4. iniciar uma instância")
        click.echo("5. reiniciar uma instância")
        click.echo("6. deletar uma instância")
        click.echo("7. Atualizar instância")
        click.echo("8. Conectar instância")
        click.echo("0. Sair")

        option = click.prompt("Escolha uma opção", type=int)

        if option == 1:
            instance_name = click.prompt('Nome da instância')
            instances = manager.create_vm(ec2_resources, instance_name)
            if instances:
                print("Instancia criada", instances[0].id)

        elif option == 2:
            instances = manager.list_instances(ec2_resources)
            plot_intances(instances)
            print('\n\n\n')
        
        elif option == 3:
            instances = manager.list_instances(ec2_resources)
            plot_intances(instances)
            instance_id=click.prompt("Digite um dos ids acima:")
            manager.stop_instance(ec2_client, instance_id)

        elif option == 4:
            instances = manager.list_instances(ec2_resources)
            plot_intances(instances)
            instance_id=click.prompt("Digite um dos ids acima:")
            manager.start_instance(ec2_client, instance_id)
        
        elif option == 5:
            instances = manager.list_instances(ec2_resources)
            plot_intances(instances)
            instance_id=click.prompt("Digite um dos ids acima:")
            manager.reboot_instance(ec2_client, instance_id)
        
        elif option == 6:
            instances = manager.list_instances(ec2_resources)
            plot_intances(instances)
            instance_id=click.prompt("Digite um dos ids acima:")
            manager.delete_instance(ec2_client, instance_id)

        elif option == 7:
            update=click.prompt("M - memória | N - nome")
            instances = manager.list_instances(ec2_resources)
            plot_intances(instances)
            instance_id=click.prompt("Digite um dos ids acima:")

            if update == 'M' or update == 'm':
                size = click.prompt("Digite o valor em gb:")
                manager.update_memory(ec2_client, instance_id, int(size))

            elif update == 'N' or update == 'n':
                print('ok')
                name = click.prompt("Digite o novo nome:")
                manager.update_name(ec2_client, instance_id, name)
        elif option == 8:
            instances = manager.list_instances(ec2_resources)
            plot_intances(instances)
            instance_id=click.prompt("Digite um dos ids acima:")
            key=click.prompt("Digite a chave de acesso")
            manager.connect_instance(ec2_resources, instance_id, key)
        elif option == 0:
            return 0
        
        else:
            click.echo("Opção invalida")

if __name__ == '__main__':
    main()