# systemd units

Приклади unit-файлів для сервісу й ранкового брифа. Скопіювати в
`/etc/systemd/system/`, підставити свої шляхи, далі:

```bash
systemctl daemon-reload
systemctl enable --now assistant.service
systemctl enable --now assistant-brief.timer
systemctl list-timers | grep assistant
```

`ProtectSystem=strict` разом із `ReadWritePaths=/opt/assistant/state` означає, що
сервіс не може писати нікуди, крім свого каталогу стану. Якщо реалізація пише логи
у файл, шлях треба додати в `ReadWritePaths`, інакше запис впаде з правом доступу.
