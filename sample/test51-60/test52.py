#math_scoreに何か適当な数値を代入して
#end_scoreに何か適当な数値を代入して
#jpn_scoreに何か適当な数値を代入します。
#これらは数学、英語、国語の点数です。
#全ての科目が80点以上なら"合格"
#1つでも80点未満の科目があれば"不合格"と出力してください

math_score=75
end_score=80
jpn_score=80

if math_score>=80 and end_score>=80 and jpn_score>=80:
    print("合格")
else:
    print("不合格")