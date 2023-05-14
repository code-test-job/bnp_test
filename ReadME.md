# BNP PARIBAS - TEST
Bonjour!

Ci-dessous, l'intégralité des étapes de la résolution du challenge BNP Paribas !


*OBS1 :* Lisez attentivement le fichier README.md;

*OBS2 :* Je ne suis pas très fort en Nginx;

<h1>Structure des dossiers</h1>

<h2>Files</h2>

- `.gitignore`: Fichiers et répertoires à exclure du suivi et de la gestion des modifications;
- `Dockerfile`: Instructions pour construire l'image Docker;
- `nginx.conf`: Configuration pour le serveur web Nginx;
- `README.md`: Instructions du projet/solution;
- `requirements.txt`: Dépendances et packages nécessaires à l'exécution du projet;


<h2>Dossiers|Packages</h2>

- `app`: APP pour l'équipe A;
- `equipe_B`: Dossier avec les archives de l'équipe B;
- `tests`: Package avec les fonctions de test;


<h1>Suggestion de branches</h1>

- [x] master - Deploy en PROD
- [x] hml    - Deploy en STAGGING
- [x] dev    - Deploy en DEVELOPEMMENT

Pour lancer le docker il faut faire:

```
> docker build -t "test_bnp_paribas" --build-arg PYTHON_ENV="dev" --build-arg API_USERNAME="admin" --build-arg API_PASSWORD="mot_de_passe_fort" .

> docker run -p 5000:5000 --name test_container -e PYTHON_ENV="dev" -e API_USERNAME="admin" -e API_PASSWORD="mot_de_passe_fort" test_bnp_paribas

go to http://localhost:5000/docs
```



# Questions


<h1>1. Pouvez-vous leurs expliquer dans les grandes lignes la chaine de conception et déploiement d’une application IA et en quoi cela diffère d’une application logicielle standard ?</h1>

Dans une application logicielle standard l'objetif est de construire une solution pour communiquer entre programes ou ordinateurs a partir d'une série de commandes. Quand on pense au déploiement d'une application IA, nous avons aussi l'objetif de comuniquer entre interfaces, mais pour se faire il faut des caractéristiques spécifiques de l'IA. Par exemple, dans une application IA, nous commençerons dès la collecte et la préparation des données jusqu'au déploiement, mais ce n'est pas aussi simple, parce qu'il est necessaire d'entraîner le modèle, évaluer le modèle et aussi le ré-entraîner de temps en temps. Pour cette raison la constrution, par exemple d'une API Rest, est juste une petite partie de la vie d'un déploiement d'une Inteligence Artificielle. 


<h1>2. Équipe A :  développe une API REST écrite en Python avec un seul endpoint qui fait un calcul relativement long</h1>

Le problème du temps de réponse est un des problèmes les plus communs dans le déploiement d'une API. La résolution de cette question s'affiche dans l'archive app/main.py et est expliqué ici.

D'abord le framework utilisé a été changé de Flask pour FastAPI pour sa facilité d'écrire en FastAPI, son asynchronicité et aussi pour le fait que le programmer qui vous écrit, programme mieux en FastAPI. Néanmoins, Flask était aussi un bon framework pour ce problème. 

Le calcul relativement long s'agit d'un factoriel et le problème évident etait le fait que dans le code, le factoriel a été calculé en utilisant un for-loop. Cependant, même en résolvant ce problème, on aurait encore le probleme de Floating Point. Pour être clair, les nombres réels sont représentés au format binaire dans la mémoire de l'ordinateur, en utilisant un nombre fini de bits pour stocker la valeur et la position du point décimal. Cependant, de nombreux nombres rationnels ne peuvent pas être représentés exactement en binaire, ce qui entraîne des approximations. Ces approximations introduisent des erreurs d'arrondi, qui peuvent se propager et affecter les résultats des calculs.

À cause de cela, pour résoudre ces deux problèmes, la librairie mpmath qui fonctione très bien pour un nombre N très grand a été utilisé et son résultat était transformé en type string. De plus, le factorial_cache a été implémenté, en tant que dictionnaire de factoriels déjà calculés, c'est-à-dire que tout factoriel déjà calculé est enregistré dans ce dictionnaire et est stocké dans la mémoire cache, donc si ce même numéro est envoyé à la requête, il ne sera pas nécessaire de recalculer le factoriel, mais seulement de retourner le factoriel du dictionnaire factorial_cache.

```
> uvicorn app.main:app --reload --log-level debug
```


*OBS1 :* Certaines améliorations systématiques ont également été appliquées, telles que le typage;
*OBS2 :* Middleware a été implanté afin de voir le temps de réponse de la requête;
*OBS3 :* Tests unitaires ont été implanté afin de tester l'application.


<h1>3. Équipe B : développe un SDK Python qui fait plusieurs appels à l’API développée par l’équipe A et qui doit finir l’exécution en un temps T relativement petit</h1>

En sachant que le problème de l'équipe A a été resolu, le problème de l'équipe B s'est minimisé, donc un seul petit changement est necéssaire. La résolution de cette question s'affiche dans l'archive equipe_B/sdk_requests.py et est expliqué ici.

La résolution s'agit d'accélérer le processus de rêquetes de data (qui vient de la route /long-calculation). Pour cela, ThreadPoolExecutor a été implanté pour exécuter la fonction fetch_data en parallèle pour chaque ressource en limitant le nombre X maximum de threads, qui dans ce cas, a été mis comme 4 threads. De plus dans le ThreadPoolExecutor est utilisé un time.sleep, pour éviter la surcharge du server avec beaucoup de rêquetes en peu de temps.

*OBS1 :* Certaines améliorations systématiques ont également été appliquées, telles que le typage;


<h1>4. Dockerfile</h1>

Les problèmes "L’api est accessible publiquement et n’utilise pas la solution d’authentification standard de l’entreprise" et "Mots de passe contenus dans la configuration" on été resolu en utilisant $API_USERNAME $API_PASSWORD, qui sont passés dans le déploiment avec les variables d'environnement fournies par l'authentification standard de l'entreprise

Le problème "Pas de logs générés" a été resolu avec la dernière ligne du dockerfile, avec l'instruction --log-level=info, mais aussi ça serait interessant d'utiliser un hook pour loggings dans le Cloud Logging (GCP)

Le problème "Pas de filtrage web" a été resolu dans l'archive nginx.conf comme un commentaire où l'adresse IP viens selon les besoins de l'enterprise

<h1>5. Après résolution, vous remarquez que l’application se trouve vite surchargée en appels réseau. Quels seraient les raisons internes et externes a l’app ? Solutions potentielles (réseau et autres) ?</h1>

Les raisons internes pourraient-être une mauvaise conception de l'API ou une mauvaise gestion de la mémoire cache, ce qui n'est pas le cas, une fois que ces problèmes ont déjà été resolu. Les raisons externes pourraient-être une augmentation très grande d'utilisateurs ou un mauvais équilibrage de charge. La solution serait donc d'ajuster les capacités de l'infrastructure kubernetes et mieux configurer un équilibrage de charge pour distribuer efficacement le trafic entre les différents pods.


<h1>6. Code Python très critique </h1>

List, Callable, Any ont été implanté en utilisant typing. Après lancer mypy aucun problème ne s'est produit. La résolution de cette question s'affiche dans l'archive equipe_B/critique.py

<h1>Si vous avez des questions, n'hésitez pas à envoyer un commentaire</h1>