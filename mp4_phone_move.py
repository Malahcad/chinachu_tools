# ==================================================
# chinachu録画ファイルのスマホコピーバッチ
#
# 使用方法：
# 1.転送フォルダに転送対象ファイルを配置する
# 2.本バッチを実行するとスマホの/sdcard/aviに転送される
# ==================================================

# import
import numpy as np
import glob
from os.path import join,relpath

# 変数宣言
# 転送元ディレクトリ変数
SOURCE_DIR="C:\Work\mp4_phone_move\target"

# 転送先ディレクトリ変数
DESTINATION_DIR="/sdcard/avi"

# renameシェルのパス
RENAME_SHELL="/sdcard/temp/rename.sh"
RENAME_SHELL_LOCAL="C:\Work\chinachu_script\rename.sh"

# renameリストファイルのパス
RENAME_LIST="C:\Work\chinachu_script\rename_list.txt"
DEST_RENAME_LIST="/sdcard/temp/rename_list.txt"

# ファイル名配列

# ファイルリスト配列

# ループカウント変数
COUNT = 0

# ==================================================
# ファイルリスト作成処理
# ==================================================
# 転送元フォルダ内のファイル一覧を取得する
Arr_Target_Filename=[relpath(x,SOURCE_DIR) for x in glob(join(SOURCE_DIR, '*'))]
$ARR_TARGET_FILENAME=Get-ChildItem $SOURCE_DIR -Name

# ファイル名配列分ループし、文字列を作成する
ForEach($V in $ARR_TARGET_FILENAME){
    $ARR_CSV_DATA+="tempfile_" + $COUNT + ".tmp,$V"
    $COUNT = $COUNT + 1
}

# renameリストファイルに吐き出す
$Data = $ARR_CSV_DATA -Join "`n"
$Data | Out-File -FilePath $RENAME_LIST -Encoding UTF8

# ==================================================
# リネーム処理
# ==================================================
# renameリスト配列を使用し、ファイル名を変更する。（元ファイル名→仮ファイル名）
ForEach($V in $ARR_CSV_DATA) {
    $FILE_NAME=$V.Split(",")
    $Var1 = $SOURCE_DIR + "\" + $FILE_NAME[0]
    $Var2 = $SOURCE_DIR + "\" + $FILE_NAME[1]
    rename-item $Var2 -newName $Var1
}


# ==================================================
# 転送処理
# ==================================================
# shellとリストファイルの転送
Start-Process -FilePath adb.exe -ArgumentList "push $RENAME_SHELL_LOCAL $RENAME_SHELL" -Wait
Start-Process -FilePath adb.exe -ArgumentList "push $RENAME_LIST $DEST_RENAME_LIST" -Wait

# 対象ファイルを転送
ForEach($V in $ARR_CSV_DATA) {
    $FILE_NAME=$V.Split(",")
    Start-Process -FilePath adb.exe -ArgumentList "push $SOURCE_DIR\$FILE_NAME[0] $DESTINATION_DIR" -Wait
    if ($?){
        Write-Output "transfer success:" + $FILE_NAME[1]
    }else{
        Write-Output "transfer Failure:" + $FILE_NAME[1]
    }
}


# ==================================================
# ファイル名変更処理
# ==================================================
Start-Process -FilePath adb.exe -ArgumentList "shell sh $RENAME_SHELL" -Wait
if ($?){
    Write-Output "rename success"
}else{
    Write-Output "rename Failure"
}

exit 0
