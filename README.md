# SBC

http://jaub.developpez.com/tutoriels/weka/weka/

Nos données d'entrée concernent des plats, leurs ingrédients ainsi que leur origine obtenus sur la plateforme dbPedia.
Notre but est de prédire si un plat est Américain (Etats-Unis, Canada, Argentine, Brésil, Mexico, Cuba, Chili, Jamaica, Venezuela) ou non.

Pour cela, nous appliquons l'algorithme du Random Forest à l'aide du logiciel Weka. Pour convertir notre fichier .csv en .arff nous avons utilisé http://ikuz.eu/csv2arff/ qui est un convertisseur en ligne. Tous les champs vides doivent être remplis par un ? pour bien être interprétés par Weka.
Nous avons utilisé deux options de test du Random Forest : 
1) l'utilisation d'un ensemble d'apprentissage et de test avec deux fichiers distincts
2) la cross-validation à 10 plis qui brasse automatiquement les données pour construire 10 arbres avec des données d'apprentissage et de test qui sont définies aléatoirement à chaque construction d'arbre

Nous avons deux scripts de préprocessing :
- un qui transforme les données de dbPedia en tableau et leur attribue l'origine America ou Other_region
- l'autre qui enlève les doublons et qui brasse les données en deux fichiers : un jeu de test et un jeu d'entraînement

Problèmes : un plat peut aussi être un ingrédient, Weka ne supporte que des fichiers d'au plus 1000 lignes, les données de dbPedia sont mal formées.

Structure du fichier d'entrée :
--------------------------------------------------
Food | Ingr1 | Ingr2 | Ingr3 | ... | Origin
--------------------------------------------------
Soup | Tomato|   ?   |   ?   | ... | Other_region


Requête SPARQL :

SELECT DISTINCT ?Food ?Ingredient ?Origin
WHERE {{?Food a dbo:Food.
?Food dbo:origin ?Origin.
?Origin rdf:type dbo:Country.
?Food dbo:ingredient ?Ingredient.
}
UNION {?Food a dbo:Food.
?Food dbo:origin ?Origin2.
?Origin2 dbo:country ?Origin.
?Food dbo:ingredient ?Ingredient.
}}
ORDER BY ASC(?Food)