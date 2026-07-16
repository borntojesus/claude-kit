---
description: Аналіз навантаження Mac — усі локальні сервери (LISTEN порти) + claude-сесії + dev-сервери з RSS/CPU/uptime, відсортовані за впливом на swap.
---

Покажи користувачу повну картину того, що навантажує його Mac прямо зараз. Виведення — у термінал, ніяких файлів, ніяких підтверджень. Не вбивай нічого без явного запиту.

Виконай ці кроки **одним блоком паралельних Bash-викликів** (де можливо) і виведи зведену таблицю в кінці.

## Що зібрати

1. **System pressure:** `uptime`, `sysctl vm.swapusage`, `vm_stat | head -10`, кількість users
2. **Локальні listening порти** (це ключове — "локалхости"):
   ```sh
   lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | awk 'NR>1 {print $2, $1, $9}' | sort -u
   ```
   Для кожного порту: підтягни PID → RSS / %CPU / etime / робочу теку через
   ```sh
   ps -Ao pid,ppid,pcpu,rss,etime,command -p <PID>
   lsof -p <PID> -d cwd 2>/dev/null | tail -1
   ```
3. **Claude-сесії** (часта причина swap death):
   ```sh
   ps -Ao pid,ppid,pcpu,rss,etime,command | grep -E ' claude( |$)' | grep -v grep
   ```
   Познач поточну сесію (її PID = `$PPID` цієї bash-сесії).
4. **Dev-сервери** (vite/next/astro/nuxt/payload):
   ```sh
   ps -Ao pid,ppid,pcpu,rss,etime,command | grep -E "(vite|next dev|next-server|astro dev|nuxt dev|payload)" | grep -v grep
   ```
5. **Orphan-процеси** (PPID=1, потенційно зомбі від закритих терміналів):
   ```sh
   ps -Ao pid,ppid,rss,command | awk '$2==1 && $3>20000' | sort -rn -k3 | head -15
   ```
6. **Node-сума** (агрегат пам'яті всіх node-процесів):
   ```sh
   ps -Ao pid,rss,comm | awk '$3=="node" {sum+=$2; n++} END {printf "%d procs, %.0f MB total\n", n, sum/1024}'
   ```

## Як вивести

Один зведений markdown-блок:

### 🔥 Тиск системи

- Load avg / swap used / free RAM / uptime
- Маркер: 🟢 норм / 🟡 тривога (swap > 50%) / 🔴 swap death (swap > 90% або load > N_cores)

### 🌐 Локальні сервери (LISTEN порти)

Таблиця: `Порт | PID | Процес | RSS | CPU% | Етіме | Тека (cwd) | Проєкт`
Сортуй за RSS спадно. Проєкт визнач за cwd (порівняй з global registry портів у CLAUDE.md якщо співпадає).

### 🤖 Claude-сесії

Таблиця: `PID | Час життя | RSS | CPU% | Поточна?` — постав ✅ біля своєї.

### 🧟 Orphan / dev-сервери варті уваги

Список з командою і RSS.

### 💡 Рекомендація

1–3 рядки: що варто закрити в першу чергу, з конкретними PID. **Не пропонуй kill автоматично** — лише назви кандидатів. Якщо swap > 90% — нагадай про `cleanup` функцію в `~/.zshrc` (вбиває тільки orphans) і про memory [[project_mac_swap_death]].

## Правила

- НЕ kill-ай нічого, навіть якщо очевидно мертве. Тільки діагностика.
- НЕ створюй файлів. Все у відповідь.
- Українською. Стисло, таблицями.
- Якщо `lsof` потребує дозволу — повідом і пропусти цей блок, решту виконай.
