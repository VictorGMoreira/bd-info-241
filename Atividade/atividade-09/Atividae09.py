import mysql.connector

# Conexão com o banco de dados
cnx = mysql.connector.connect(
    user='seu_usuario',
    password='sua_senha',
    host='seu_host',
    database='bd_scn'
)

# Criar cursor
cursor = cnx.cursor()

# Criar tabela TB_ALUNOS
create_table_query = """
    CREATE TABLE TB_ALUNOS (
        id INT UNSIGNED AUTO_INCREMENT,
        nome VARCHAR(50) NOT NULL,
        N1 DECIMAL(4,2),
        N2 DECIMAL(4,2),
        Faltas INT(2),
        Aprovado_SN BOOLEAN,
        PRIMARY KEY (id)
    )
"""
cursor.execute(create_table_query)

# Funcionalidades CRUD

# Create
def create_aluno(nome, N1, N2, Faltas, Aprovado_SN):
    insert_query = """
        INSERT INTO TB_ALUNOS (nome, N1, N2, Faltas, Aprovado_SN)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (nome, N1, N2, Faltas, Aprovado_SN))
    cnx.commit()

# Read
def read_alunos():
    select_query = "SELECT * FROM TB_ALUNOS"
    cursor.execute(select_query)
    return cursor.fetchall()

# Update
def update_aluno(id, nome, N1, N2, Faltas, Aprovado_SN):
    update_query = """
        UPDATE TB_ALUNOS
        SET nome = %s, N1 = %s, N2 = %s, Faltas = %s, Aprovado_SN = %s
        WHERE id = %s
    """
    cursor.execute(update_query, (nome, N1, N2, Faltas, Aprovado_SN, id))
    cnx.commit()

# Delete
def delete_aluno(id):
    delete_query = "DELETE FROM TB_ALUNOS WHERE id = %s"
    cursor.execute(delete_query, (id,))
    cnx.commit()

# Ler todos os registros da tabela TB_ALUNOS e mostrar o status de Aprovação
def check_approval_status():
    select_query = "SELECT * FROM TB_ALUNOS"
    cursor.execute(select_query)
    alunos = cursor.fetchall()
    
    for aluno in alunos:
        id, nome, N1, N2, Faltas, Aprovado_SN = aluno
        
        # Calcular média aritmética de N1 e N2
        media = (N1 + N2) / 2
        
        # Verificar se o aluno está aprovado ou reprovado
        if Faltas >= 20 or media < 6.0:
            Aprovado_SN = False
        else:
            Aprovado_SN = True
        
        # Atualizar o status de aprovação do aluno
        update_query = """
            UPDATE TB_ALUNOS
            SET Aprovado_SN = %s
            WHERE id = %s
        """
        cursor.execute(update_query, (Aprovado_SN, id))
        cnx.commit()
        
        # Mostrar o status de aprovação do aluno
        print(f"Aluno {nome} está {'APROVADO' if Aprovado_SN else 'REPROVADO'}")

# Incluir 5 registros na tabela TB_ALUNOS
create_aluno("João", 8.50, 9.20, 2, True)
create_aluno("Maria", 7.80, 8.50, 1, False)
create_aluno("Pedro", 9.00, 9.80, 0, True)
create_aluno("Ana", 8.20, 8.80, 2, False)
create_aluno("Luiz", 9.50, 9.90, 1, True)

# Consulta para retornar os alunos cadastrados
print("Alunos cadastrados:")
for aluno in read_alunos():
    print(aluno)

# Atualizar o aluno cujo id é 4
update_aluno(4, "Luiz Carlos", 9.50, 9.90, 1, True)

# Excluir o aluno cujo id = 3
delete_aluno(3)

# Verificar o status de aprovação dos alunos
check_approval_status()

# Fechar conexão
cursor.close()
cnx.close()