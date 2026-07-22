# Архітектура

## Data flow

```text
Markdown and YAML
  -> parser
  -> schema validation
  -> research inheritance
  -> visibility filter
  -> typed presentation model
     -> grouped sidebar
     -> live deck
     -> current slide kitchen
     -> research pages
     -> public exporter
```

Content loader не повинен знати про React. UI отримує готову типізовану модель. Завдяки цьому той самий loader можна використати для web viewer, CLI validation, MCP server і майбутнього PPTX export.

## Чотири модулі

### Content engine

Читає файлову структуру, frontmatter і Markdown. Перевіряє schemas, slugs, media, links, visibility та дозволені секції slide kitchen.

### Navigation shell

Будує бокове меню з двох груп research: спільної для проєкту та власної для презентації. На desktop меню згортається до icon rail. На mobile стає drawer. Для реалізації використовується наявний skill `sidebar-nav-shell`.

### Deck viewer

Отримує слайди через props. Підтримує Arrow keys, Page Up, Page Down, Space, Backspace, Home, End, fullscreen і black screen. На останньому слайді зайвий клік нічого не робить.

### Slide kitchen

Показує internal дані лише для поточного слайда. Fullscreen охоплює тільки slide canvas, тому кухня не потрапляє на екран у залі. Public build не отримує цей блок узагалі.

## Маршрути

```text
/
/p/<project>
/p/<project>/<presentation>
/p/<project>/<presentation>/deck
/p/<project>/<presentation>/r/<research>
/p/<project>/<presentation>/s/<slide>
```

Постійне посилання на слайд використовує filename slug без числового префікса. Перестановка слайдів не ламає вже роздані URL.

## Розміщення на сторінці

```text
App shell
  Sidebar
    Project switcher
    Presentation switcher
    Project research
    Presentation research
    Q&A and risks
  Main
    Sticky breadcrumb bar
    Deck canvas
    Deck controls
    Slide kitchen
    Related research
```

Slide kitchen завжди йде одразу після deck controls. Автор не повинен переходити на іншу сторінку, щоб перевірити, навіщо існує слайд або звідки взялася цифра.

## State

URL зберігає project, presentation і slide slug. Local storage може зберігати лише UI preference: collapsed sidebar, open menu groups і theme. Content state залишається у файлах та Git.

## Data ownership

1. Slide frontmatter володіє тим, що бачить зал.
2. Slide body володіє кухнею конкретного слайда.
3. Presentation research володіє контекстом одного deck.
4. Project research володіє матеріалами, які ділять кілька deck.
5. Evidence ledger володіє trace від claim до exact source location.
