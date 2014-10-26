Sandbox
=======
##Files
###crawler.py

This file is a simple crawler using requests and pattern python packages to build a NetworkX directed graph. It follows all the links corresponding to a given pattern and adds a node for every new page that has been discovered.


###db_storage.csv

> In progress. Feel free to help by completing this file or by adding some modifications to the database.

This db includes some information about storage in order to create an interactive timeline on data storage devices. The structure of the database is not definitive yet. Some columns might be added or removed in the next few days.

Field description:
* *Id*
* *Device:* Storage name (ie. Compact Disk, Floppy Disk...).
* *CreationDate:* First commercialized product (not invention as it is quite difficult to determine the precise invention dates of some storage types.
* *EndDate:* Only exists if the product manufacturing has been discontinued
* *StorageType:* Group similar devices (same technology or same form-factor) within the same label (ie. flash devices or disks)
* *Format:* Differentiate evolutions of the same technology (5"1/4 vs 3"1/2 floppy disks or CD vs mini-disks)
* *DataType:*	If it has only be used for some kind of datatype, this one has to be precised here (may disappear in a future update as it may not be as relevant as I thought first)
* *ImagePath:* Path to free illustration (accepted licences to be determined)
* *KbPrice:* Price per kb of data in *CreationDate*
* *Capacity:* May be an float followed by the uppercase units (xMB) or a range (*xKB-yGB*) if it has evolved during the lifespan of the product.
