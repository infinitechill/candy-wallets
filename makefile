#infinite chill / 2017
all: clean candy-wallets run

candy-wallets: candy-wallets.py
	cp candy-wallets.py candy-wallets
	chmod u+x candy-wallets
run:
	./candy-wallets

clean:
	rm -f candy-wallets
	
