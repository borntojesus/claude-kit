# Public та internal версії

## Модель видимості

Поле `visibility: public | internal` доступне на project, presentation, research document і slide.

Правило спадкування просте: child може бути суворішим за parent, але не може бути публічнішим. Internal project робить internal увесь вкладений content.

## Дві незалежні збірки

Internal build містить deck, slide kitchen, research, speaker notes, objections і draft Q&A. Для нього встановлюється `noindex`.

Public build містить лише audience facing routes та content. Він не будує internal routes.

Видалення internal сторінок після build недостатнє. Текст може залишитися у JavaScript chunk, JSON payload або search index.

## Leak test

Додати sentinel strings у internal fixtures. Після public build просканувати весь output directory. Build має впасти, якщо знайдено хоча б один marker.

Також перевірити:

1. Internal routes повертають 404 у public artifact.
2. Slide kitchen відсутня в DOM та bundle.
3. Public navigation не містить internal labels.
4. Shared slide links не змінюють значення після visibility filtering.
5. Source documents із персональними даними не копіюються в public assets.

## Credentials та приватні джерела

Credentials не є presentation content. Вони зберігаються в approved secret store. Presentation files містять лише source IDs або sanitized paths.
