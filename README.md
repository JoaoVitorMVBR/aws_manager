A CLI gerencia chamadas de funções baseadas nas opções do usuário, centralizando a lógica de operações em uma classe chamada `Manager`.

A classe `Manager` fornece uma série de métodos para operações comuns em VMs na AWS, incluindo:

1. **Criação de VMs (`create_vm`)**: Cria uma nova instância EC2 com uma configuração pré-definida, como AMI, tipo de instância, chave de segurança e grupo de segurança.

2. **Listagem de Instâncias (`list_instances`)**: Lista todas as instâncias disponíveis, retornando informações como ID da instância, nome e status atual.

3. **Gerenciamento de Estado de Instâncias**:
    - **Parar** (`stop_instance`): Para uma instância específica.
    - **Iniciar** (`start_instance`): Inicia uma instância que estava parada.
    - **Reiniciar** (`reboot_instance`): Reinicia uma instância.

4. **Exclusão de Instâncias (`delete_instance`)**: Exclui (ou termina) uma instância específica, liberando os recursos alocados.

5. **Atualização de Configurações**:
    - **Memória (`update_memory`)**: Altera o tamanho do volume de armazenamento da instância.
    - **Nome (`update_name`)**: Modifica o nome de uma instância por meio de tags.
    
6. **Conexão SSH com Instâncias (`connect_instance`)**: Conecta-se a uma instância em execução usando SSH, obtendo o IP público e criando o comando SSH de forma automática, utilizando a chave fornecida.
