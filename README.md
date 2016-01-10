# SBC

http://jaub.developpez.com/tutoriels/weka/weka/

Nos données d'entrée concernent des plats, leurs ingrédients ainsi que leur origine obtenus sur la plateforme dbPedia.
Notre but est de prédire si un plat est Nord-Américain (Etats-Unis, Canada) ou non.

Pour cela, nous appliquons l'algorithme du Random Forest à l'aide du logiciel Weka. Pour convertir notre fichier .csv en .arff nous avons utilisé http://ikuz.eu/csv2arff/ qui est un convertisseur en ligne. Tous les champs vides doivent être rempli par un ? pour bien être interprétés par Weka.

Problèmes : un plat peut aussi être un ingrédient.

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