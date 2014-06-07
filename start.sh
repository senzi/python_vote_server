#!/bin/bash
echo -e "请选择语言版本"
echo -e "en or zh"
read -p "Please select a language version:  " sel

if    [ "$sel" == "en" ];then 
             python ./en_vote_server.py	
elif [ "$sel" == "zh" ];then
	python ./ch_vote_server.py
fi