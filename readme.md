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

Build imagens
```
docker-compose build
```

Executar os containers
```
docker-compose up -d
```

Executar as migrações
```
docker-compose run web python manage.py migrate
```

Acessar a API
```
localhost:8000
```

Execução dos testes
```
docker-compose run web make test-cov
```

Execução do code convention
```
docker-compose run web make code-convention
```


