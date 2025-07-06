# Note Diary para NVDA

Um complemento do NVDA que permite criar, modificar, importar e exportar notas de forma rápida e eficiente.

## Recursos

*   **Gerenciamento de Diários e Capítulos**: Organize suas notas em diários e capítulos para uma melhor estrutura.
*   **Edição Rápida**: Abra e edite capítulos com facilidade.
*   **Importação e Exportação**: Salve e restaure seus diários e capítulos em arquivos `.ndn`.
*   **Pesquisa Integrada**: Encontre rapidamente diários e capítulos por nome.
*   **Acessibilidade Aprimorada**: Projetado com a acessibilidade em mente para usuários do NVDA.
*   **Sons Personalizáveis**: Configure sons para eventos chave no complemento.

## Instalação

1.  Baixe a versão mais recente do complemento no link de download.
2.  Abra o arquivo `.nvda-addon` baixado.
3.  Confirme a instalação quando solicitado pelo NVDA.
4.  Reinicie o NVDA para que as alterações entrem em vigor.

## Como usar o complemento

Para usar o complemento, siga estes passos:

1.  **Abrir o complemento**: Acesse o Note Diary no menu do NVDA, em `Ferramentas` > `Note Diary`. Você pode atribuir um atalho de teclado em `Preferências` > `Gestos de entrada` na categoria `Note Diary`.
2.  **Criar um diário**: Pressione o botão de menu `Mais opções` e selecione `Novo diário`, ou use `CTRL+N` na árvore de diários. Digite o nome do diário (ex., "Meu diário pessoal", "Curso de Python").
3.  **Criar capítulos**: Com o diário selecionado, pressione `Mais opções` > `Novo capítulo`, ou use `CTRL+P`. Dê um nome ao capítulo (ex., "Aula 01 Olá mundo", "05/07/2025").
4.  **Escrever em um capítulo**: Selecione um capítulo e pressione `Enter`, ou `Aplicativos` / `Shift+F10` e selecione `Editar`. Comece a escrever no campo de texto multilinha.
5.  **Salvar o capítulo**: Pressione `Alt+G` ou navegue com `Tab` até o botão `Salvar` e pressione-o. Se houver alterações e você fechar a janela, será perguntado se deseja salvar.

## Explicação da interface

### A lista de diários

É uma visualização em árvore que permite navegar por diários e capítulos. Os diários estão no nível 0. Use as setas para cima/para baixo para mover-se, `Enter` ou setas para a esquerda/direita para expandir/recolher diários. Você também pode navegar com as letras do alfabeto.

### O botão de mais opções

Ao pressionar este botão ou focá-lo e pressionar a seta para baixo, as seguintes opções aparecem:

*   **Novo diário**: Cria um novo diário.
*   **Novo capítulo**: Cria um novo capítulo no diário selecionado.
*   **Importar diários**: Restaura diários de um arquivo `.ndn`.
*   **Exportar diários**: Salva todos os seus diários e capítulos em um arquivo `.ndn` para backup ou compartilhamento.
*   **Ajuda**: Contém `Sobre...` (informações básicas sobre o complemento) e `Documentação` (abre este arquivo no navegador).

### Caixa de informações somente leitura

Após a lista de diários, você encontrará uma caixa de edição somente leitura com informações básicas sobre o diário ou capítulo selecionado.

*   **Diários**: Mostra nome, data de criação, data de modificação e número de capítulos.
*   **Capítulos**: Mostra nome do capítulo, diário ao qual pertence, data de criação, data de modificação e número de páginas.

### O botão de fechar

Fecha a janela do complemento. Você também pode usar a tecla `Escape`.

## Lista de atalhos de teclado

### Janela principal

*   `Ctrl+N`: Cria um novo diário.
*   `Ctrl+P`: Cria um novo capítulo no diário selecionado.
*   `Delete`: Exclui um diário (com todos os seus capítulos) ou um capítulo.
*   `Enter`: Abre/fecha um diário; abre a janela de edição de um capítulo.
*   `F5`: Atualiza a janela.
*   `F2`: Renomeia o diário ou capítulo selecionado.
*   `F1`: Abre este documento.
*   `Aplicativos` ou `Shift+F10`: Abre um menu de contexto para o diário ou capítulo selecionado.

### Atalhos úteis na janela principal

*   `Alt+M`: Abre o menu `Mais opções`.
*   `Alt+D`: Foca a lista de diários.
*   `Alt+I`: Foca a caixa de edição de informações.
*   `Alt+C`: Fecha a janela do complemento.

### Atalhos úteis dentro da janela de edição de um capítulo

*   `Alt+N`: Foca o campo de edição.
*   `Alt+P`: Copia todo o conteúdo do capítulo para a área de transferência.
*   `Alt+G`: Salva o capítulo.
*   `Alt+C`: Fecha o diálogo do capítulo.

## Configuração do complemento

Nas opções do NVDA, em `Note Diary`, você pode ativar ou desativar os sons do complemento. Quando ativados, os sons serão reproduzidos em eventos como a mudança de diário ou capítulo.

## Download

Você pode baixar a versão mais recente do complemento no seguinte link:
[Baixar Note Diary para NVDA](https://github.com/JohanAnim/Note-diary/releases/latest/download/Note.diary.for.NVDA.nvda-addon)

## Colaboradores

Créditos aos seguintes usuários por colaborar com parte do código-fonte e com algumas funcionalidades:

*   [Héctor J. Benítez Corredera](https://github.com/hxebolax/): Implementou a parte inicial deste complemento.
*   [metalalchemist](https://github.com/metalalchemist/): Implementação de algumas das funcionalidades do complemento.

---

© 2023-2025 Johan G

## Histórico de Alterações

Você pode ver todas as alterações e versões do complemento no [Histórico de Alterações](CHANGELOG.md).