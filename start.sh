#!/bin/bash

read -p "Please select a language version: (en/zh) " sel

if    [ "$sel" == "en" ];then 
             python ./en_vote_server.py	
elif [ "$sel" == "zh" ];then
	python ./ch_vote_server.py
fi