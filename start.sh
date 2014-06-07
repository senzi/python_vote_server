#!/bin/bash
echo -e "(en/zh)\nqing ni xuan zhe yi ge yu yan ban ben"
read -p "Please select a language version:  " sel

if    [ "$sel" == "en" ];then 
             python ./en_vote_server.py	
elif [ "$sel" == "zh" ];then
	python ./ch_vote_server.py
fi