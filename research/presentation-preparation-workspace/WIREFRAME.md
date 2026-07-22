# Wireframe

## Desktop preparation view

```text
┌────────────────────┬───────────────────────────────────────────────┐
│ Project             │ Project / Presentation / Slide              │
│ Presentation        ├───────────────────────────────────────────────┤
│                     │                                               │
│ PRESENTATION        │              16:9 slide canvas                │
│   Deck              │                                               │
│   Slide outline     ├───────────────────────────────────────────────┤
│                     │ 01 02 03 04       4 / 18     black  fullscreen│
│ PROJECT RESEARCH    ├───────────────────────────────────────────────┤
│   Audience          │ KITCHEN, SLIDE 4                              │
│   Market            │                                               │
│   Data              │ Goal                 Voice                    │
│                     │ Research             Claims                   │
│ PRESENTATION DATA   │ Sources              Objections               │
│   Risks             │ Timing               Audience response        │
│   Q&A               │ Verification                                  │
│   Sources           ├───────────────────────────────────────────────┤
│                     │ Related research document                     │
└────────────────────┴───────────────────────────────────────────────┘
```

## Collapsed desktop

Sidebar стає icon rail. Deck отримує більше ширини. Active item зберігає label через tooltip. Collapse state зберігається локально.

## Mobile preparation view

На mobile sidebar відкривається як drawer. Deck і slide kitchen йдуть одним vertical flow. Sticky bar містить menu button, presentation title і slide counter.

## Fullscreen

Fullscreen root охоплює лише slide canvas. Controls можуть зникати після короткої бездіяльності. Slide kitchen і sidebar фізично знаходяться поза fullscreen element.

## Interaction rules

1. Зміна слайда оновлює kitchen без переходу сторінки.
2. Відкриття research document не втрачає поточний slide slug.
3. Shared slide URL відкриває slide і його supporting data у internal view.
4. Public shared URL показує лише audience facing content.
