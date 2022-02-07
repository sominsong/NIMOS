OUTPUT=/opt/output/

## Install dependencies and configure
build: 
	./configure.sh
	./setup.sh

## Remove previous temporal output directory
clean:
	rm -rf $(OUTPUT)temp/*

## Remove previous temporal/permanent output directory
clean-all:
	rm -rf $(OUTPUT)temp/* $(OUTPUT)perm/*
