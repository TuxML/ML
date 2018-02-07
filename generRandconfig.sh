#!/bin/bash

cwd=`pwd`
mkdir -p configs
cd $1
for i in `seq 1 100`;
do
#Faire ces actions tant qu'on a pas generer le bon nombre de .config
echo "config numero" $i 1>&2
KCONFIG_ALLCONFIG="$cwd"/../core/tuxml.config make randconfig
echo " " 1>&2
cp .config $cwd/configs/$i.config
done
