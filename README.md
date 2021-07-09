# Fotocodering
Dit is een tooltje om aan de hand van een excel bestand de codering van een foto met een druk op de knop te veranderen.

Allereerst wordt via het excel bestand de kolom 'barcode' gezocht. Die kolom samen met andere kolommen vormen de nieuwe codering.
De EAN code (barcode) wordt gematcht met een bestaande foto naam bv: 1234567891234.png. Pandas merge left join. left in dit geval is de smslijst.xlsx

Vervolgens wordt de naam van de afbeelding veranderd in de gematchte barcode naar de andere kolommen uit excel.
kolommen zijn: ProductID, Product, Color, soort

