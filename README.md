# python ポートフォリオ GUIアプリ
## 課題名：顔画像検出アプリケーション
氏名：白井　正真

## 仕様
- 処理はopenCV，Nunpy，Pillow(画像表示時)を使用．
- Tkinterを用いたGUI開発
- ファイルは定数が入るconfig.pyファイル，CUI時に用いた関数が入るmodule_cui.pyファイル，GUIの配置や実行処理が含まれたss2403.pyからなる．
- ss2403.pyを実行するとSelectボタンが出てきて，その中の画像ファイルを選択するとその写真が表示される．
- Saveボタン(顔検出結果の表示と保存，その結果の数値をcsvファイルへの出力を行う)
- Blurボタン(下のバーによりぼやけ具合を選択でき，値が小さいほどぼやけ度が大きい．これも変更後の画像が保存されるようになっている)
- Changeボタン(ボタンを押すと，ファイルの選択画面が出てきて，選択写真の中の顔を抽出し元の顔と交換する．交換後の写真は二枚保存されるようになっている)
- Sunburnボタン(下のバーにより日焼け具合を選択でき，値が大きいほど日焼け具合が大きくなり，小さいほど日焼け具合が小さくなる．これも変更後の画像が保存されるようになっている)
- Grabcutボタン(ボタンを押すとファイルの選択画面が出てきてGrabcutを行う．変更後の画像は保存される．)

## 使用技術
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

- Python 3.7以上
- Numpy
- Pillow

## 実行方法
```bash
$ python ss2403.py
```

## コメント
- Backボタン(押すと元の画像へ戻る)，Closeボタン(押すとアプリケーションを終了する)を作成した．
- Saveボタン，Blurボタン，Changeボタン，Sunburnボタン，Grabcutボタンを押した場合は二回連続で画像を加工できないようにして，SelectボタンとBackボタン，Closeボタンのみ押すことができる．
- 操作が終わるごとに適切なコメント文を出すように変更した．
- 顔が入れ替えられない場合やファイルが読み込めない場合にエラーを返すようにしている．

## 参考資料
- [Pythonの設定ファイル管理まとめ](https://kodocode.net/python-begin-settings/#:~:text=%E4%BD%BF%E3%81%84%E6%96%B9%E3%81%AF%E7%B0%A1%E5%8D%98%E3%81%A7%E3%81%99%E3%80%82%20%E4%BD%9C%E6%88%90%E3%81%99%E3%82%8BPython%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%A0%E3%81%A8%E5%90%8C%E3%81%98%E3%83%87%E3%82%A3%E3%83%AC%E3%82%AF%E3%83%88%E3%83%AA%E3%81%AB%E3%80%81%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E5%90%8D%E3%80%8Csettings.py%E3%80%8D%E3%81%AE%E8%A8%AD%E5%AE%9A%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%82%92%E7%BD%AE%E3%81%8D%E3%81%BE%E3%81%99%E3%80%82%20%E3%81%82%E3%81%A8%E3%81%AF,%E3%80%8Cimport%20settings%E3%80%8D%E3%81%A8%E5%86%92%E9%A0%AD%E3%81%AB%E8%A8%98%E8%BF%B0%E3%81%99%E3%82%8B%E3%81%A0%E3%81%91%E3%81%A7%E8%A8%AD%E5%AE%9A%E6%83%85%E5%A0%B1%E3%82%92%E8%AA%AD%E3%81%BF%E8%BE%BC%E3%82%80%E3%81%93%E3%81%A8%E3%81%8C%E3%81%A7%E3%81%8D%E3%81%BE%E3%81%99%20%28Python%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%A0%E3%81%AEimport%E3%81%AE%E4%BB%95%E7%B5%84%E3%81%BF%E3%82%92%E5%88%A9%E7%94%A8%E3%81%97%E3%81%A6%E3%81%84%E3%82%8B%29%E3%80%82)
- [[Python Tkinter] ボタンを押せないように無効化する方法](https://af-e.net/python-tkinter-button-disable/)
- [GrabCutを使った対話的前景領域抽出](https://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_grabcut/py_grabcut.html)
- [OpenCV 画像の色相、彩度、明度の変更【HSV】](https://sciencompass.com/machine-learning/opencv_rgb_hsv_change)
- [tkinterに、リセットボタンと終了ボタンを作る](https://program.kihituji8.com/tkinter%e3%81%ab%e3%80%81%e3%83%aa%e3%82%bb%e3%83%83%e3%83%88%e3%83%9c%e3%82%bf%e3%83%b3%e3%82%92%e4%bd%9c%e3%82%8b/)
