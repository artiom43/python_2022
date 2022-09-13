# Frequently Asked Questions

Для упрощения жизни и атмосферы в чатике - ответы на некоторые популярные вопросы вынесены сюда. 


### Q: Запускается глобальный `pip`/`mypy`/`flake8`, а не из `shad_env`

<details><summary><b>A: [под спойлером]</b></summary>
Для начала нужно проверить какой именно (откуда) пакет вы запускайте 

```shell
# на примере `mypy`
$ which mypy
# [some path here]
```

Если путь не ведёт в папку с `shad_env`, то у вас проблемы =) 

Убедитесь, что вы активировали environment с пакетами
```shell
$ source shad_env/bin/activate  # замените здесь путь до места установки shad_env 

(shad_env)$ .
```
В консоли появится имя окружения перед вводом команды. 

Проверьте ещё раз
```shell
# на примере `mypy`
(shad_env)$ which mypy
# [some path here]
```

Если ничего не изменилось - печально. У пакетов не всегда получается прописать себя в этот скоуп при активации. 

Самый надежный способ запуска пакеты именно для конкретного питона - вызвать его как модуль
```shell
(shad_env)$ which python
(shad_env)$ python -m mypy
```
(при уже включённом `venv`)

</details>


### Q: Локально проходят все тесты, а на сервере ошибка `flake8`/`mypy`

<details><summary><b>A: [под спойлером]</b></summary>
В первую очередь нужно проверить, что вы запускайте тесты и линтеры с учётом файла конфигурации (`setup.cfg`).  

Есть 2 варианта как запустить тесты и линтеры 
* Можно запускать из корня проекта, тогда файл подцепится автоматически
  ```shell
  (shad_env)$ python -m flake8 ./path/to/the/task
  (shad_env)$ python -m mypy ./path/to/the/task
  (shad_env)$ python -m pytest ./path/to/the/task
  ```
* Можно запускать из любой директории, но нужно указать файл ручками
  ```shell
  (shad_env)$ python -m flake8 --config ../../setup.cfg task_name
  (shad_env)$ python -m mypy --config-file ../../setup.cfg task_name
  (shad_env)$ python -m pytest -c ../../setup.cfg task_name
  ```
(при уже включённом `venv`)
</details>


### Q: На сервере какая-то странная ошибка про `.gitlab-ci.yml`

<details><summary><b>A: [под спойлером]</b></summary>
Перед запуском всех тестов проверяется, что файл `.gitlab-ci.yml` не был изменён.

Для этого дополнительно сравнивается файл `.gitlab-ci.yml` в вашем репозитории и самая последняя версия из публичного репозитория. 
Если файлы различаются, то выкидывается ошибка.  
Возникнуть она может даже если вы не меняли файл, но в публичном репозитории он обновился. 

Решение очень простое:
```shell
$ git pull upstream main
```
</details>


### Q: Ошибка импорта библиотеки `testlib`

<details><summary><b>A: [под спойлером]</b></summary>
Часть функций для тестирования ваших решений мы вынесли в отдельную мини-библиотечку, которую можно найти в папке `tools/testlib`

На сервере эта библиотечка устанавливается автоматически.

Локально эта библиотечка так же прописана в `requirements.txt`. Но в случае возникновения ошибок можно её переустановить
```shell
(shad_env)$ python -m pip install --editable tools/testlib
```
(при уже включённом `venv`)
</details>


### Q: gitlab pipeline упал, но задачка точно сделана верно

<details><summary><b>A: [под спойлером]</b></summary>

* Откройте и внимательно прочитайте логи в gitlab pipeline 
  (нужно нажать на красную кнопку `failed` в упавшей джобе и откроются логи)
* Если тестируется несколько задач, то job будет падать если хоть одна из них упала.
  НО: Для всех успешно проверенных задачек баллы будут выставлены независимо от остальных
* Если задачка одна, но падает и нет никаких ошибок, то.. Почитайте логи ещё раз
* Если в логах написано, что баллы выставлены, но их точно нет - багрепортьте в чат, тегая админа
  (и сразу описывая что именно упало и прикрепляя ссылку на пайплайн)

</details>