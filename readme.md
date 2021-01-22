# Nexx Test - Conta Virtual

[Documentação da api](./docs.md)

## Instruções para executar a api.

Clonar o projeto
```
git clone git@github.com:miguelvieiraramos/nexx-test.git
```

Acessar a pasta
```
cd nexx-test/
```

Executar os containers
```
docker-compose up
```

Executar as migrações
```
docker-compose run web python manage.py migrate
```

Execução dos testes
```
docker-compose run web make test-cov
```

Execução do code convention
```
docker-compose run web make code-convention
```


