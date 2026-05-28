# ReadStage

## ① リポジトリのクローン

リポジトリをクローンします。

```
git clone git@github.com:Spring-Hackathon-2026-F-team/ReadStage.git
```

ディレクトリに移動します。

```
cd ReadStage
```

## ② 環境変数ファイル（.env）の作成

- Mac、Windows(PowerShell、Git Bash)の場合

```
cp .env.example .env
```

- Windows(コマンドプロンプト)の場合

```
copy .env.example .env
```

## ③Docker コンテナのビルドと起動

### コンテナのビルド

docker-compose.yml を元にコンテナイメージをビルドします。  
初回または依存パッケージを更新(requirements.txt)したときに実行してください。  
※docker-compose.yml があるディレクトリで実行してください。

```
docker compose build
```

### コンテナの起動

コンテナを起動します。

```
docker compose up
```

`-d` をつけるとバックグラウンドで起動します。

```
docker compose up -d
```

### ブラウザで確認

ブラウザで以下の URL にアクセスしてください。

```
http://localhost:55000/
```

## ④MySQL の操作方法

### MySQL コンテナへの接続

MySQL コンテナに接続するには、以下のコマンドを実行します。

```
docker exec -it MySQL bash
```

その後、MySQL に接続します。

```
mysql -u root -p
```

パスワードを聞かれたら、.env ファイルに記載されている MYSQL_ROOT_PASSWORD の値を入力してください。

```
Enter password:
```

### テストユーザーについて

初期データとして、以下のテストユーザーが登録されています。
| ユーザー名 | パスワード |
|------------|------------|
| taro@example.com | test1234 |
| jiro@example.com | test1234 |
| tanaka@example.com | test1234 |
| suzuki@example.com | test1234 |
| satou@example.com | test1234 |

### プリセットの書籍について
| ID | 書籍タイトル | カテゴリ | キーワード |
|------------|------------|------------|------------|
| 1 | マスタリングTCP/IP―入門編―(第6版) | Web, ネットワーク | TCP/IP |
| 2 | Linux標準教科書 Ver.4.0.1 | Linux | Linuxコマンド, Viエディタ |
| 3 | Webを支える技術 ―― HTTP，URI，HTML，そしてREST | Web | Web, HTTP, HTML, REST |



## その他

### コンテナの停止

コンテナを停止します。

```
docker compose down
```

### ディレクトリ構成

```

```
