# Documentação da API

## Endpoints
| Caminho                              | Método | Descrição                                          | Body                                                                                           |
|--------------------------------------|--------|----------------------------------------------------|------------------------------------------------------------------------------------------------|
| /usuarios/                           | Get    | Retorna uma lista de usuários.                     |                                                                                                |
| /usuarios/                           | Post   | Cria um usuário.                                   | ``` {     "username": "Miguel",     "email": "miguel@gmail.com",     "password": "senha" } ``` |
| /usuarios/<id>/                      | Get    | Retorna um usuário específico.                     |                                                                                                |
| /usuarios/<id>/creditar/             | Post   | Realiza crédito no usuário.                        | ``` {     "credito": 200 } ```                                                                 |
| /usuarios/<id>/debitar/              | Post   | Realiza débito no usuário.                         | ``` {     "debito": 200 }```                                                                   |
| /usuarios/<id>/extrato/              | Get    | Retorna uma lista de transações de um usuário.     |                                                                                                |
| /usuarios/<id>/extrato/?tipo=Crédito | Get    | Retorna uma lista de transações do tipo 'Crédito'. |                                                                                                |
| /usuarios/<id>/extrato/?tipo=Débito  | Get    | Retorna uma lista de transações do tipo 'Débito'.  |                                                                                                |