DROP DATABASE IF EXISTS snsapp;

DROP USER IF EXISTS 'testuser'@'%';


CREATE USER 'testuser'@'%' IDENTIFIED BY 'testuser';

CREATE DATABASE IF NOT EXISTS snsapp
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;


GRANT ALL PRIVILEGES ON snsapp.* TO 'testuser'@'%';

FLUSH PRIVILEGES;

USE snsapp;

CREATE TABLE
    users (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        mail_address VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        updated_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        PRIMARY KEY (id),
        UNIQUE KEY uq_users_mail_address (mail_address)
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
        status ENUM('BASIC', 'START', 'STANDARD', 'EXPERT') NOT NULL,
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



INSERT INTO users (mail_address, password)
VALUES 
  ('taro@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244'),
  ('jiro@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244'),
  ('tanaka@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244'),
  ('suzuki@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244'),
  ('satou@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244');

INSERT INTO books (title, introduction)
VALUES
  ('マスタリングTCP/IP―入門編―(第6版)', 'TCP/IP解説書の決定版! 時代の変化によるトピックを加え内容を刷新!
本書は、ベストセラーの『マスタリングTCP/IP 入門編』を時代の変化に即したトピックを加え、内容を刷新した第6版として発行するものです。豊富な脚注と図版・イラストを用いたわかりやすい解説により、TCP/IPの基本をしっかりと学ぶことができます。プロトコル、インターネット、ネットワークについての理解を深める最初の一歩として活用ください。'),
  ('Linux標準教科書 Ver.4.0.1', '『Linux標準教科書』は、Linux初心者の方が基礎からLinuxを学ぶために最適な「基本的なLinuxのコマンド操作と簡単なシステム管理を行うことができる」教科書です。
本教科書は、Linux技術者認定試験（リナック）【LinuC レベル 1 認定】（ https://linuc.org/ ）の 101 試験と 102 試験の学習範囲に含まれる基本的なコマンド、ネットワークの設定と管理、ファイル管理など、Linuxの基礎知識を系統立てて学べるように構成されており、Linuxを初めて触る初学者が独学で手を動かして学習することができる演習中心のテキストです。
本教科書はすでに20万回以上ダウンロードされ、「授業でも独学でも使える実践的な教科書」として学校教育、若手エンジニア教育、個人学習などに広くご利用いただいています。
本教科書で学習することにより、Linuxの体系的な知識を身につける準備ができたことになります。次のステップで「LinuC レベル1」の認定取得に向けた学習をすることにより、業務で Linux サーバーの操作と運用が行えるスキルの習得を目指すことができます。
本教科書は、LinuC（Linux技術者認定試験 リナック）（ https://linuc.org/ ）を実施しているNPOのLPI-Japanが開発した教材であり、LinuC（リナック）の合格を目指す方々にもお勧めの教材です。 LPI-Japan では、本教科書の提供を通じ、Linux/OSS技術者の育成と技術力向上、およびLinux/OSS環境の利用推進を支援していきます。
本教科書はIT技術者コミュニティ「LinuC Open Network（ https://linuc.community/ ）」の学習教材開発プロジェクトの協力により開発されました。今後もコミュニティ内での意見交換やレビューなどを通じて、最新の技術動向への対応や新たなコンテンツの追加などのアップデートを随時行っていきます。'),
 ('Webを支える技術 ―― HTTP，URI，HTML，そしてREST', 'Webは誕生から20年で爆発的な普及を果たし，17億人のユーザと2億台のサーバを抱える巨大システムへと成長しました。Webがここまで成功した秘密は，その設計思想，いわゆるアーキテクチャにあります。Webのアーキテクチャ，そしてHTTP，URI，HTMLといったWebを支える技術は，Webがどんなに巨大化しても対応できるように設計されていたのです。
私たちが作る個々のWebサービスも，Webのアーキテクチャにのっとることで成功へとつながります。Webのアーキテクチャに正しく適応したWebサービスは，情報が整理され，ユーザの使い勝手が向上し，ほかのサービスと連携しやすくなり，将来的な拡張性が確保されるからです。
本書のテーマは，Webサービスの実践的な設計です。まずHTTPやURI，HTMLなどの仕様を歴史や設計思想を織り交ぜて解説します。そしてWebサービスにおける設計課題，たとえば望ましいURI，HTTPメソッドの使い分け，クライアントとサーバの役割分担，設計プロセスなどについて，現時点のベストプラクティスを紹介します。');

INSERT INTO recommends (user_id, book_id, evaluation, status, message)
VALUES
    (1, 1, 5, 'START', '知りたいことが書いてあってよかった。'),
    (2, 1, 2, 'BASIC', 'あまり面白くなかった'),
    (3, 1, 2, 'START', '普通。'),
    (4, 1, 5, 'EXPERT', '久しぶりに読み直した。'),
    (5, 1, 3, 'STANDARD', 'よかった。');

INSERT INTO categories (category)
VALUES
    ('Web'),
    ('Linux'),
    ('ネットワーク');

INSERT INTO book_categories (book_id, category_id)
VALUES
    (1, 1),
    (1, 3),
    (2, 2),
    (3, 1);

INSERT INTO keywords (keyword)
VALUES
    ('Linuxコマンド'),
    ('Viエディタ'),
    ('Web'),
    ('HTTP'),
    ('HTML'),
    ('REST'),
    ('TCP/IP');

INSERT INTO book_keywords (book_id, keyword_id)
VALUES
    (1, 7),
    (2, 1),
    (2, 2),
    (3, 3),
    (3, 4),
    (3, 5),
    (3, 6);

