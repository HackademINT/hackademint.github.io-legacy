---
layout: default
---

<!-- List  -->
<h2 align="center"><u><b>Formations - Travaux Pratiques</b></u></h2>
<div class="wrapper style1">
  <div class="container">
    <section>
      <h3>&nbsp;&nbsp;<u><b>2018-2019</b></u></h3>
      <ul style="margin-left: 3em; margin-right:3em">
	<li>
	  <a href="./TP/Programmation/programmation.pdf">Programmation</a><br />
	</li>
	<li>
	  <a href="./TP/XSS_CSRF/xss_csrf.pdf">XSS/CSRF</a><br />
	</li>
	<li>
	  <a onclick="activate('TPPentestWeb1')">Pentest Web 1</a><br />
	  <div class="id" id="TPPentestWeb1">
	    <?php include('TP/Pentest/Pentest_Web_1.php') ?>
	  </div>
	</li>
	<li>
	  <a href="./TP/Hygiene_Numerique/tp_hygiene_numerique.pdf">Hygiène Numérique</a><br />
	</li>
	<li>
	  <a href="./TP/Ressources/tp_ressources.pdf">Ressources HackademINT</a><br />
	</li>
	  <!--
	  <li>
	    <a onclick="activate('TPPasscracking')">Passcracking</a><br />
	    <div class="id" id="TPPasscracking">
	      <?php include('TP/Passcracking/passcracking.php') ?>
	    </div>
	  </li>
	  -->
      </ul>
    </section>
  </div>
</div>
<div class="wrapper style1">
  <div class="container">
    <section>
      <h3>&nbsp;&nbsp;<u><b>2017-2018</b></u></h3>
      <ul style="margin-left: 3em; margin-right:3em">
	<li>
	  <a onclick="activate('TPWebCrawling')">Web Crawling</a><br />
	  <div class="id" id="TPWebCrawling">
	    <?php include('TP/WebCrawling/webcrawing.php') ?>
	  </div>
	</li>
	<li>
	  <a onclick="activate('TPRSA')">RSA</a><br />
	  <div class="id" id="TPRSA">
	    <?php include('TP/RSA/rsa.php') ?>
	  </div>
	</li>
      </ul>
    </section>
  </div>
</div>
<div class="wrapper style1">
  <div class="container">
    <section>
      <h3>&nbsp;&nbsp;<u><b>2016-2017</b></u></h3>
      <ul style="margin-left: 3em; margin-right:3em">
	<li>
	  <a href="TP/InjectionSQL/InjectionSQL.pdf">Injection SQL</a><br />
	</li>
	<li>
	  <a href="TP/post-exploitation.pdf">From webshell to root</a><br />
	</li>
	<!--
	<li>
	  <a href="TP/stapler.pdf">From nothing to root</a><br />
	</li>
	-->
      </ul>
    </section>
  </div>
</div>

<style>
section { margin: 10px; padding: 0px}
h2 { margin-bottom: 50px; }
</style>
