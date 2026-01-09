# (アプリ名)

## 概要

時間割を記録できるWEBアプリです。授業名、教室名、教授名、メモ、課題を保存できます。また、同一の授業を複数のコマに配置可能です。

## デプロイ先URL

https://your-app-url.com

## 機能

| 画面 | 機能概要 |
| :---: | :--- |
| <img src="images/screenshot_index.png" alt="授業一覧" width="300"> | **授業一覧**<br>すべての授業を表示します。授業詳細画面や追加画面に移行できます。 |
| <img src="images/screenshot_add_class.png" width="300"> | **授業追加**<br>新規授業を追加したり、既存の授業から選択して追加できます。 |
| <img src="images/screenshot_class_info.png" width="300"> | **授業詳細**<br>選択した授業の情報を閲覧、編集できます。 |
| <img src="images/screenshot_homework.png" width="300"> | **課題一覧**<br>すべての課題を閲覧し、完了済みかどうかを編集できます。 |

## 使用技術

| Category | Technology |
| :--- | :--- |
| **Language** | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) |
| **Framework & Libs** | ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![WhiteNoise](https://img.shields.io/badge/whitenoise-%23092E20.svg?style=for-the-badge&logoColor=white) |
| **Frontend** | ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![Bootstrap](https://img.shields.io/badge/bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white) |
| **Database** | ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) |
| **Infrastructure** | ![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white) ![Render](https://img.shields.io/badge/Render-%2346E3B7.svg?style=for-the-badge&logo=render&logoColor=white) |

## なぜ作ったのか

本アプリは、大学のサークル活動の一環としてdjangoやweb開発の学習用に作成したものです。  
現在使用している時間割アプリに同一の授業を複数のコマに配置する機能が無かったため、題材を時間割アプリに決定しました。

## こだわったポイント

1. **レスポンシブ対応:** スマホでの利用を想定し、gridの大きさやフォントサイズなどを画面の大きさによって調整しました。
2. **授業の同期:** 同一の授業を複数のコマに配置する機能を実装しました。
3. **少ないページ更新:** Java Scriptのfetch APIを活用した非同期通信を用い、授業の追加、編集、削除の際にページ更新を挟まないストレスフルなアプリを目指しました。

## 苦労した点

* **Uzuki Alto**
  * **学習面:** djangoとcssはほぼ何も知らない状態からのスタートだったので、アプリの作成と平行しての学習が大変でした。djangoは[このサイト](https://str1ng-blog.vercel.app/)を参考にしました。
  * **レスポンシブ対応:** 授業一覧画面をスマートフォンの縦画面で見たときに縦に引き伸ばされてしまい、視認性と操作性のバランスが難しかったです。

## 今後の展望

* 追加したい機能
  * 課題一覧のソート機能
  * Google カレンダーとの連携
  * 時間割共有機能
  * 出席日数、欠席日数、遅刻回数の管理
* 修正したいこと
  * 課題一覧へのアクセスの悪さ

## 開発者

[![Uzuki Alto](https://img.shields.io/badge/Uzuki_Alto-121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/uzukialto)  
[![kete113](https://img.shields.io/badge/kete113-121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/kete113)
