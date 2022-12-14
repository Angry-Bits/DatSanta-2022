# Hackathon-DatSanta-2022

## Подготовка к совместной работе

Во время хакатона мы будем использовать [Git](https://git-scm.com/) для контроля версий, [Poetry](https://python-poetry.org/) для управления пакетами и виртуальными окружениями + язык [Python](https://www.python.org/) новейшей версии 3.11.1.

Чтобы установить свежую версию Python, можно воспользоваться [Pyenv](https://github.com/pyenv/pyenv) — менеджером для управления и установки различных версий Python. Если он уже был ранее установлен, обязательно обновите его (иначе новую версию не найдет). На Linux это выглядит так:

```bash
pyenv update && pyenv install 3.11.1
```

В случае возникновения ошибки
```bash
error: failed to download Python-3.11.1.tar.xz

BUILD FAILED (Ubuntu 22.04 using python-build 2.3.8-10-g23576296)
```

обновите системный менеджер и скачайте необходимые [зависимости](https://github.com/pyenv/pyenv/wiki#suggested-build-environment), для Linux это выглядит следующим образом:

```bash
sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev libsasl2-dev python3-dev libldap2-dev
```

После этого снова введите первую команду. Проверить корректность установки версии можно командой ```pyenv versions```. Должна быть строка с указанной версией, например:
```bash
* system (set by /home/user/.pyenv/version)
  3.11.1
```

Теперь клонируем репозиторий и переходим в него по команде ниже, после чего инсталлируем пакет и зависимости.
```bash
git clone git@github.com:IgorGakhov/Hackathon-DatSanta-2022.git && cd Hackathon-DatSanta-2022
```

Зависимости проекта установит Poetry, когда вы введете команду ```poetry install```. Новые зависимости добавлять исходя из деления продакшен/девелопер. Линтер [flake8](https://flake8.pycqa.org/en/latest/) предустановлен, при работе с JSON используем модуль стандартной библиотеки [json](https://docs.python.org/3/library/json.html), необходимые команды при разработке можно найти в Makefile. Не забудьте настроить нужный интерпретатор!
