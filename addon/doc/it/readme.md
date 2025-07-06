# Note Diary para NVDA

Un complemento de NVDA que te permite crear, modificar, importar y exportar notas de manera rápida y eficiente.

## Características

*   **Gestión de Diarios y Capítulos**: Organiza tus notas en diarios y capítulos para una mejor estructura.
*   **Edición Rápida**: Abre y edita capítulos con facilidad.
*   **Importación y Exportación**: Guarda y restaura tus diarios y capítulos en archivos `.ndn`.
*   **Búsqueda Integrada**: Encuentra rápidamente diarios y capítulos por nombre.
*   **Accesibilidad Mejorada**: Diseñado pensando en la accesibilidad para usuarios de NVDA.
*   **Sonidos Personalizables**: Configura sonidos para eventos clave del complemento.

## Instalación

1.  Descarga la última versión del complemento desde el enlace de descarga.
2.  Abre el archivo `.nvda-addon` descargado.
3.  Confirma la instalación cuando NVDA te lo solicite.
4.  Reinicia NVDA para que los cambios surtan efecto.

## Cómo usar el complemento

Para usar el complemento, sigue los siguientes pasos:

1.  **Abrir el complemento**: Accede a Note Diary desde el menú de NVDA, en `Herramientas` > `Note Diary`. Puedes asignar un gesto de teclado en `Preferencias` > `Gestos de entrada` bajo la categoría `Note Diary`.
2.  **Crear un diario**: Pulsa el botón de menú `Más opciones` y selecciona `Nuevo diario`, o usa `CTRL+N` en el árbol de diarios. Introduce el nombre del diario (ej., "Mi diario personal", "Curso de Python").
3.  **Crear capítulos**: Con el diario seleccionado, pulsa `Más opciones` > `Nuevo capítulo`, o usa `CTRL+P`. Dale un nombre al capítulo (ej., "Clase 01 Hola mundo", "05/07/2025").
4.  **Escribir en un capítulo**: Selecciona un capítulo y pulsa `Intro`, o `Aplicaciones` / `Shift+F10` y selecciona `Editar`. Comienza a escribir en el campo multilínea.
5.  **Guardar el capítulo**: Pulsa `Alt+G` o navega con `Tab` hasta el botón `Guardar` y púlsalo. Si hay cambios y cierras la ventana, se te preguntará si deseas guardar.

## Explicación de la interfaz

### La lista de diarios

Es una vista de árbol que permite navegar por diarios y capítulos. Los diarios están en el nivel 0. Usa las flechas arriba/abajo para moverte, `Intro` o flechas izquierda/derecha para expandir/contraer diarios. También puedes navegar con las letras del alfabeto.

### El botón de más opciones

Al pulsar este botón o enfocarlo y pulsar flecha abajo, aparecen las siguientes opciones:

*   **Nuevo diario**: Crea un nuevo diario.
*   **Nuevo capítulo**: Crea un nuevo capítulo en el diario seleccionado.
*   **Importar diarios**: Restaura diarios desde un archivo `.ndn`.
*   **Exportar diarios**: Guarda todos tus diarios y capítulos en un archivo `.ndn` para copia de seguridad o compartir.
*   **Ayuda**: Contiene `Acerca de...` (información básica del complemento) y `Documentación` (abre este archivo en el navegador).

### Cuadro de información de solo lectura

Después de la lista de diarios, encontrarás un cuadro de edición de solo lectura con información básica del diario o capítulo seleccionado.

*   **Diarios**: Muestra nombre, fecha de creación, fecha de modificación y número de capítulos.
*   **Capítulos**: Muestra nombre del capítulo, diario al que pertenece, fecha de creación, fecha de modificación y número de páginas.

### El botón de cerrar

Cierra la ventana del complemento. También puedes usar la tecla `Escape`.

## Lista de atajos de teclado

### Ventana principal

*   `Ctrl+N`: Crea un nuevo diario.
*   `Ctrl+P`: Crea un nuevo capítulo en el diario seleccionado.
*   `Suprimir`: Elimina un diario (con todos sus capítulos) o un capítulo.
*   `Intro`: Abre/cierra un diario; abre la ventana de edición de un capítulo.
*   `F5`: Actualiza la ventana.
*   `F2`: Renombra el diario o capítulo seleccionado.
*   `F1`: Abre este documento.
*   `Aplicaciones` o `Shift+F10`: Abre un menú contextual para el diario o capítulo seleccionado.

### Atajos útiles en la ventana principal

*   `Alt+M`: Abre el menú `Más opciones`.
*   `Alt+D`: Enfoca la lista de diarios.
*   `Alt+I`: Enfoca el cuadro de edición de información.
*   `Alt+C`: Cierra la ventana del complemento.

### Atajos útiles dentro de la ventana de edición de un capítulo

*   `Alt+N`: Enfoca el campo de edición.
*   `Alt+P`: Copia todo el contenido del capítulo al portapapeles.
*   `Alt+G`: Guarda el capítulo.
*   `Alt+C`: Cierra el diálogo del capítulo.

## Configuración del complemento

En las opciones de NVDA, bajo `Note Diary`, puedes activar o desactivar los sonidos del complemento. Cuando están activados, se reproducirán sonidos en eventos como el cambio de diario o capítulo.

## Descarga

Puedes descargar la última versión del complemento desde el siguiente enlace:
[Descargar Note Diary para NVDA v2025.1.0](https://github.com/JohanAnim/Note-diary/releases/download/2025.1.0/Note.diary.for.NVDA-2025.1.0.nvda-addon)

## Colaboradores

Créditos a los siguientes usuarios por colaborar con parte del código fuente y con algunas funcionalidades:

*   [Héctor J. Benítez Corredera](https://github.com/hxebolax/): Implementó la parte inicial de este complemento.
*   [metalalchemist](https://github.com/metalalchemist/): Implementación de algunas de las funcionalidades del complemento.

---

© 2023-2025 Johan G