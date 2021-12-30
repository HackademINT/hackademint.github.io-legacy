---
title: "SluffleShop"
subtitle: "Challenge de Web de la finale du FCSC 2020"
published: true
author: "Bdenneu"
ctf: "FCSC_FINALE"
annee: "2020"
---

# L'énoncé

Vous venez d'entrer dans un château ...

URL : http://shuffleshop.fcsc/

# A l'assaut!

![](/assets/images/FCSCFINALE2020/Shuffleshop/1.png)

![](/assets/images/FCSCFINALE2020/Shuffleshop/2.png)

```js
var potions = JSON.parse('[{"idx":0,"name":"Health potion","price":10,"color":"#ff0000"},{"idx":1,"name":"Stamina potion","price":10,"color":"#33cc33"},{"idx":2,"name":"Strengh potion","price":15,"color":"#996633"},{"idx":3,"name":"Clerverness potion","price":15,"color":"#99ffcc"},{"idx":9,"name":"Flag potion","price":100000,"color":"#ffff00"},{"idx":4,"name":"Breath potion","price":25,"color":"#00ffcc"},{"idx":5,"name":"Invisible potion","price":30,"color":"#ffffcc"},{"idx":6,"name":"Fly potion","price":59,"color":"#ff99ff"},{"idx":7,"name":"Love potion","price":99,"color":"#ff0066"},{"idx":8,"name":"Fire-protection potion","price":67,"color":"#ff6600"}]');
	var cart_enc = "";
	var p1 = 0, p2 = 1, p3 = 2;

	function displayPotions()
	{
		document.getElementById('potion_name_1').innerHTML = potions[p1]['name'];
		document.getElementById('potion_name_1').style = "background-color:" + potions[p1]['color'];
		document.getElementById('potion_price_1').innerHTML = potions[p1]['price'];
		document.getElementById('potion_buy_1').onclick = function(){addItem(potions[p1]['idx']);};

		document.getElementById('potion_name_2').innerHTML = potions[p2]['name'];
		document.getElementById('potion_name_2').style = "background-color:" + potions[p2]['color'];
		document.getElementById('potion_price_2').innerHTML = potions[p2]['price'];
		document.getElementById('potion_buy_2').onclick = function(){addItem(potions[p2]['idx']);};

		document.getElementById('potion_name_3').innerHTML = potions[p3]['name'];
		document.getElementById('potion_name_3').style = "background-color:" + potions[p3]['color'];
		document.getElementById('potion_price_3').innerHTML = potions[p3]['price'];
		document.getElementById('potion_buy_3').onclick = function(){addItem(potions[p3]['idx']);};
	}

	function shuffleStand()
	{
		var max = potions.length;
		p1 = Math.floor(Math.random() * max);
		p2 = Math.floor(Math.random() * max);
		p3 = Math.floor(Math.random() * max);
		displayPotions();
	}

	function addItem(idx)
	{
		var xhr_addItem = new XMLHttpRequest();
		xhr_addItem.open("GET", "cart.php?add&idx="+idx, true);
		xhr_addItem.onload = function()
		{
			if(this.readyState === XMLHttpRequest.DONE && this.status === 200)
			{
				if(this.responseText === "not enough FCSC-coins")
					alert("Le montant de votre panier ne peut pas dépasser la quantité de FCSC-coins que vous possédez !");
				else if(this.responseText === "potion added")
					refreshCart();
			}
		}
		xhr_addItem.send();
	}

	function refreshCart()
	{
		var xhr_refreshCart = new XMLHttpRequest();
		xhr_refreshCart.open("GET", "cart.php?refresh", true);
		xhr_refreshCart.onload = function()
		{
			if (this.readyState === XMLHttpRequest.DONE && this.status === 200)
				document.getElementById('cart').innerHTML = this.responseText;
		}

		var xhr_refreshCartEnc = new XMLHttpRequest();
		xhr_refreshCartEnc.open("GET", "cart.php?refreshEnc", true);
		xhr_refreshCartEnc.onload = function()
		{
			if (this.readyState === XMLHttpRequest.DONE && this.status === 200)
				cart_enc = this.responseText;
		}

		xhr_refreshCart.send();
		xhr_refreshCartEnc.send();
	}

	function validateCart()
	{
		refreshCart();
		var xhr_validateCart = new XMLHttpRequest();
		xhr_validateCart.open("GET", "cart.php?validate&cart="+cart_enc, true);
		xhr_validateCart.onload = function()
		{
			if (this.readyState == XMLHttpRequest.DONE && this.status === 200)
				alert(this.responseText);
		}
		xhr_validateCart.send();
	}
```


J'ai ici supposé que la clé ne changeait pas (ça n'aurait pas de sens d'en changer). Aussi, la carte était indépendante, et la taille coincidait avec celle du message affiché:


```json
{"total":0,"Health potion":0,"Stamina potion":0,"Strengh potion":0,"Clerverness potion":0,"Flag potion":0,"Breath potion":0,"Invisible potion":0,"Fly potion":0,"Love potion":0,"Fire-protection potion":0}```


Le card_enc comprennait 13 blocs d'AES ECB.


{"total":0,"Health potion":0,"Stamina potion":0,"Strengh potion":0,"Clerverness potion":0,"Flag potion":0,"Breath potion":0,"Invisible potion":0,"Fly potion":0,"Love potion":0,"Fire-protection potion":0}


L'idée va être de remplacer le bloc 'potion": 0,"Flag' par un autre bloc à 1. Le nom importe peu vu que le programme bosse avec des ids. Donc acheter une potion de Clerverness et remplacer le bloc de flag suffira.


![](/assets/images/FCSCFINALE2020/Shuffleshop/3.png)


![](/assets/images/FCSCFINALE2020/Shuffleshop/4.png)


# Flag

FCSC{c9582322dfa2997384b7d38b73b5a80a69374d5f3f616c431e98823172f5c7df}


