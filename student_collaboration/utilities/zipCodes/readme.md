## Utilities ~ zip code position generation

### If the postal code entries in empty in the collaborative tool simply add the `zipcodes.sql` to the database ! 



### zipCodes Generator:

Based on all existing Belgian zip code we find -  using Google Map API - it's geographical position in order to after evaluate distance between 2 users.

The source code is still here in case change happens (either in the country, in the API we use, etc.)

The `csv`source is from http://www.bpost.be/site/fr/envoyer/adressage/rechercher-un-code-postal/ (excel converted as csv after purge of useless zipcodes)



Just launch the `py` code (either in python 2.7 or 3) to update the `sql`

`googlemaps` should be preinstalled :

```pip install -U googlemaps```

Need to modify the code if any change in the table structure/scheme 