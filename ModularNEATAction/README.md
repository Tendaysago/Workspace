## Action Game + NEAT + Modular Network ##

アクションゲーム学習におけるモジュラーネットワークの導入にて使用したプログラム。  
アクションゲームの基盤の作成には以下を基とし,画像は独自に描いた(自機はデザインを参考にした)。  
["Github aidiary/pygame/tree/master/action"](https://github.com/aidiary/pygame/tree/master/action)  
動作にはpygameとneat-python(と,それらの依存関係のプログラム)が必要。  
これらの実行にあたっては,python3.6.5,pygame 1.9.5,neat-python-0.92を想定している。  

## プログラム,フォルダーとそれらの仕様について ##  

'snakecheck.py':実際にアクションゲームを遊ぶ場合に起動。  
'snaketrain2.py':アクションゲームを学習させる際に,訓練環境として使用  
(画面が出ず,キー入力を受け付けない事以外は,snakecheckとほとんど同じ…筈。)  
* 'evolve-...のファイル群':ネットワークを進化させる際に使用。  
    -easyenemystage.py:15種類の内比較的難易度が低いとみなされた10個のエネミーステージを学習する。  
    -easyjumpstage.py:15種類の内比較的難易度が低いとみなされた10個のジャンプステージを学習する。  
    -singleenemy.py:15種類のエネミーステージの内,一つのステージだけを学習する。  
    -singlejump.py:15種類のジャンプステージの内,一つのステージだけを学習する。  
    -jumpstate:15種類のジャンプステージをランダムな順序で学習する。  
    -enemystage:15種類のエネミーステージをランダムな順序で学習する。  
    -multistage:難易度の高いステージを一つ指定し,  
    evolve-enemystage.pyとevolve-jumpstage.pyで作成したネットワークをモジュラーネットワークとして学習する。  
    -multistageeasy:難易度の高いステージを一つ指定し,  
    evolve-easyenemystage.pyとevolve-easyumpstage.pyで作成したネットワークをモジュラーネットワークとして学習する。  
    -multistagesingle:難易度の高いステージを一つ指定し,  
    evolve-singleenemy.pyとevolve-singlejump.pyで作成したネットワークをモジュラーネットワークとして学習する。  
    -multi-normalneat:難易度の高いステージを一つ指定し,evolve-enemystageなど同じ設定で,普通にNEATによる学習を行う。  
'snakecheckAutoplay.py':進化させたエネミーネットワーク,ジャンプネットワークによってどのようなプレイになるか確認する為に使用。  
'snakecheckAutoplay_multi.py':難しいステージに対して,モジュラーネットワークを導入した結果どのようなプレイになるか確認する為に使用。  
’visualize.py':学習後のネットワークの画像ファイルの出力に使用  
(neat-pythonライブラリ内でネットワークの可視化に使用しているvisualizeファイルをそのまま使用)  

* 'Network':学習する中で得られたネットワーク群を格納したフォルダー。  
上手な戦略を獲得したネットワークもあれば,適当な戦略に落ち着いたネットワークもある。  
    -winner-action-enemy-[Num]:evolve-enemystageによる学習を通して得られたネットワーク  
    -winner-action-jump-[Num]:evolve-jumpstageによる学習を通して得られたネットワーク  
    -winner-action-easyenemy-[Num]:evolve-easyenemystageによる学習を通して得られたネットワーク  
    -winner-action-easyjump-[Num]:evolve-easyjumpstageによる学習を通して得られたネットワーク  
    -winner-enemyNo[Num]:evolve-singleenemyによる学習を通して得られたネットワーク  
    -winner-jumpNo[Num]:evolve-singlejumpによる学習を通して得られたネットワーク  
    -winner-multi-No[Num]:evolve-multistageによる学習を通して得られたネットワーク  

*'data':ゲームを実行するのに必要なデータ。拡張子でファイルの種類が決まっている  
-.map:ステージマップのデータファイル。中身はテキストデータであり,このテキストデータを基にしてマップを生成している。  
-.bmp:ゲーム内で使用したゲームオブジェクトの画像ファイル。  
-.ene:敵のデータファイル。接触ダメージや,倒した時の得点,移動速度などが設定できる。  
-.item:アイテムのデータファイル。今はコインとゴールと回復アイテムのみ。  

*'config-...ファイル群と,multi-only':neat-pythonの実行に必要なパラメーターの設定ファイル.  



## TO DO ##  
・ゲームオブジェクトの種類の追加  
・evolve-...ファイルでステージクリアまで学習できたネットワークが,  
snakeAutoplay.pyで確認した場合に,途中でゲームオーバーになる事がある不具合への対処。  
・より多様なステージの追加  
・evolve-multi...シリーズで使用するモジュラーネットワークを丸ごとソースコード内に書いている為,  
使用するモジュラーネットワークの指定などの機能の追加。  
