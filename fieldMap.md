Name > Name
Image URL > Image URL
Flavor text > Entry
Type > Type (
  Artifact > Item,
  Creature > Character,
  Artifact Creature > Character,
  Land > Location,
  None of the above > 0
  )
If TYPE in (Artifact Creature, Creature), and if SUBTYPE in (Vedalken * , 
Human * , Dwarf * , Aetherborn * ) then RACE = Subtype.split(" ")[0]

If TYPE in (Artifact Creature, Creature), Subtype>Title
