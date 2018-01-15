# Скрипты сборок приложения
Скрипты сборок находятся в каталоге build.\
Запускать необходимо из корневого каталога проекта.

```
$ build/build
$ build/build --publish
$ build/build shell
$ build/build_market
```

## Важно!
В build/common/publish/confluence/update_confluence_page.py используется хеш авторизации Base64 Алексея Фальштынского. Скрипт редактирует страницы от его лица.\
В скрипте build/common/publish/save_builds/save_builds_json.py используется личный токен авторизации в GitLab Алексея Фальштынского.\
Коммиты строго запрещены! Только после смены токена авторизации на ваш.\

## Инструментарий
Собирать необходимо на MacOS. XCode последней версии\
Python и Ruby входят в состав MacOS, но если они вдруг отсутствуют - необходимо установить\
Для работы с XCode из консоли необходимо поставить Ruby-библиотеку xcodeproj:

```
$ [sudo] gem install xcodeproj
```

Для Python необходимо установить библиотеки для работы с http и шаблонизатором mustache:

```
$ [sudo] pip install requests
$ [sudo] pip install pystache
```

## Сборки под стенды
Скрипт build/build настроен собирать сборки под любой стенд, любую сборку (ios, android), в любом режиме (debug, release) и для любой ветки или сразу набор сборок.\
Требуемые сборки указыаются первым параметром. Если ни одного из вариантов указано не будет, соберутся все сборки, для всех стендов, во всех режимах.\
Возможные варианты, целиком под стенд:

```
shell  - собирает сборки ios, android в режимах debug, release для стенда shell
qatar  - собирает сборки ios, android в режимах debug, release для стенда qatar
test01 - собирает сборки ios, android в режимах debug, release для стенда test01
online - собирает сборки ios, android в режимах debug, release для стенда online
```

С указанием режима сборки:

```
shell_debug    - собирает сборки ios, android в режиме debug для стенда shell)
qatar_debug    - собирает сборки ios, android в режиме debug для стенда qatar)
test01_debug   - собирает сборки ios, android в режиме debug для стенда test01)
online_debug   - собирает сборки ios, android в режиме debug для стенда online)
shell_release  - собирает сборки ios, android в режиме release для стенда shell)
qatar_release  - собирает сборки ios, android в режиме release для стенда qatar)
test01_release - собирает сборки ios, android в режиме release для стенда test01)
online_release - собирает сборки ios, android в режиме release для стенда online)
```

С указанием конкретной платформы:

```
shell_debug_ios        - собирает сборки ios в режиме debug для стенда shell)
qatar_debug_ios        - собирает сборки ios в режиме debug для стенда qatar)
test01_debug_ios       - собирает сборки ios в режиме debug для стенда test01)
online_debug_ios       - собирает сборки ios в режиме debug для стенда online)
shell_debug_android    - собирает сборки android в режиме debug для стенда shell)
qatar_debug_android    - собирает сборки android в режиме debug для стенда qatar)
test01_debug_android   - собирает сборки android в режиме debug для стенда test01)
online_debug_android   - собирает сборки android в режиме debug для стенда online)
shell_release_ios      - собирает сборки ios в режиме release для стенда shell)
qatar_release_ios      - собирает сборки ios в режиме release для стенда qatar)
test01_release_ios     - собирает сборки ios в режиме release для стенда test01)
online_release_ios     - собирает сборки ios в режиме release для стенда online)
shell_release_android  - собирает сборки android в режиме release для стенда shell)
qatar_release_android  - собирает сборки android в режиме release для стенда qatar)
test01_release_android - собирает сборки android в режиме release для стенда test01)
online_release_android - собирает сборки android в режиме release для стенда online)
```

Перечисленные параметры можно комбинировать в любом количестве, важно, чтобы этот набор параметров был первым.\

Для обновления исходников перед сборкой указать --update:

```
build/build shell --update
```

Сборка с данным флагом анализирует изменение package.json - в случае изменения будут переустановлены пакеты node_modules и плагины plugins.\

Для принудительной переустановки пакетов node_modules указать --npm_install:

```
build/build shell --npm_install
```

Для выполнения хака ios сборки для стенда с невалидным сертификатом указать --hack:

```
build/build shell --hack
```

Для переопределения каталога сборок указать --outputPath:

```
build/build shell --outputPath build/folder
```

Для указания ветки сборки --branch (по умолчанию ветка текущая):

```
build/build shell --branch release
```

Для публикации после сборки указать флаг --publish:

```
build/build shell qatar --update --publish
```

Публикация включает в себя:
- архивацию сборок (build/common/publish/archive/archive)
- публикацию в dropbox (build/common/publish/dropbox/dropbox_upload)
- обновление страницы сборок в конфлюенсе (build/common/publish/confluence/update_confluence_page.py)
- отправку письма заинтересованным лицам (build/common/publish/email/send_email_ok.py)
- отправку письма об ошибке сборки, если не найден хотя бы один файл из собираемых (build/common/publish/email/send_email_error.py)

Данные для каждого стенда заданы в build/common/constants:
- список всех стендов
- урлы на стенды
- общая часть названия проекта
- общая часть идентификатора приложения
- флаг enableSSLPinning для каждого стенда (проверка включена для банковских стендов)
- страницы в конфлюенсе для веток develop и release
- данные для сборки в маркет

Название проекта формируется константной частью, названием стенда и режимом сборки.\
Например:

```
UL-shell.ipa                    - ios приложение для shell в режиме release
UL-shell-d.ipa                  - ios приложение для shell в режиме debug
android-armv7-release-shell.apk
android-x86-release-shell.apk   - android приложения для shell в режиме release
android-armv7-debug-shell.apk
android-x86-debug-shell.apk     - android приложения для shell в режиме debug
```

