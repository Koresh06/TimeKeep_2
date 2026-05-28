**Auth:**
<!-- - `POST /auth/register` — ADMIN создаёт пользователя
- `POST /auth/login` — все -->

---

<!-- **Overtime:**
- `POST /overtimes` — USER, создать свою переработку
- `DELETE /overtimes/{id}` — USER, удалить свою переработку
- `GET /overtimes/me` — USER, свои переработки (фильтр по status, date_)
- `GET /overtimes/department` — MODERATOR, переработки своего департамента
- `GET /overtimes/organization` — ADMIN, переработки своей организации
- `GET /overtimes` — SUPER_ADMIN, все переработки системы -->

---

<!-- **DayOff:**
- `POST /day-offs` — USER, взять отгул
- `GET /day-offs/me` — USER, свои отгулы (фильтр по status)
- `GET /day-offs/department` — MODERATOR, отгулы своего департамента (фильтр по status)
- `GET /day-offs/organization` — ADMIN, отгулы своей организации
- `GET /day-offs` — SUPER_ADMIN, все отгулы системы
- `PATCH /day-offs/{id}/moderate` — MODERATOR, подтвердить/отклонить
- `GET /day-offs/{id}/report` — USER, скачать рапорт -->

---

**Organization:**
<!-- - `POST /organizations` — SUPER_ADMIN, создать организацию
- `GET /organizations/{id}` — ADMIN, SUPER_ADMIN
- `GET /organizations` — SUPER_ADMIN, все организации -->

---

**Department:**
<!-- - `POST /departments` — ADMIN, создать департамент в своей организации
- `GET /departments/{id}` — MODERATOR, ADMIN
- `GET /departments/organization/{organization_id}` — ADMIN, SUPER_ADMIN -->

---

**Users:**
<!-- - `GET /users/me` — все, свой профиль
- `GET /users/department` — MODERATOR, пользователи своего департамента
- `GET /users/organization` — ADMIN, все пользователи своей организации
- `GET /users` — SUPER_ADMIN, все пользователи системы
- `PATCH /users/{id}/role` — ADMIN, изменить роль пользователя
- `PATCH /users/{id}/work-mode` — ADMIN, изменить режим работы
- `PATCH /users/{id}/activate` — ADMIN, активировать/деактивировать пользователя -->