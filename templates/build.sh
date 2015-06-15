#!/bin/bash
# Creates the output file to deployment
# 

DIRSOURCE='/Users/horacioibrahim/Developer/projetos/siscomando/templates/'
DIRTARGET='/Users/horacioibrahim/Developer/projetos/siscomando/mockend/src/templates/'
FILESOURCE='build.html'
FILEOUTPUT='app.html'

# Replace the directory of the assets
DEVELOPMENTDIR='../../../templates/'
PRODUCTIONDIR='/static/'


# goto DIRSOURCE
cd $DIRSOURCE
vulcanize -o $DIRTARGET$FILEOUTPUT $FILESOURCE
cd $DIRTARGET
sed "#$DEVELOPMENTDIR#$PRODUCTIONDIR#g" $FILEOUTPUT > _app.html