Аналогично для остальных стендов (отличие в shell).\

Идентификаторы приложений формируются из константой части, названия стенда и режима сборки для возможности установить абсолютно все приложения одновременно.\
Например:

```
ru.softlab.rshb.mbul.shell   - id приложения для shell в режиме release
ru.softlab.rshb.mbul.shell.d - id приложения для shell в режиме debug
```

Аналогично для остальных стендов (отличие в shell).\

Данные о сборках сохраняются в файлы build/data builds_current.json (информация о текущей последней сборке, пересоздается) и builds.json (полная информация о всех сборках, используется для дальнейших)\
Формат json:

```
{
  "release": {  // ветка
    "shell": {  // стенд
      "debug": {  // режим debug
        "android": {  // для андроида
          "merged_merge_request_list": [], // мерджи, вошедшие в последнюю сборку
          "opened_merge_request_list": [], // мерджи, ожидающие включение в сборку
          "last_merge_request_id": 6920,  // id последнего включенного мерджа
          "urls": [ // урлы на сборки в dropbox
            "https://www.dropbox.com/s/1knk0b44je6m111/android-armv7-debug-shell.apk",
            "https://www.dropbox.com/s/nppf426d8eqj222/android-x86-debug-shell.apk"
          ],
          "date": "24.11.2017 00:18", // дата время сборки
          "revision": "f4769c9b"  // ревизия сборки
        },
        "ios": {  // для иос
          "merged_merge_request_list": [],
          "opened_merge_request_list": [],
          "last_merge_request_id": 6920,
          "urls": [
            "itms-services://?action=download-manifest&amp;amp;url=https://dl.dropboxusercontent.com/s/heybtj03j795333/UL-shell-d.plist"
          ],
          "date": "24.11.2017 00:18",
          "revision": "f4769c9b"
        }
      },
      "release": { // режим release
        "android": {
          "merged_merge_request_list": [],
          "opened_merge_request_list": [],
          "last_merge_request_id": 6920,
          "urls": [
            "https://www.dropbox.com/s/us8h46dz3oa9444/android-armv7-release-shell.apk",
            "https://www.dropbox.com/s/kz7e7xw67xxi555/android-x86-release-shell.apk"
          ],
          "date": "24.11.2017 00:18",
          "revision": "f4769c9b"
        },
        "ios": {
          "merged_merge_request_list": [],
          "opened_merge_request_list": [],
          "last_merge_request_id": 6920,
          "urls": [
            "itms-services://?action=download-manifest&amp;amp;url=https://dl.dropboxusercontent.com/s/74m8ppkds4h0666/UL-shell.plist"
          ],
          "date": "24.11.2017 00:18",
          "revision": "f4769c9b"
        }
      }
    },
    "qatar": {
      ... // аналогично
    },
    "test01": {
      ... // аналогично
    },
    "online": {
      ... // аналогично
    }
  }
}
```

Для обновления страницы о сборках в конфлюенсе используется шаблонизатор [mustache](https://mustache.github.io/mustache.5.html) - пакет Python [pystache](https://github.com/defunkt/pystache).\
Шаблон задан в build/common/publish/confluence/page.mustache.\
Для заполнения шаблона сохраненные данные о сборках в build/data/builds.json конвертируются в структуру вида:

```
{
  "stand": [  // массив данных по каждому стенду
    {
      "name": "shell",
      "mode": [ // массив режимов сборки стенда
        {
          "name": "debug",
          "platform": "android",
          "date": "24.11.2017 00:18",
          "revision": "f4769c9b",
          "urls": [
            {
              "url": "https://www.dropbox.com/s/1knk0b44je6m777/android-armv7-debug-shell.apk"
            },
            {
              "url": "https://www.dropbox.com/s/nppf426d8eqj888/android-x86-debug-shell.apk"
            }
          ]
        },
        {
          "name": "debug",
          "platform": "ios",
          "date": "24.11.2017 00:18",
          "revision": "f4769c9b",
          "urls": [
            {
              "url": "itms-services://?action=download-manifest&amp;amp;url=https://dl.dropboxusercontent.com/s/heybtj03j795999/UL-shell-d.plist"
            }
          ],
        },
        {
          "name": "release",
          "platform": "android",
          "date": "24.11.2017 00:18",
          "revision": "f4769c9b",
          "urls": [
            {
              "url": "https://www.dropbox.com/s/us8h46dz3oa9111/android-armv7-release-shell.apk"
            },
            {
              "url": "https://www.dropbox.com/s/kz7e7xw67xxi222/android-x86-release-shell.apk"
            }
          ]
        },
        {
          "name": "release",
          "platform": "ios",
          "date": "24.11.2017 00:18",
          "revision": "f4769c9b",
          "urls": [
            {
              "url": "itms-services://?action=download-manifest&amp;amp;url=https://dl.dropboxusercontent.com/s/74m8ppkds4h0333/UL-shell.plist"
            }
          ]
        }
      ]
    },
    {
      "name": "qatar",
      ...
    },
    ...
  ]
}
```

## Сборка для маркета
Скрипт build/build_market настроен собирать архив .xcarchive ios и unsigned apk android для передачи в банк для последующей публикации.\
Возможно задать конкретную платформу для сборки (без указания собираются обе), например:

```
$ build/build_market ios
$ build/build_market android
```

После успешной сборки заданных платформ производится этап публикцаии (build/common/publish/publish_market):
- сборки переименовываются с добавлением даты времени сборки
- запаковываются в запароленный zip архив
- архивируется на машине
- публикуется в dropbox
- ссылка на архив в dropbox отправляется по почте заинтересованным лицам

Данные для сборок в маркет заданы в constants:
- название приложения
- id приложения (да, у ios и android разные id по вине банка)
- url пром стенда
- версии сборок ios и android
