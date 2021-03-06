# コンテナの環境設定  
コンテナ内にpythonプログラムを配置している想定で環境設定します。ubuntu想定です。  

## ubuntuであることの確認  
/ect/に移動すると、「[ディストリビューション名]-release」というフォルダがある。  
ubuntuの場合は、「lsb-release」がある。  

## sudoのインストール  
まさかのsudoが入っていませんでした。。。下記のコマンドでエラーを吐く場合はapt-getをupdateします。  
```
$ apt install sudo
```

## pipのインストール→pip3のインストール  
これでpython(3)も入ります。  
```
$ apt-get install python(3)-pip
```

## mecabのインストール  
だいたいmecab使ってること多いよね。  
(https://github.com/mengziQ/study_room/tree/master/setup_linux)参照。  

## その他入れたもの  
- bs4  
- requests  
- ssh

## httpによる疎結合を実施するための環境設定  
0. httpリクエスト・レスポンスでデータを送受信するためのプログラムを開発(例ではserver.pyとする)  
1. 上記プログラムの権限を変更し、/usr/binに配置してコマンドとして実行できるようにする  
```
$ chmod +x server.py
$ sudo cp server.py /usr/bin
```
2. 1のままコンテナをエクスポートして業務システム側に受け渡す。業務システム側はイメージをインポートしたら、以下のコマンドで起動する。   
```
port1: 外部からアクセスされるポート番号
port2: コンテナ側のポート番号

$ docker run -p [port1]:[port2] -it [REPOSITORY] server.py
```

※ bashを立ち上げたい場合は以下  
```
bashで中のプログラムを変更するだけならpオプションはなくてもOK
$ docker run -p [port1]:[port2] -it [REPOSITORY] bash
```
※　bashが起動できなかった場合は、/bin/bashを/usr/bin/にコピーすることでエラーが解消した。  

※ pythonのモジュールが使えなくなっていたら、server.pyの1行目に以下を足す  
```
#!/usr/bin/python3
``` 

## httpでのデータの受け渡し処理の参考スクリプト  
以下のコードは[こちら](https://github.com/GINK03/docker-compose-templates)を参考にしています。  

**server.py**  

サーバー側(コンテナ導入側)でのデータ受け渡し処理を記述したスクリプト  

**client.py**  

クライアント側(コンテナの機能を利用する側)でのデータ受け渡し処理を記述したスクリプト  
