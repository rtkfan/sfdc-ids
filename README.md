# SFDC ID conversion utility
Simple library that converts Salesforce IDs between the SFDC internal 15-character form, and the case-insensitive 18-character form.

More background and description of the algorithm from [this StackExchange post](https://salesforce.stackexchange.com/questions/1653/what-are-salesforce-ids-composed-of), but essentially: The last 3 characters are used to encode case information of the first 15 characters, so that IDs can be reliably compared in systems that treat string comparison case-insensitively (like Excel):

- Each 15-digit ID is split into 3 5-digit chunks
- Each 5-digit chunk's casing information is encoded into a 5-bit integer (MSB to the right), mapped to the character set `[A-Z0-5]`, in that order
- These three digits are appended to the end of the 15-bit ID, making it unique case-insensitive.
