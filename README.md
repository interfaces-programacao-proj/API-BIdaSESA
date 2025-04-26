# API-BI da SESA
Aplicação Flask BI da SESA

## Passos 
1. Instale as lib requeridas com base no arquivo 'lib/requeriments.txt' com:
```cmd
pip install -r lib/requirements.txt
```
ou
```cmd
python3 -m pip install -r lib/requirements.txt
```

2. Após crie sua propria branch:
    1. Primeiro, garante que você está no repositório certo:

    ```bash
    git status
    ```

    2. Aí você cria e já muda pra nova branch com:

    ```bash
    git checkout -b nome-da-sua-branch
    ```

    **Exemplo:**
    ```bash
    git checkout -b feat/nova-funcionalidade
    ```

    **Explicando:**  
    - `checkout -b` cria **e** muda para a branch nova numa tacada só.
    - `nome-da-sua-branch` pode seguir um padrão, tipo `feat/`, `fix/`, `hotfix/`, depende do seu fluxo.

    3. Depois que trabalhar e quiser subir as mudanças:

    ```bash
    git add .
    git commit -m "mensagem do commit explicando a mudança"
    git push origin nome-da-sua-branch
    ```

    **Importante:** A primeira vez que você der o `push`, talvez precise usar:

    ```bash
    git push --set-upstream origin nome-da-sua-branch
    ```

    Aí o Git já entende que sua branch local tá conectada com a remota.

    ---
   