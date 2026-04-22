DROP DATABASE IF EXISTS readstage;

DROP USER IF EXISTS 'testuser'@'%';


CREATE USER 'testuser'@'%' IDENTIFIED BY 'testuser';

CREATE DATABASE IF NOT EXISTS readstage
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;


GRANT ALL PRIVILEGES ON readstage.* TO 'testuser'@'%';

FLUSH PRIVILEGES;

USE readstage;

CREATE TABLE
    users (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        updated_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        PRIMARY KEY (id),
        UNIQUE KEY uq_users_email (email)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE
    books (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        title VARCHAR(50) NOT NULL,
        introduction TEXT NOT NULL,
        created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        updated_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        PRIMARY KEY (id),
        UNIQUE KEY uq_books_title (title)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE
    recommends (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id BIGINT UNSIGNED NOT NULL,
        book_id BIGINT UNSIGNED NOT NULL,
        evaluation INT NOT NULL,
        status ENUM('START/入門', 'BASIC/基礎', 'STANDARD/応用', 'EXPERT/発展') NOT NULL,
        message VARCHAR(140),
        delete_flag TINYINT(1) DEFAULT 0,
        created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        updated_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        deleted_at DATETIME (6) DEFAULT NULL,
        PRIMARY KEY (id),
        KEY idx_comments_user_id (user_id),
        KEY idx_books_book_id (book_id),
        CONSTRAINT fk_recommends_user FOREIGN KEY (user_id) REFERENCES users (id),
        CONSTRAINT fk_recommends_book FOREIGN KEY (book_id) REFERENCES books (id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE
    categories (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        category VARCHAR(20) NOT NULL,
        created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        updated_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        PRIMARY KEY (id),
        UNIQUE KEY uq_categories_category (category)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;


CREATE TABLE
    book_categories (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        book_id BIGINT UNSIGNED NOT NULL,
        category_id BIGINT UNSIGNED NOT NULL,
        created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        updated_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        PRIMARY KEY (id),
        KEY idx_book_categories_books_book_id (book_id),
        KEY idx_book_categories_categories_category_id (category_id),
        CONSTRAINT fk_book_categories_books_book_id FOREIGN KEY (book_id) REFERENCES books (id),
        CONSTRAINT fk_book_categories_categories_category_id FOREIGN KEY (category_id) REFERENCES categories (id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE
    keywords (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        keyword VARCHAR(20) NOT NULL,
        created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        updated_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        PRIMARY KEY (id),
        UNIQUE KEY uq_keywords_keyword (keyword)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE
    book_keywords (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        book_id BIGINT UNSIGNED NOT NULL,
        keyword_id BIGINT UNSIGNED NOT NULL,
        created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        updated_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        PRIMARY KEY (id),
        KEY idx_book_keywords_books_book_id (book_id),
        KEY idx_book_keywords_keyword_id (keyword_id),
        CONSTRAINT fk_book_keywords_books_book_id FOREIGN KEY (book_id) REFERENCES books (id),
        CONSTRAINT fk_book_keywords_keywords_keyword_id FOREIGN KEY (keyword_id) REFERENCES keywords (id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;



INSERT INTO users (email, password)
VALUES 
    ('taro@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244'),
    ('jiro@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244'),
    ('tanaka@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244'),
    ('suzuki@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244'),
    ('satou@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244'),
    ('isii@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244'),
    ('yamada@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244'),
    ('katou@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244'),
    ('gotou@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244'),
    ('nakano@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244');

INSERT INTO books (title, introduction)
VALUES
    ('マスタリングTCP/IP―入門編―(第6版)', 'ネットワーク初心者に向けてTCP/IPの基礎を解説した技術書。「ネットワーク」という抽象的な分野を図やイラストを使って具体的かつ体系的に学べる内容です。ITエンジニアにとってネットワークは避けて通れないテーマなのでおすすめです。'),
    ('Linux標準教科書 Ver.4.0.1', 'Linux初心者が基礎から学べる無料の学習教材です。具体的な演習問題が含まれており、ハンズオン形式で学習することができます。Linux OSは現代のITエンジニアにとって必須と言える重要な分野ため、おすすめします。また、Linux技術者認定資格のLinuCの標準教科書となっています。'),
    ('Webを支える技術 ―― HTTP，URI，HTML，そしてREST', 'Webはどのように動いているのでしょうか？未経験エンジニアがこれからWeb開発を学ぶ上で、まずはWebシステムを知る必要があります。また、RESTアーキテクチャについて詳しく学べるため、自分でAPI設計や開発を行う際にも役に立ちます。'),
    ('SQLアンチパターン　第2版', 'データベース設計やSQLクエリの記述における「失敗例」を体系的に解説している技術書。実務で直面しがちな課題や失敗事例を学び、効率的なデータベースの運用スキルが身に付きます。初心者から脱初心者をめざす中級者におすすめできる一冊です。'),
    ('スッキリわかるPython入門　第2版', 'Python初心者やプログラミング未経験者に向けて書かれたPythonの基礎を学べる技術書。専門用語は避けつつ丁寧な解決があり、未経験者でも安心して学習できます。基本文法からオブジェクト思考など実務でも役立つ内容が網羅されていて、演習問題をハンズオン形式で学習することができます。'),
    ('改訂新版　良いコード／悪いコードで学ぶ設計入門', 'ソフトウェア開発において、コードが「変更しづらい」、「保守が難しい」と感じている読者に向けて、悪いコードをどのように改善して良いコードにしていくか、実務で役に立つノウハウが詰まった1冊です。未経験エンジニアでも理解しやすく、「どうしてこのような設計が必要なのか」を納得感をもって学ぶことができます。'),
    ('アジャイルサムライ　－達人開発者への道－', 'システムやソフトウェア開発でアジャイル開発を始めたい方向けの技術書。アジャイル開発は短いサイクルで計画・設計・実装・テストを繰り返し、段階的にシステムを完成させていく手法で、仕様変更の柔軟性やリソースが限られた現場特有の課題に対処しながら、効率よく開発していくための方法論が示されています。'),
    ('統計学が最強の学問である', 'データ社会で活躍するために統計学の本質を、日常生活や仕事で役に立つ具体例を通じて学ぶことができます。膨大な情報から価値ある洞察を得る能力が身に付きます。難しい数式は極力避けて書かれているため、数学が苦手な未経験エンジニアにも安心して読み進められます。'),
    ('Amazon Web Services 基礎からのネットワーク＆サーバー構築', 'クラウドコンピューティングの代表的なサービスであるAWSを使いながら、インフラ技術を実践的に学ぶることができる初心者向けの入門書です。自分でネットワークやサーバーを構築できるというゴールまで導いてくれる一冊です。'),
    ('ホワイトハッカーの教科書', 'サイバーセキュリティに興味がある未経験エンジニアにおすすめの書籍です。サイバーセキュリティの基礎から実践的なスキルまで体系的に学ぶことができます。また、サイバー攻撃を防ぐ専門家としての心構え、学習のステップについても書かれています。'),
    ('体系的に学ぶ安全なWebアプリケーションの作り方　第2版', 'Webセキュリティの必須知識（SQL注入、XSS、CSRF等）を、脆弱性の発生原理・攻撃手法・対策まで実例付きで解説した技術書です。初学者にも分かりやすく、セキュアな開発を行う全てのエンジニア必読の書です。本書は開発者が「攻撃者の視点」を持ってセキュアなコードを書くためのバイブルであり、Webアプリケーションの脆弱性を根本から理解したい人におすすめの一冊です。'),
    ('マスタリングTCP/IP 情報セキュリティ編 (第2版)', 'ネットワークセキュリティの基礎から応用技術までを体系的にまとめた教科書です。暗号技術、認証、PKI、セキュリティプロトコル、ホスト・ネットワーク・Webアプリのセキュリティ対策を包括的に解説し、第2版では最新技術やコンセプトの追記、情報セキュリティ概論の強化が行われています。'),
    ('暗号技術入門 第3版　秘密の国のアリス【中級】', '対称暗号、公開鍵暗号、デジタル署名、SSL/TLSなど、現代の暗号技術の仕組みを、物語仕立てのやさしい文章と豊富な図解で解説した名著です。第3版ではSHA-3などの最新技術が追加され、セキュリティの基礎から実践的な応用までを体系的に学べる入門書の決定版です。'),
    ('改訂3版JavaScript本格入門　～モダンスタイルによる基礎から現場での応用まで', 'JavaScriptの基本から現代的な開発手法までを網羅した、標準的な入門書です。ECMAScript 2022の標準仕様に対応し、基本文法から開発に欠かせない応用トピックまで解説しています。JavaScriptを多少使えるけど基本が不安な方、ECMAScript 2022による新たなJavaScript記法を学びたい方におすすめの一冊です。'),
    ('達人に学ぶDB設計徹底指南書 第2版', 'RDB設計の基礎から正規化、インデックス、ER図までを体系的に解説し、理論と現実のギャップを埋める実践的なアプローチを提示しています。論理設計の重要性を強調し、性能と保守性を両立させる設計手法やSQL特有の難所を詳しく解説しています。データベースに興味のあるエンジニア必携の実践的書籍です。'),
    ('いちばんやさしいGit&GitHubの教本 第3版', 'GitとGitHubの基本的な使い方から実践的なワークフローまでを網羅した入門書です。初心者でも理解しやすいように構成されており、コマンドライン操作を中心に、実際の開発現場で役立つ知識を習得できる内容となっています。特に、バージョン管理やチーム開発の基礎を学びたい方に適した一冊です。'),
    ('仕組みと使い方がわかる Docker&Kubernetesのきほんのきほん', '若手エンジニアやバックエンドの技術にあまり詳しくない方に向けて書かれたDockerの入門書です。Dockerがどのような仕組みで動いているのか、きちんと理解できるようにイラストを使用して解説しています。また、Docker ComposeやKubernetesについても、初歩から説明があり、ひととおり動かすまでの流れをハンズオンを交えて解説しています。'),
    ('Flask本格入門　～やさしくわかるWebアプリ開発～', 'FlaskはPythonでアプリケーション開発を行うためのフレームワークです。本書は，Flaskの最新のバージョン2.3.2に対応し、ルーティングの基礎、データ操作の方法、テンプレート／Formの活用方法、Webアプリケーション開発の一連の流れが学べます。はじめてFlaskでWebアプリケーションを開発したい人におすすめの一冊です。'),
    ('Web API: The Good Parts', 'APIは、設計次第で使いづらいものになってしまうだけではなく、保守運用も難しくなってしまいます。本書はより良いAPI設計するための方法を解説した書籍です。HTTPを通信形式として利用したAPIの中でも広義のRESTの設計を解説しています。ウェブAPIを開発するエンジニア、開発者におすすめの一冊です。');

INSERT INTO recommends (user_id, book_id, evaluation, status, message)
VALUES
    (1, 1, 1, 'START/入門', 'ネットワークの基礎が体系的にまとめられていますが、初学者でもう少し簡単な書籍からはじめたいと思いました。'),
    (6, 1, 5, 'EXPERT/発展', ''),
    (8, 1, 2, 'START/入門', ''),
    (7, 1, 5, 'STANDARD/応用', 'ネットワークエンジニア以外でもすべてのエンジニアにおすすめしたい書籍です。'),
    (2, 1, 4, 'BASIC/基礎', 'ページ数が400ページくらいで基礎にしてはボリューミーで読み切るのが大変でした。内容的には大変勉強になりました。'),
    (9, 1, 3, 'BASIC/基礎', 'ネットワークに関する書籍でもっとも有名だと思いますが、読み切るのが大変。'),
    (3, 1, 3, 'START/入門', 'OSI参照モデルなどネットワークの抽象的な概念が多く、もう少し初歩の導入的な書籍で勉強してから学習しなおしたい。'),
    (4, 1, 5, 'EXPERT/発展', 'ネットワーク技術の全体像を体系的かつ網羅的に学ぶことができる。ITエンジニアには必須の学習初期だと思います。'),
    (5, 1, 3, 'STANDARD/応用', 'ネットワーク初学者が中級者へのステップアップするのに必要な知識が書かれています。資格試験にも有効です。'),
    (10, 1, 4, 'STANDARD/応用', 'ネットワーク初学者が中級者へのステップアップするのに必要な知識が書かれています。資格試験にも有効です。'),
    (3, 2, 3, 'START/入門', 'LinuxのCUIになれるために、ハンズオンでコマンドの練習を繰り返したい。'),
    (1, 2, 4, 'START/入門', '各ネットワークプロトコルの役割やTCP/IPという大枠がよくわからない人は騙されたと思って一度読んでください。'),
    (4, 2, 5, 'EXPERT/発展', 'Linuxの資格試験の標準教科書です。'),
    (6, 3, 4, 'START/入門', 'httpの歴史や成り立ちがじっくり描かれておりわかりやすいです。知識詰め込みタイプの本ではないので読みやすかったです。'),
    (8, 3, 5, 'STANDARD/応用', 'RESTについて、この書籍で勉強して理解できました。'),
    (9, 3, 5, 'EXPERT/発展', ''),
    (1, 4, 3, 'START/入門', '独学で勉強している人には難しいかもしれません。'),
    (5, 4, 4, 'BASIC/基礎', 'データベースの論理設計、物理設計、SQL設計、アプリケーション設計を事例を使ってアンチパターンを紹介してくれている。'),
    (2, 5, 3, 'BASIC/基礎', ''),
    (8, 5, 4, 'START/入門', 'Pythonについて、初心者向けに非常にわかりやすく説明している一冊でした。'),
    (10, 5, 3, 'EXPERT/発展', '網羅性が不十分だが、必要最低限の知識を、手早く学習するにはとても良い本だと思う。');

INSERT INTO categories (category)
VALUES
    ('Web'),
    ('Linux'),
    ('ネットワーク'),
    ('セキュリティ'),
    ('プログラミング言語'),
    ('データベース'),
    ('開発手法'),
    ('統計学'),
    ('クラウドインフラ'),
    ('Webアプリ開発'),
    ('バージョン管理'),
    ('コンテナ技術'),
    ('コーディング'),
    ('チーム開発');

INSERT INTO book_categories (book_id, category_id)
VALUES
    (1, 1),
    (1, 3),
    (2, 2),
    (3, 1),
    (3, 10),
    (4, 5),
    (4, 6),
    (5, 5),
    (6, 5),
    (6, 13),
    (7, 7),
    (7, 14),
    (8, 8),
    (9, 9),
    (10, 4),
    (11, 4),
    (11, 10),
    (12, 4),
    (13, 4),
    (14, 5),
    (14, 10),
    (15, 6),
    (16, 11),
    (17, 12),
    (18, 10),
    (19, 10);

INSERT INTO keywords (keyword)
VALUES
    ('Linuxコマンド'),
    ('Viエディタ'),
    ('Web'),
    ('HTTP'),
    ('HTML'),
    ('REST'),
    ('TCP/IP'),
    ('URI設計'),
    ('ステータスコード'),
    ('OSI参照モデル'),
    ('IP'),
    ('DNS'),
    ('NAT/NAPT'),
    ('TCP/UDP'),
    ('パーミッション'),
    ('プロセス管理'),
    ('ファイル管理'),
    ('シェルスクリプト'),
    ('Python'),
    ('オブジェクト'),
    ('モジュール'),
    ('クラス設計'),
    ('リファクタリング'),
    ('名前設計'),
    ('コメントルール'),
    ('モデリング'),
    ('コレクション'),
    ('アジャイルチーム'),
    ('アジャイルな方向づけ'),
    ('アジャイルな計画'),
    ('プロジェクト運営'),
    ('プログラミング'),
    ('開発プロセス'),
    ('因果推論'),
    ('誤差'),
    ('ランダム化'),
    ('サンプリング'),
    ('ビッグデータ'),
    ('システム構築'),
    ('ネットワーク構築'),
    ('サーバー構築'),
    ('TCP/IP通信'),
    ('ホワイトハッカー'),
    ('脆弱性'),
    ('XSS'),
    ('SQLインジェクション'),
    ('CSRF'),
    ('エスケープ処理'),
    ('暗号技術'),
    ('認証技術'),
    ('PKI'),
    ('セキュリティプロトコル'),
    ('ホストのセキュリティ'),
    ('ネットワークセキュリティ'),
    ('公開鍵'),
    ('JavaScript'),
    ('ECMAScript'),
    ('Node.js'),
    ('CSS'),
    ('WebAPI'),
    ('エンドポイント'),
    ('リクエスト'),
    ('レスポンス'),
    ('SQL'),
    ('RDBMS'),
    ('DB設計'),
    ('ER図'),
    ('正規化'),
    ('スキーマ'),
    ('GitHub'),
    ('リポジトリ'),
    ('ブランチ'),
    ('プルリクエスト'),
    ('Docker'),
    ('Dockerコマンド'),
    ('Docker image'),
    ('Kubernetes'),
    ('Flask'),
    ('ルーティング'),
    ('Jinja2'),
    ('ORM'),
    ('SQLAlchemy'),
    ('バリデーション'),
    ('ナイーブツリー'),
    ('IDリクワイアド'),
    ('キーレスエントリ'),
    ('EAV'),
    ('ポリモーフィック'),
    ('ラウンディングエラー');

INSERT INTO book_keywords (book_id, keyword_id)
VALUES
    (1, 7),
    (2, 1),
    (2, 2),
    (3, 3),
    (3, 4),
    (3, 5),
    (3, 6),
    (3, 8),
    (3, 9),
    (1, 10),
    (1, 11),
    (1, 12),
    (1, 13),
    (1, 14),
    (2, 15),
    (2, 16),
    (2, 17),
    (2, 18),
    (4, 84),
    (4, 85),
    (4, 86),
    (4, 87),
    (4, 88),
    (4, 89),
    (5, 19),
    (5, 20),
    (5, 21),
    (6, 22),
    (6, 23),
    (6, 24),
    (6, 25),
    (6, 26),
    (6, 27),
    (7, 28),
    (7, 29),
    (7, 30),
    (7, 31),
    (7, 32),
    (7, 33),
    (8, 34),
    (8, 35),
    (8, 36),
    (8, 37),
    (8, 38),
    (9, 39),
    (9, 40),
    (9, 41),
    (9, 42),
    (10, 43),
    (11, 44),
    (11, 45),
    (11, 46),
    (11, 47),
    (11, 48),
    (12, 49),
    (12, 50),
    (12, 51),
    (12, 52),
    (12, 53),
    (12, 54),
    (13, 49),
    (13, 50),
    (13, 51),
    (13, 55),
    (14, 56),
    (14, 57),
    (14, 58),
    (14, 5),
    (14, 59),
    (15, 64),
    (15, 65),
    (15, 66),
    (15, 67),
    (15, 68),
    (15, 69),
    (16, 70),
    (16, 71),
    (16, 72),
    (16, 73),
    (17, 74),
    (17, 75),
    (17, 76),
    (17, 77),
    (18, 78),
    (18, 79),
    (18, 80),
    (18, 81),
    (18, 82),
    (18, 83),
    (19, 60),
    (19, 61),
    (19, 62),
    (19, 63),
    (19, 4);