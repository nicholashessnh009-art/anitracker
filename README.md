# anitracker
Second semester AeP project, built on Python

Proposta Software AeP Segundo Semestre:
Nicholas Hess

Tracker de animes assistidos
Features:
Deixa adicionar séries que já assisti
Criador de listas (favoritos, por categoria etc)
Placar por rating pessoal (por categoria, listas)
Fácil de rodar (talvez com uma interface própria)
Como irei fazer esse projeto?
Vou pegar uma API de animes como MyAnimeList ou AniList para acessar uma database de animes. Posso expandir para outros tipos de mídia no futuro (filmes, séries, documentários).
Não sei quais estruturas de dados vou utilizar.
Meu software terá um menu (se eu conseguir não no terminal, com uma interface própria como um aplicativo).

## Próximo passo: biblioteca em memória

A primeira camada do projeto está em `mainfolder/`. Ela mantém os animes
durante a execução do programa, sem usar SQLite ainda:

- `models.py` define o modelo `Anime`, incluindo a validação da nota de 1 a 10.
- `library.py` define `AnimeLibrary`, que adiciona animes, cria listas
  personalizadas e faz rankings por gênero ou lista.

Para executar os testes dessa etapa, a partir da pasta `anitracker`, use:

```text
.venv\Scripts\python.exe -m unittest discover -s tests -t . -v
```

Essa camada foi separada da API e do banco de dados de propósito. No próximo
passo, o SQLite poderá persistir os objetos `Anime` sem mudar as regras da
biblioteca.
