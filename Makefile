
all: html

upload:
	git push origin master

update: 
	git push origin dev

index:
	doctoc README.md

html: README.md
	grip README.md --gfm --export README.html
