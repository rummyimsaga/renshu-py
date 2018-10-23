[実行環境]
- Vagrant(2.1.5)
    Box: http://cloud.centos.org/centos/7/vagrant/x86_64/images/CentOS-7-x86_64-Vagrant-1809_01.VirtualBox.box
    Plugin: vagrant-hostsupdater, vagrant-share, vagrant-vbguest
- VirtualBox(5.2.18)

[手順]
0)
  1.必要なリポジトリ、ライブラリ等をインストール
    $ sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm
    $ sudo yum install -y python36u python36u-debug python36u-devel python36u-libs python36u-pip python36u-tools
    $ sudo ln -s /usr/bin/python3.6 /usr/local/bin/python3
    $ sudo ln -s /usr/bin/pip3.6 /usr/local/bin/pip3
    $ su
    # pip3 install --upgrade pip
    # pip3 install --upgrade requests
    # pip3 install --upgrade google-api-python-client oauth2client
    # exit
  2.Google Cloud Consoleから「APIとサービス」->「認証情報」
    「認証情報を作成」-> 「OAuth2.0 クライアントID」->「その他」->「作成」でクライアントIDを作成
    「認証情報」の画面に戻ったら作成したクライアントIDのリストの一番右のアイコン(ダウンロードアイコン)を
    クリックしてjsonを保存する
    このとき、ファイル名を「gdrivecredentials.json」とし、GetAndSaveToGoogleDrive-v0.2.pyと同じフォルダに置く

1)実行
  $ python3 GetAndSaveToGoogleDrive-v0.2.py --noauth_local_webserver
  
2)認証
  認証されていない場合)
    1.実行時に
      Go to the following link in your browser:
      のメッセージの後に続いてhttps://から始まるリンクが表示されるのでメモ
    2.リンクをブラウザで見るとGoogleのログイン画面になるため、ログインする
    3.コードが表示されるのでメモ
    4.Enter verification code:の後に続けてコードを入力しEnterを押下
    
3)認証後
  1.Please Input DL Link >> に続いて取得したいファイルのURLを入力
  2.Continue?([Y]es/[N]o)と表示されるのでy,nのいずれかを入力
  3.yの場合1.に戻る
    nの場合4.に進む
    なお同時に取得可能なファイル数は5つまでとしている
  4.自動でGoogleDriveにフォルダ作成、ダウンロードしたファイルの格納が行われる
  
